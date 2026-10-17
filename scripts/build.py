#!/usr/bin/env python3
"""读取 README.md 里的表情包登记表，生成 prompt.md。

用法：python3 scripts/build.py
「文件」一列写仓库内路径（如 zoggy/aini.jpg）会自动转成 jsDelivr 外链；
写完整的 http(s) 链接（图床图片）则原样使用。
仓库里还没有图片文件的行会跳过并给出提示。
"""
from pathlib import Path
from urllib.parse import quote

REPO = "d5cwf9rk4t-sys/meme-library"
BRANCH = "main"
CDN = f"https://cdn.jsdelivr.net/gh/{REPO}@{BRANCH}/"

root = Path(__file__).resolve().parent.parent

stickers = []
for line in (root / "README.md").read_text(encoding="utf-8").splitlines():
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    if len(cells) != 4 or cells[0] == "文件" or set(cells[0]) <= set("-: "):
        continue
    file, name, _, usage = cells
    if file.startswith(("http://", "https://")):
        url = file
    elif (root / file).is_file():
        url = CDN + quote(file)
    else:
        print(f"跳过「{name}」：仓库里没有 {file}")
        continue
    stickers.append((name, usage, url))

names = [s[0] for s in stickers]
dupes = sorted({n for n in names if names.count(n) > 1})
if dupes:
    raise SystemExit(f"表情包重名，请改名：{', '.join(dupes)}")

lines = [
    "<表情包>",
    "你可以在回复中适当插入表情包来表达情绪，每条回复最多一个，不要每条都用。",
    "格式：![名字](链接)，只能使用下面列表中的表情包，链接必须原样照抄。",
    "",
]
lines += [f"- {name}（{usage}）：{url}" for name, usage, url in stickers]
lines.append("</表情包>")
(root / "prompt.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

print(f"已生成 {len(stickers)} 个表情包 → prompt.md")
