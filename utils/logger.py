"""
utils/logger.py — UPSC Master Bot Logging Setup
=================================================
Rotating file logger: logs/upsc_bot.log, max 5MB, 3 backups.
Structured log format with timestamp, level, module, function.
"""
import logging
import logging.handlers
import pathlib
import sys


def setup_logging(level: int = logging.INFO) -> None:
    """Configure root logger with console + rotating file handlers."""
    root_logger = logging.getLogger()
    if root_logger.handlers:
        return  # Already configured

    root_logger.setLevel(level)

    fmt = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)-30s | %(funcName)-25s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # ── Console handler ──────────────────────────────────────────────────────
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(fmt)
    root_logger.addHandler(console_handler)

    # ── Rotating file handler ────────────────────────────────────────────────
    log_dir = pathlib.Path(__file__).parent.parent / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / "upsc_bot.log"

    try:
        file_handler = logging.handlers.RotatingFileHandler(
            log_path,
            maxBytes=5 * 1024 * 1024,  # 5 MB
            backupCount=3,
            encoding="utf-8",
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(fmt)
        root_logger.addHandler(file_handler)
    except (OSError, PermissionError) as exc:
        root_logger.warning("Could not create log file at %s: %s", log_path, exc)

    # Suppress noisy third-party loggers
    for noisy in ("httpx", "httpcore", "urllib3", "telegram.ext._updater"):
        logging.getLogger(noisy).setLevel(logging.WARNING)

    root_logger.info("✅ Logging initialised | level=%s | file=%s", logging.getLevelName(level), log_path)
