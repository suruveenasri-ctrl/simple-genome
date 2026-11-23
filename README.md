# Simple Genome Browser

A lightweight genome browser. **Python + Biopython** parse a GenBank file and generate the data;
a static web page (HTML/JS) displays it as an interactive browser and is hosted on **GitHub Pages**.

**Features:** pan/zoom, ruler, gene track (+/− strand arrows), GC-content track, DNA sequence at base level,
gene search, click for protein translation, download gene FASTA.

## Run locally
```bash
pip install -r requirements.txt
python make_demo.py            # creates data/demo.gb (synthetic genome)  -- OR --
python fetch_genome.py NC_001416.1 you@email.com   # real phage lambda genome from NCBI
python build_site.py data/demo.gb                  # or data/NC_001416.1.gb
cd docs && python -m http.server 8000              # open http://localhost:8000
```

## Publish on GitHub
1. Create a repo, push this folder (include `docs/data.js` after running `build_site.py`).
2. Repo → **Settings → Pages → Source: Deploy from a branch → `main` / `/docs`**.
3. Your site appears at `https://<username>.github.io/<repo>/`.

## How it works
| Step | File | Biopython used |
|---|---|---|
| Get data | `fetch_genome.py` | `Bio.Entrez` |
| Parse + analyse | `build_site.py` | `Bio.SeqIO`, `Bio.SeqUtils.gc_fraction` |
| Demo data | `make_demo.py` | `Bio.Seq` (translate, reverse_complement), `SeqFeature` |
| Visualise | `docs/index.html` | – (Canvas + JavaScript) |

Best for small genomes (phages, plasmids, bacteria up to a few Mb).
