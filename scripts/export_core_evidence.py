"""Export actual NB1-NB4 output to HTML pages for submission screenshots."""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "submission" / "evidence"
ANSI = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    paths = ([ROOT / "notebooks" / name for name in sys.argv[1:]]
             if len(sys.argv) > 1 else sorted((ROOT / "notebooks").glob("0[1-4]*.ipynb")))
    for path in paths:
        notebook = json.loads(path.read_text(encoding="utf-8"))
        cards = []
        heading = path.stem
        for cell in notebook["cells"]:
            source = "".join(cell.get("source", []))
            if cell["cell_type"] == "markdown":
                headings = [line.lstrip("# ") for line in source.splitlines() if line.startswith("#")]
                if headings:
                    heading = headings[-1]
                continue
            if cell.get("execution_count") is None:
                raise RuntimeError(f"Unexecuted cell in {path.name}")
            texts = []
            for output in cell.get("outputs", []):
                if output["output_type"] == "error":
                    raise RuntimeError(f"Notebook error in {path.name}: {output.get('evalue')}")
                if output["output_type"] == "stream" and output.get("name") == "stdout":
                    texts.append("".join(output["text"]))
                elif "text/plain" in output.get("data", {}):
                    texts.append("".join(output["data"]["text/plain"]))
            text = ANSI.sub("", "\n".join(texts)).strip()
            if not text or text == "True":
                continue
            if path.name.startswith("01") and text.startswith("Corpus size:"):
                text = text.splitlines()[0]
            details = ""
            if path.name.startswith("04") and "Registered feature views:" in text:
                log, listing = text.split("Registered feature views:", 1)
                summary = "\n".join(line for line in log.splitlines() if line.startswith((
                    "Applying changes", "Created project", "Created entity", "Created feature view",
                    "Updated feature view", "No changes to infrastructure",
                )))
                text = summary + "\n\nRegistered feature views:" + listing
                details = f"<details><summary>Full feast apply log</summary><pre>{html.escape(log)}</pre></details>"
            cards.append(f"<section><h2>{html.escape(heading)}</h2><pre>{html.escape(text)}</pre>{details}</section>")
        page = f"""<!doctype html><html lang="vi"><meta charset="utf-8">
<title>{html.escape(path.stem)} — evidence</title>
<style>
body{{margin:32px auto;padding:0 28px;max-width:1100px;background:#f4f6fa;color:#172337;font:16px 'Segoe UI',sans-serif}}
h1{{font-size:25px;margin-bottom:8px}} .meta{{color:#526174;margin-bottom:24px}}
section{{background:white;border:1px solid #dce3ed;border-radius:9px;padding:16px 20px;margin:14px 0}}
h2{{font-size:17px;margin:0 0 12px}}pre{{font:14px/1.6 Consolas,'DejaVu Sans Mono',monospace;white-space:pre-wrap;overflow-wrap:anywhere;margin:0}}
details{{margin-top:12px;color:#526174}}summary{{cursor:pointer}}
</style><h1>{html.escape(path.stem)}</h1>
<div class="meta">Lite · Actual executed notebook output · Source: notebooks/{html.escape(path.name)}</div>
{''.join(cards)}</html>"""
        destination = OUT / f"{path.stem}.html"
        destination.write_text(page, encoding="utf-8")
        print(destination.relative_to(ROOT))


if __name__ == "__main__":
    main()
