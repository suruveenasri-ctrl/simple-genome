"""Download a real genome from NCBI with Biopython's Entrez.
Usage: python fetch_genome.py [ACCESSION] [YOUR_EMAIL]
Default: NC_001416.1 (Escherichia phage lambda, ~48 kb)
"""
import sys
from Bio import Entrez

acc = sys.argv[1] if len(sys.argv) > 1 else "NC_001416.1"
Entrez.email = sys.argv[2] if len(sys.argv) > 2 else "student@example.com"
with Entrez.efetch(db="nucleotide", id=acc, rettype="gb", retmode="text") as h:
    text = h.read()
out = f"data/{acc}.gb"
open(out, "w").write(text)
print("Saved", out)
