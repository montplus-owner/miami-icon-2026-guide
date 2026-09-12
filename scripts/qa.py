from pathlib import Path
import json, re, sys
from html.parser import HTMLParser

ROOT=Path(__file__).resolve().parents[1]
errors=[]
warnings=[]

required=[
    "index.html","manifest.webmanifest","service-worker.js",
    "version.json","offline.html","icon-192.png","icon-512.png"
]
for name in required:
    if not (ROOT/name).exists():
        errors.append(f"Missing required file: {name}")

def load_json(name):
    try:
        return json.loads((ROOT/name).read_text(encoding="utf-8"))
    except Exception as e:
        errors.append(f"{name} invalid JSON: {e}")
        return {}

manifest=load_json("manifest.webmanifest")
version=load_json("version.json")

if manifest:
    for key in ("name","short_name","start_url","display","icons"):
        if key not in manifest: errors.append(f"manifest missing: {key}")
    if manifest.get("display")!="standalone":
        warnings.append("manifest display is not standalone")

if version and not re.fullmatch(r"\d+\.\d+\.\d+", str(version.get("version",""))):
    errors.append("version.json version must be semver x.y.z")

index=(ROOT/"index.html").read_text(encoding="utf-8") if (ROOT/"index.html").exists() else ""

# Full trip date coverage.
for day in range(9,21):
    date=f"2026-12-{day:02d}"
    if date not in index:
        errors.append(f"Trip day missing from index.html: {date}")

# Decision layers expected in UI.
for token in ("TRYB DZISIAJ","LIVE CENTER","PLAN B","HARD / RETURN","PLAN SIĘ ZMIENIŁ"):
    if token not in index:
        errors.append(f"Required UI layer missing: {token}")


# Critical route invariant: on Sunday from Government Center to Earlington Heights,
# Green Line must be northbound toward Palmetto before transferring to Airport Shuttle.
bad_route = "Government Center → Green Line southbound → Earlington Heights"
good_route = "Government Center → Green Line northbound"
if bad_route in index:
    errors.append("CRITICAL ROUTE ERROR: Dec20 Government Center → Earlington Heights cannot be southbound.")
if good_route not in index or "kierunku Palmetto" not in index:
    errors.append("Dec20 transit backup must state Green Line northbound toward Palmetto to Earlington Heights.")

# No accidental obvious secrets.
secret_patterns={
    "Google API key":r"AIza[0-9A-Za-z\-_]{30,}",
    "GitHub token":r"gh[pousr]_[0-9A-Za-z]{20,}",
    "OpenAI-style key":r"\bsk-[0-9A-Za-z\-_]{20,}",
}
for label,pat in secret_patterns.items():
    if re.search(pat,index):
        errors.append(f"Possible secret found in index.html: {label}")

class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__(); self.ids=set(); self.hrefs=[]
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if "id" in d: self.ids.add(d["id"])
        if tag=="a" and "href" in d: self.hrefs.append(d["href"])

p=LinkParser(); p.feed(index)
for href in p.hrefs:
    if href.startswith("#") and href[1:] and href[1:] not in p.ids:
        # Dynamic day anchors are generated at runtime; allow their template.
        if not href.startswith("#day"):
            errors.append(f"Broken internal anchor: {href}")
    if href.startswith("http://"):
        errors.append(f"Insecure external link: {href}")

sw=(ROOT/"service-worker.js").read_text(encoding="utf-8") if (ROOT/"service-worker.js").exists() else ""
for name in ("index.html","manifest.webmanifest","version.json","offline.html","icon-192.png","icon-512.png"):
    if name not in sw:
        errors.append(f"service-worker core does not mention: {name}")
if "SKIP_WAITING" not in sw:
    errors.append("service-worker missing update activation handler")

print("Miami + Icon guide QA")
print("=====================")
for w in warnings: print("WARN:",w)
for e in errors: print("ERROR:",e)
if errors:
    print(f"\nFAILED: {len(errors)} error(s)")
    sys.exit(1)
print("\nPASS: required files, trip coverage, internal anchors, PWA update hooks and basic secret scan are OK.")
