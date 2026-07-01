"""Final pre-package validation: syntax, imports, app build."""
import sys
import ast
import os

sys.path.insert(0, ".")

# ── 1. Syntax check ──────────────────────────────────────────────────────────
syntax_errors = []
files_checked = 0
for root, dirs, fs in os.walk("."):
    dirs[:] = [d for d in dirs if d not in ("__pycache__", ".git", "venv")]
    for f in fs:
        if f.endswith(".py"):
            fpath = os.path.join(root, f)
            files_checked += 1
            try:
                ast.parse(open(fpath).read())
            except SyntaxError as e:
                syntax_errors.append((fpath, str(e)))

status = "PASS" if not syntax_errors else "FAIL"
print(f"1. Syntax check:  {status}  ({files_checked} files, {len(syntax_errors)} errors)")
for fpath, e in syntax_errors:
    print(f"   ERROR: {fpath}: {e}")

# ── 2. Module imports ─────────────────────────────────────────────────────────
modules = [
    "config", "keyboards", "media",
    "utils.logger", "utils.helpers", "utils.ephemeral",
    "storage.database",
    "services.gemini", "services.plan_loader", "services.backup", "services.notifier",
    "data.plan_reviews", "data.fallbacks",
    "handlers.onboarding", "handlers.home", "handlers.tasks",
    "handlers.revision", "handlers.answer_writing", "handlers.mock_test",
    "handlers.current_affairs", "handlers.essay", "handlers.ethics",
    "handlers.optional", "handlers.progress", "handlers.streak",
    "handlers.doubt", "handlers.timer", "handlers.settings", "handlers.admin",
]
import_errors = []
for m in modules:
    try:
        __import__(m)
    except Exception as e:
        import_errors.append((m, str(e)))

status = "PASS" if not import_errors else "FAIL"
print(f"2. Import check:  {status}  ({len(modules)} modules, {len(import_errors)} errors)")
for m, e in import_errors:
    print(f"   ERROR {m}: {e}")

# ── 3. App build ──────────────────────────────────────────────────────────────
try:
    from utils.logger import setup_logging
    setup_logging()
    import bot as b
    app = b.build_application()
    total = sum(len(v) for v in app.handlers.values())
    groups = len(app.handlers)
    print(f"3. App build:     PASS  ({total} handlers in {groups} groups)")
    build_ok = True
except Exception as e:
    print(f"3. App build:     FAIL  {e}")
    build_ok = False

print()
all_ok = not syntax_errors and not import_errors and build_ok
if all_ok:
    print("✅  ALL CHECKS PASSED — bot is ready to deploy")
else:
    print("❌  SOME CHECKS FAILED — fix above before deploying")
    sys.exit(1)
