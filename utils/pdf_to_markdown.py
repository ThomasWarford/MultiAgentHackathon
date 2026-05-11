import argparse
import pymupdf4llm
from pathlib import Path
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import os
import time

ARXIV_API_URL = "http://export.arxiv.org/api/query"
ARXIV_NS = "{http://www.w3.org/2005/Atom}"


def fetch_papers_by_author(author_name, max_results=10):
    query = f'au:"{author_name}"'
    params = urllib.parse.urlencode({
        "search_query": query,
        "start": 0,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    })
    url = f"{ARXIV_API_URL}?{params}"

    with urllib.request.urlopen(url) as response:
        xml_content = response.read()

    root = ET.fromstring(xml_content)
    entries = root.findall(f"{ARXIV_NS}entry")

    papers = []
    for entry in entries:
        arxiv_id = entry.find(f"{ARXIV_NS}id").text.split("/abs/")[-1]
        title = entry.find(f"{ARXIV_NS}title").text.strip().replace("\n", " ")
        pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
        papers.append({"id": arxiv_id, "title": title, "pdf_url": pdf_url})

    return papers


def download_paper(paper, output_dir):
    safe_title = "".join(c if c.isalnum() or c in " .-_()" else "_" for c in paper["title"])
    filename = f"{paper['id'].replace('/', '_')}_{safe_title[:60]}.pdf"
    filepath = os.path.join(output_dir, filename)

    if os.path.exists(filepath):
        print(f"  Already exists, skipping: {filename}")
        return

    print(f"  Downloading: {paper['title'][:70]}...")
    urllib.request.urlretrieve(paper["pdf_url"], filepath)
    print(f"  Saved to: {filename}")


def download_papers_by_author(author_name, max_results=50):
    output_dir = os.path.join("papers", author_name)
    os.makedirs(output_dir, exist_ok=True)
    print(f"Fetching papers by '{author_name}'...")

    papers = fetch_papers_by_author(author_name, max_results)
    print(f"Found {len(papers)} papers.\n")

    for i, paper in enumerate(papers, start=1):
        print(f"[{i}/{len(papers)}] {paper['id']}")
        download_paper(paper, output_dir)
        time.sleep(1)  # be polite to the API

    print(f"\nDone. Papers saved to: {os.path.abspath(output_dir)}")


def process_authors(author_names: list[str], max_results: int = 20) -> None:
    for author_name in author_names:
        download_papers_by_author(author_name=author_name, max_results=max_results)

        author_dir = Path("papers") / author_name
        for pdf in sorted(author_dir.glob("*.pdf")):
            md_path = pdf.with_suffix(".md")
            print(f"Converting {pdf.name} ...", flush=True)
            if md_path.exists():
                print(f"  {md_path.name} already exists.")
            else:
                md = pymupdf4llm.to_markdown(str(pdf))
                md_path.write_text(md, encoding="utf-8")
                print(f"  -> {md_path.name} ({len(md):,} chars)", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Download arXiv papers and convert to Markdown for a list of authors."
    )
    parser.add_argument(
        "authors",
        nargs="+",
        help='Author name(s), e.g. "Yoshua Bengio" "Geoffrey Hinton"',
    )
    parser.add_argument(
        "--max-results",
        type=int,
        default=20,
        help="Maximum papers to fetch per author (default: 20)",
    )
    args = parser.parse_args()
    process_authors(args.authors, max_results=args.max_results)




