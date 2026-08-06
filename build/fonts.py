import re, base64, subprocess, sys, pathlib, collections

css = pathlib.Path("gf.css").read_text(encoding="utf-8")

# Collect the basic-latin @font-face block for each family/weight.
rows = []
for b in re.findall(r"@font-face\s*\{(.*?)\}", css, re.S):
    if "U+0000-00FF" not in b:          # keep only the basic-latin subset
        continue
    fam = re.search(r"font-family: '([^']+)'", b).group(1)
    wgt = re.search(r"font-weight: ([^;]+);", b).group(1).strip()
    url = re.search(r"url\((https://[^)]+\.woff2)\)", b).group(1)
    rows.append((fam, wgt, url))

# Google serves ONE variable file for several declared weights. Group by URL so
# each payload is embedded exactly once.
by_url = collections.OrderedDict()
for fam, wgt, url in rows:
    by_url.setdefault(url, {"fam": fam, "weights": []})["weights"].append(wgt)

# Real variable ranges (Google's CSS only ever names the weights we asked for).
VAR_RANGE = {"IBM Plex Sans": "100 700"}

out, total = [], 0
for url, meta in by_url.items():
    fam, weights = meta["fam"], meta["weights"]
    name = fam.replace(" ", "") + "-" + "_".join(weights) + ".woff2"
    subprocess.run(["curl", "-s", "-m", "40", "-A", "Mozilla/5.0 Chrome/120.0",
                    url, "-o", name], check=True)
    raw = pathlib.Path(name).read_bytes()
    if raw[:4] != b"wOF2":
        sys.exit("not a woff2: " + name)
    total += len(raw)

    if len(weights) > 1:                       # one file, many weights => variable
        decl = VAR_RANGE.get(fam) or f"{min(weights)} {max(weights)}"
        kind = f"VARIABLE {decl}"
    else:
        decl, kind = weights[0], "static"
    print(f"{fam:15} {kind:18} {len(raw):>7,} bytes")

    out.append(
        "@font-face{font-family:'%s';font-style:normal;font-weight:%s;"
        "font-display:swap;src:url(data:font/woff2;base64,%s) format('woff2')}"
        % (fam, decl, base64.b64encode(raw).decode())
    )

pathlib.Path("fonts.css").write_text("\n".join(out), encoding="utf-8")
print(f"\n{len(out)} faces embedded")
print(f"raw total   {total:,} bytes")
print(f"css inlined {len(pathlib.Path('fonts.css').read_text(encoding='utf-8')):,} bytes")
