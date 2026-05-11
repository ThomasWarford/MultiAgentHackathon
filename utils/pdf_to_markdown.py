import pymupdf4llm
from pathlib import Path

dirs = [
    "10papers_csanyi",
    "10papers_pellegrini",
]

for d in Path('papers').iterdir():
    for pdf in sorted(d.glob("*.pdf")):
        md_path = pdf.with_suffix(".md")
        print(f"Converting {pdf.name} ...", flush=True)
        if md_path.exists():
            print(f'{md_path.name} alreayd exists.')
        else:
            md = pymupdf4llm.to_markdown(str(pdf))
            md_path.write_text(md, encoding="utf-8")
            print(f"  -> {md_path.name} ({len(md):,} chars)", flush=True)
