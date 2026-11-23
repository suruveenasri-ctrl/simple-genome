"""Parse a GenBank file with Biopython and generate the data used by the website.
Usage: python build_site.py [data/demo.gb]
Output: docs/data.js  (loaded by docs/index.html)
"""
import sys, json
from Bio import SeqIO
from Bio.SeqUtils import gc_fraction

WINDOW = 500
KEEP = {"CDS", "tRNA", "rRNA", "ncRNA", "tmRNA", "misc_RNA"}

path = sys.argv[1] if len(sys.argv) > 1 else "data/demo.gb"
rec = SeqIO.read(path, "genbank")
seq = rec.seq
L = len(seq)

features = []
for f in rec.features:
    if f.type not in KEEP:
        continue
    q = f.qualifiers
    get = lambda k: q.get(k, [""])[0]
    name = get("gene") or get("locus_tag") or f.type
    tr = get("translation")
    features.append({
        "type": f.type,
        "start": int(f.location.start),
        "end": int(f.location.end),
        "strand": f.location.strand or 1,
        "name": name,
        "locus_tag": get("locus_tag"),
        "product": get("product") or "unknown",
        "translation": tr,
        "aa": len(tr),
    })
features.sort(key=lambda x: x["start"])

gc_windows = [{"s": i, "w": min(WINDOW, L - i), "v": round(gc_fraction(seq[i:i + WINDOW]), 4)}
              for i in range(0, L, WINDOW)]

data = {
    "id": rec.id,
    "description": rec.description,
    "length": L,
    "gc": round(gc_fraction(seq) * 100, 2),
    "n_features": len(features),
    "features": features,
    "gc_windows": gc_windows,
    "sequence": str(seq),
}
with open("docs/data.js", "w") as fh:
    fh.write("const GENOME = " + json.dumps(data) + ";")

print(f"{rec.id}: {L} bp, GC {data['gc']}%, {len(features)} features -> docs/data.js")
