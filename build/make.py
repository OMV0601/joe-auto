"""
Builds the two deliverables from one source.

  build/page.html  ->  index.html      full standalone document (open in a browser)
                   ->  artifact.html   body content only (the artifact host wraps it)

Only needed if you regenerate the fonts. To change Joe's phone number, hours or
service area, just edit the BIZ block near the bottom of index.html directly.

    python build/make.py
"""
import pathlib, sys

HERE = pathlib.Path(__file__).parent
ROOT = HERE.parent

page  = (HERE / "page.html").read_text(encoding="utf-8")
fonts = (HERE / "fonts.css")

if not fonts.exists():
    sys.exit("build/fonts.css missing — run build/fonts.py first")

if "/*@FONTS@*/" not in page:
    sys.exit("build/page.html has no /*@FONTS@*/ marker")

page = page.replace("/*@FONTS@*/", fonts.read_text(encoding="utf-8"), 1)

TITLE = "Joe — Mobile Auto Repair"
DESC  = ("Joe does auto repair at your place — oil changes to engine swaps, "
         "dents to a full respray. No shop; he drives to the car.")

doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{TITLE}</title>
<meta name="description" content="{DESC}">
<meta name="color-scheme" content="dark light">
<meta property="og:title" content="{TITLE}">
<meta property="og:description" content="{DESC}">
<meta property="og:type" content="website">
</head>
<body>
{page}
</body>
</html>
"""

(ROOT / "index.html").write_text(doc, encoding="utf-8")
(ROOT / "artifact.html").write_text(page, encoding="utf-8")

for f in ("index.html", "artifact.html"):
    print(f"{f:16} {(ROOT / f).stat().st_size:>9,} bytes")
