from pathlib import Path

files = [
    "app/templates/admin/mining/index.html",
    "app/templates/admin/marketplace/index.html",
]

replacements = [
    (
        'class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-gray-800 p-4 rounded-xl border border-gray-700"',
        'class="bg-gray-800/80 border border-gray-700/60 backdrop-blur-md rounded-2xl p-5 text-center shadow-xl"',
    ),
    (
        'rounded-lg',
        'rounded-xl',
    ),
]

for f in files:
    p = Path(f)
    if not p.exists():
        print(f"SKIP: {f}")
        continue

    backup = p.with_suffix(p.suffix + ".bak")
    if not backup.exists():
        backup.write_text(p.read_text(encoding="utf-8"), encoding="utf-8")

    txt = p.read_text(encoding="utf-8")

    for old, new in replacements:
        txt = txt.replace(old, new)

    p.write_text(txt, encoding="utf-8")
    print(f"UPDATED: {f}")

print("Done.")
