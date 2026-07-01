"""
media.py — UPSC Master Bot Parallel Image Loading
===================================================
ARCHITECTURE: Images load IN PARALLEL with message text.
The user sees content INSTANTLY. The image swaps in silently in background.

Flow:
1. edit_message_caption() → text appears INSTANTLY (0ms delay)
2. asyncio.create_task(_swap_image()) → image loads in background
3. If file_id cached → edit_message_media() with file_id (near-instant)
4. If no cache → upload file from disk → cache file_id → swap image
5. If image fails → text content already visible, user unaffected

CAPTION LENGTH SAFETY:
Telegram limits photo/video CAPTIONS to 1024 characters, while plain text
messages allow up to 4096. Several screens in this bot (plan analysis,
task details, framework references, help text) legitimately need more
than 1024 characters of pre-generated content. If we blindly called
edit_caption() with long text, Telegram would reject the request and the
edit would silently fail — leaving the user stuck looking at a stale
screen with no error shown.

To handle this safely: any caption over CAPTION_SAFE_LIMIT is rendered as
a plain TEXT message instead (no image, full 4096-char budget). Short
captions keep the full "instant text + parallel image" experience. This
check is centralised here so every handler gets the safety automatically.
"""
import asyncio
import logging
import pathlib

from telegram import InputMediaPhoto, Message
from telegram.error import BadRequest, TelegramError
from telegram.ext import ContextTypes

import config
from storage.database import save_image_cache, log_error

logger = logging.getLogger(__name__)

HTML = "HTML"

# Telegram's real limit is 1024; keep a safety margin for emoji/entity overhead.
CAPTION_SAFE_LIMIT = 950


# ── Core navigation function ───────────────────────────────────────────────────

async def show_section(
    query,
    context: ContextTypes.DEFAULT_TYPE,
    image_key: str,
    caption: str,
    keyboard,
    background_image: bool = True,
) -> None:
    """
    Navigate to a bot section.

    INSTANT: Shows text caption immediately (removes Telegram spinner).
    PARALLEL: Loads/swaps the section image in background.
    SAFE: Automatically falls back to a plain text message (no image) when
    the content is too long to fit Telegram's 1024-char caption limit.

    Args:
        query: CallbackQuery object
        context: PTB context
        image_key: Key in config.IMAGE_FILES (e.g. "tasks", "progress")
        caption: HTML-formatted message text
        keyboard: InlineKeyboardMarkup
        background_image: If False, skip image (text-only sections)
    """
    # ── Step 1: Remove spinner IMMEDIATELY ────────────────────────────────────
    try:
        await query.answer()
    except Exception:
        pass

    is_long = len(caption) > CAPTION_SAFE_LIMIT

    if is_long:
        # Long content can't fit a photo caption. Render as plain text with
        # the full 4096-char budget instead of risking a silent edit failure.
        await _show_long_text(query, caption, keyboard)
        return

    # ── Step 2: Show text INSTANTLY ───────────────────────────────────────────
    edit_ok = False
    needs_resend = False
    current_message = query.message  # local reference; query.message itself is immutable
    try:
        if current_message and current_message.photo:
            await current_message.edit_caption(
                caption=caption,
                parse_mode=HTML,
                reply_markup=keyboard,
            )
            edit_ok = True
        else:
            await current_message.edit_text(
                text=caption,
                parse_mode=HTML,
                reply_markup=keyboard,
            )
            edit_ok = True
    except BadRequest as e:
        msg = str(e).lower()
        if "not modified" in msg:
            edit_ok = True  # Content unchanged — that's fine
        else:
            # Message is in an unexpected state (deleted, wrong content type,
            # stale reference, etc). Rather than leaving the user stuck on a
            # stale screen, self-heal by sending a fresh message below.
            logger.debug("show_section edit failed, will self-heal: %s", e)
            needs_resend = True
    except Exception as e:
        logger.warning("show_section step2 failed: %s", e)
        needs_resend = True

    if needs_resend and current_message:
        # Self-heal: delete the broken message and send a fresh one. Since
        # the caption is short here (long captions already returned above),
        # this still qualifies for the photo treatment via Step 3 below —
        # but we need a live message to attach Step 3's background task to,
        # so send fresh text first, then let Step 3 upgrade it to a photo.
        try:
            await current_message.delete()
        except Exception:
            pass
        try:
            current_message = await current_message.chat.send_message(
                text=caption, parse_mode=HTML, reply_markup=keyboard,
            )
        except Exception as e:
            logger.warning("show_section self-heal resend failed: %s", e)
            return

    # ── Step 3: Swap image in background ──────────────────────────────────────
    if background_image and current_message:
        asyncio.create_task(
            _swap_image_background(
                message=current_message,
                image_key=image_key,
                caption=caption,
                keyboard=keyboard,
            )
        )


async def _show_long_text(query, caption: str, keyboard) -> None:
    """
    Render long content (> CAPTION_SAFE_LIMIT) as a plain text message.
    If the current message is a photo, it's replaced with a fresh text
    message since Telegram cannot convert a photo message into plain text
    in-place.
    """
    message = query.message
    try:
        if message and not message.photo:
            # Already a text message — simple edit, up to 4096 chars.
            await message.edit_text(text=caption, parse_mode=HTML, reply_markup=keyboard)
            return
    except BadRequest as e:
        if "not modified" in str(e).lower():
            return
        logger.debug("_show_long_text edit_text failed, will resend: %s", e)
    except Exception as e:
        logger.debug("_show_long_text edit_text error, will resend: %s", e)

    # Current message is a photo (or edit failed) — delete and send fresh text.
    try:
        if message:
            await message.delete()
    except Exception:
        pass
    try:
        if message:
            await message.chat.send_message(text=caption, parse_mode=HTML, reply_markup=keyboard)
    except Exception as e:
        logger.warning("_show_long_text send_message failed: %s", e)


async def _resend_as_photo(message: Message, image_key: str, caption: str, keyboard) -> None:
    """
    Self-healing path: the existing message can't be edited into the shape
    we need (e.g. it was a text message and we now want a photo). Delete it
    and send a fresh photo message so future short screens regain images.
    """
    chat = message.chat
    try:
        await message.delete()
    except Exception:
        pass

    file_id = config.IMAGE_CACHE.get(image_key)
    filename = config.IMAGE_FILES.get(image_key, "")
    img_path = config.IMAGES_DIR / filename if filename else None

    if file_id:
        try:
            await chat.send_photo(photo=file_id, caption=caption, parse_mode=HTML, reply_markup=keyboard)
            return
        except BadRequest:
            config.IMAGE_CACHE.pop(image_key, None)
        except Exception as e:
            logger.debug("_resend_as_photo cached file_id failed: %s", e)

    if img_path and img_path.is_file():
        try:
            with open(img_path, "rb") as f:
                msg = await chat.send_photo(photo=f, caption=caption, parse_mode=HTML, reply_markup=keyboard)
            if msg and msg.photo:
                fid = msg.photo[-1].file_id
                config.IMAGE_CACHE[image_key] = fid
                save_image_cache(image_key, fid)
            return
        except Exception as e:
            logger.debug("_resend_as_photo disk upload failed: %s", e)

    # Last resort: plain text (still better than nothing)
    try:
        await chat.send_message(text=caption, parse_mode=HTML, reply_markup=keyboard)
    except Exception as e:
        logger.warning("_resend_as_photo text fallback failed: %s", e)


async def _swap_image_background(
    message: Message,
    image_key: str,
    caption: str,
    keyboard,
) -> None:
    """
    Background task: swap in the section image.
    Silently fails — user already sees text content.
    Self-heals if the message has no existing media to edit (e.g. it was
    previously a long-content text message) by deleting and resending as
    a fresh photo message.
    """
    try:
        # Check in-memory cache first (fastest)
        file_id = config.IMAGE_CACHE.get(image_key)

        if file_id:
            # Use cached Telegram file_id — very fast
            await message.edit_media(
                media=InputMediaPhoto(
                    media=file_id,
                    caption=caption,
                    parse_mode=HTML,
                ),
                reply_markup=keyboard,
            )
            return

        # Load from disk
        filename = config.IMAGE_FILES.get(image_key, "")
        if not filename:
            return  # No image defined for this key

        img_path = config.IMAGES_DIR / filename
        if not img_path.is_file():
            logger.debug("Image file not found: %s", img_path)
            return

        # Upload file to Telegram and cache the file_id
        with open(img_path, "rb") as f:
            result = await message.edit_media(
                media=InputMediaPhoto(
                    media=f,
                    caption=caption,
                    parse_mode=HTML,
                ),
                reply_markup=keyboard,
            )

        # Cache the file_id for future instant loads
        if result and result.photo:
            fid = result.photo[-1].file_id
            config.IMAGE_CACHE[image_key] = fid
            save_image_cache(image_key, fid)
            logger.debug("Cached file_id for image_key=%s", image_key)

    except BadRequest as e:
        msg = str(e).lower()
        if "message is not modified" in msg:
            pass  # Fine — content same
        elif "wrong file" in msg or "file_id" in msg:
            # Stale file_id — clear and will be re-uploaded next time
            config.IMAGE_CACHE.pop(image_key, None)
            logger.info("Cleared stale file_id for key=%s", image_key)
        else:
            # Covers "there is no media in the message to edit" and any other
            # edit-media failure mode. Rather than relying on exact wording
            # from Telegram's API (which can shift), self-heal by default:
            # delete and resend fresh as a photo message so future short
            # screens regain their image instead of staying silently stuck
            # on text-only.
            logger.debug("_swap_image_background BadRequest, self-healing: %s", e)
            asyncio.create_task(_resend_as_photo(message, image_key, caption, keyboard))
    except TelegramError as e:
        logger.debug("_swap_image_background TelegramError: %s", e)
    except Exception as e:
        logger.debug("_swap_image_background error: %s", e)


# ── Send new photo message (for onboarding or non-edit contexts) ──────────────

async def send_photo_message(
    context: ContextTypes.DEFAULT_TYPE,
    chat_id: int,
    image_key: str,
    caption: str,
    keyboard=None,
) -> Message | None:
    """
    Send a new photo message (not an edit).
    Tries cached file_id first; falls back to disk upload; falls back to text.
    Long captions (> CAPTION_SAFE_LIMIT) skip the photo entirely and go
    straight to a plain text message, since Telegram would reject an
    over-length caption outright.
    """
    if len(caption) > CAPTION_SAFE_LIMIT:
        try:
            return await context.bot.send_message(
                chat_id=chat_id,
                text=caption,
                parse_mode=HTML,
                reply_markup=keyboard,
            )
        except Exception as e:
            logger.error("send_photo_message long-text send failed: %s", e)
            return None

    file_id = config.IMAGE_CACHE.get(image_key)
    filename = config.IMAGE_FILES.get(image_key, "")
    img_path = config.IMAGES_DIR / filename if filename else None

    # Try cached file_id
    if file_id:
        try:
            return await context.bot.send_photo(
                chat_id=chat_id,
                photo=file_id,
                caption=caption,
                parse_mode=HTML,
                reply_markup=keyboard,
            )
        except BadRequest:
            # Stale file_id — clear it
            config.IMAGE_CACHE.pop(image_key, None)

    # Try uploading from disk
    if img_path and img_path.is_file():
        try:
            with open(img_path, "rb") as f:
                msg = await context.bot.send_photo(
                    chat_id=chat_id,
                    photo=f,
                    caption=caption,
                    parse_mode=HTML,
                    reply_markup=keyboard,
                )
            # Cache the file_id
            if msg.photo:
                fid = msg.photo[-1].file_id
                config.IMAGE_CACHE[image_key] = fid
                save_image_cache(image_key, fid)
            return msg
        except Exception as e:
            logger.warning("send_photo_message disk upload failed key=%s: %s", image_key, e)

    # Fallback: text-only message
    try:
        return await context.bot.send_message(
            chat_id=chat_id,
            text=caption,
            parse_mode=HTML,
            reply_markup=keyboard,
        )
    except Exception as e:
        logger.error("send_photo_message text fallback failed: %s", e)
        return None


async def edit_to_text(
    query,
    caption: str,
    keyboard=None,
) -> None:
    """Edit a message to plain text (no image). Used for simple info screens."""
    try:
        await query.answer()
    except Exception:
        pass
    try:
        if query.message and query.message.photo:
            await query.message.edit_caption(
                caption=caption,
                parse_mode=HTML,
                reply_markup=keyboard,
            )
        else:
            await query.message.edit_text(
                text=caption,
                parse_mode=HTML,
                reply_markup=keyboard,
            )
    except BadRequest as e:
        if "not modified" not in str(e).lower():
            logger.warning("edit_to_text failed: %s", e)
    except Exception as e:
        logger.warning("edit_to_text error: %s", e)


async def safe_answer(query) -> None:
    """Safely answer a callback query, ignoring errors."""
    try:
        await query.answer()
    except Exception:
        pass


def preload_image_cache() -> None:
    """
    Load image file_ids from DB into in-memory cache at startup.
    Called once during bot initialization.
    """
    from storage.database import load_image_cache as db_load
    cache = db_load()
    config.IMAGE_CACHE.update(cache)
    logger.info("✅ Image cache loaded | %d entries", len(cache))


async def edit_to_text(
    query,
    caption: str,
    keyboard=None,
) -> None:
    """Edit a message to plain text (no image). Used for simple info screens."""
    try:
        await query.answer()
    except Exception:
        pass
    try:
        if query.message and query.message.photo:
            await query.message.edit_caption(
                caption=caption,
                parse_mode=HTML,
                reply_markup=keyboard,
            )
        else:
            await query.message.edit_text(
                text=caption,
                parse_mode=HTML,
                reply_markup=keyboard,
            )
    except BadRequest as e:
        if "not modified" not in str(e).lower():
            logger.warning("edit_to_text failed: %s", e)
    except Exception as e:
        logger.warning("edit_to_text error: %s", e)


async def safe_answer(query) -> None:
    """Safely answer a callback query, ignoring errors."""
    try:
        await query.answer()
    except Exception:
        pass


def preload_image_cache() -> None:
    """
    Load image file_ids from DB into in-memory cache at startup.
    Called once during bot initialization.
    """
    from storage.database import load_image_cache as db_load
    cache = db_load()
    config.IMAGE_CACHE.update(cache)
    logger.info("✅ Image cache loaded | %d entries", len(cache))
