import os
from django.conf import settings
ENTRIES_DIR = settings.BASE_DIR / "entries"
def list_entries():
    if not ENTRIES_DIR.exists():
        return []
    return sorted(os.path.splitext(f)[0] for f in os.listdir(ENTRIES_DIR) if f.lower().endswith(".md"))
def save_entry(title, content):
    ENTRIES_DIR.mkdir(parents=True, exist_ok=True)
    with open(ENTRIES_DIR / f"{title}.md", "w", encoding="utf-8") as f:
        f.write(content)
def get_entry(title):
    if not title or title in {".", ".."} or "/" in title or "\\" in title:
        return None
    path = ENTRIES_DIR / f"{title}.md"
    if not path.is_file():
        return None
    with open(path, encoding="utf-8") as f:
        return f.read()
