"""Small browser UI for running researcher matchmaking.

The server deliberately uses only the Python standard library so the web UI
does not add another dependency stack to the hackathon project.
"""

from __future__ import annotations

import asyncio
import html
import traceback
import uuid
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs


def _available_researchers() -> list[str]:
    papers_dir = _papers_dir()
    if not papers_dir.exists():
        return []
    return sorted(path.name for path in papers_dir.iterdir() if path.is_dir())


def _papers_dir() -> Path:
    try:
        from matchmaker.config import load_settings

        return load_settings().papers_dir
    except ModuleNotFoundError:
        return Path("papers")


def _outputs_dir() -> Path:
    from matchmaker.config import load_settings

    return load_settings().outputs_dir


def _overview_dir() -> Path:
    return Path("researcher_overview")


def _read_overview_file(researcher: str, filename: str) -> str:
    path = _overview_dir() / researcher / filename
    if not path.exists():
        return "_No local overview file found._"
    return path.read_text(encoding="utf-8").strip()


def _render_local_overview_match(researcher_a: str, researcher_b: str) -> str:
    sections = [
        ("Summary", "summary.md"),
        ("Methods", "methods.md"),
        ("Open questions", "open_questions.md"),
        ("Significance", "significance.md"),
    ]
    parts = [
        f"# Local match brief: {researcher_a} x {researcher_b}",
        "",
        "_Rendered from the local researcher_overview files. Install the project environment and run the full pipeline for generated collaboration hypotheses._",
    ]
    for title, filename in sections:
        parts.extend(
            [
                "",
                f"## {title}",
                "",
                f"### {researcher_a}",
                _read_overview_file(researcher_a, filename),
                "",
                f"### {researcher_b}",
                _read_overview_file(researcher_b, filename),
            ]
        )
    return "\n".join(parts)


def _page(*, result: str = "", error: str = "", researcher_a: str = "", researcher_b: str = "") -> bytes:
    researchers = _available_researchers()
    researcher_options = "".join(
        f'<option value="{html.escape(name)}">{html.escape(name)}</option>' for name in researchers
    )
    result_block = ""
    if result:
        result_block = f"""
        <section class="output love-note" aria-live="polite">
          <div class="section-label">Match report</div>
          <pre>{html.escape(result)}</pre>
        </section>
        """
    elif error:
        result_block = f"""
        <section class="output error" aria-live="polite">
          <div class="section-label">Something needs attention</div>
          <pre>{html.escape(error)}</pre>
        </section>
        """
    else:
        result_block = """
        <section class="output empty" aria-live="polite">
          <div class="section-label">Output</div>
          <p>Your collaboration report will appear here after the run finishes.</p>
        </section>
        """

    body = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Research Matchmaker</title>
  <style>
    :root {{
      color-scheme: light;
      --ink: #26151d;
      --muted: #715c65;
      --line: #ead4db;
      --paper: #fffafb;
      --rose: #c9285c;
      --rose-dark: #8f1640;
      --gold: #b88721;
      --mint: #dff2ea;
      --shadow: 0 18px 55px rgba(143, 22, 64, 0.14);
    }}

    * {{ box-sizing: border-box; }}

    body {{
      margin: 0;
      min-height: 100vh;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      color: var(--ink);
      background:
        radial-gradient(circle at 20% 18%, rgba(255, 192, 203, 0.42), transparent 30%),
        radial-gradient(circle at 86% 8%, rgba(223, 242, 234, 0.9), transparent 26%),
        linear-gradient(135deg, #fff7f8 0%, #fffafb 48%, #f8fff9 100%);
    }}

    main {{
      width: min(1120px, calc(100% - 32px));
      margin: 0 auto;
      padding: 34px 0 44px;
    }}

    .hero {{
      display: grid;
      grid-template-columns: minmax(0, 0.9fr) minmax(320px, 1.1fr);
      gap: 26px;
      align-items: end;
      margin-bottom: 24px;
    }}

    h1 {{
      margin: 0 0 10px;
      font-size: clamp(2.2rem, 5vw, 4.7rem);
      line-height: 0.95;
      letter-spacing: 0;
      color: var(--rose-dark);
    }}

    .subcopy {{
      margin: 0;
      max-width: 58ch;
      color: var(--muted);
      font-size: 1.02rem;
      line-height: 1.6;
    }}

    .heart {{
      display: inline-grid;
      place-items: center;
      width: 42px;
      height: 42px;
      border-radius: 50%;
      background: var(--rose);
      color: white;
      font-size: 1.35rem;
      box-shadow: 0 12px 30px rgba(201, 40, 92, 0.24);
    }}

    .panel, .output {{
      background: rgba(255, 250, 251, 0.9);
      border: 1px solid var(--line);
      border-radius: 8px;
      box-shadow: var(--shadow);
    }}

    .panel {{
      padding: 22px;
    }}

    form {{
      display: grid;
      grid-template-columns: 1fr 1fr auto;
      gap: 14px;
      align-items: end;
    }}

    label {{
      display: grid;
      gap: 8px;
      color: var(--rose-dark);
      font-weight: 750;
      font-size: 0.92rem;
    }}

    input {{
      width: 100%;
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 13px 14px;
      font: inherit;
      color: var(--ink);
      background: white;
      outline: none;
    }}

    input:focus {{
      border-color: var(--rose);
      box-shadow: 0 0 0 4px rgba(201, 40, 92, 0.12);
    }}

    button {{
      border: 0;
      border-radius: 8px;
      padding: 14px 18px;
      min-height: 50px;
      font: inherit;
      font-weight: 800;
      color: white;
      background: linear-gradient(135deg, var(--rose), var(--rose-dark));
      cursor: pointer;
      box-shadow: 0 10px 24px rgba(143, 22, 64, 0.2);
      white-space: nowrap;
    }}

    button:hover {{ filter: brightness(1.04); }}

    .hint {{
      margin: 14px 0 0;
      color: var(--muted);
      font-size: 0.9rem;
      line-height: 1.45;
    }}

    .chips {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-top: 14px;
    }}

    .chip {{
      border: 1px solid var(--line);
      border-radius: 999px;
      padding: 6px 10px;
      color: var(--rose-dark);
      background: #fff;
      font-size: 0.84rem;
    }}

    .output {{
      margin-top: 22px;
      overflow: hidden;
    }}

    .section-label {{
      padding: 13px 18px;
      border-bottom: 1px solid var(--line);
      color: var(--rose-dark);
      background: linear-gradient(90deg, rgba(255, 228, 235, 0.88), rgba(223, 242, 234, 0.7));
      font-weight: 850;
    }}

    pre {{
      margin: 0;
      padding: 20px;
      max-height: 68vh;
      overflow: auto;
      white-space: pre-wrap;
      word-wrap: break-word;
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace;
      font-size: 0.92rem;
      line-height: 1.55;
      background: rgba(255, 255, 255, 0.72);
    }}

    .empty p {{
      margin: 0;
      padding: 22px;
      color: var(--muted);
    }}

    .error {{
      border-color: #ef9a9a;
    }}

    datalist {{ display: none; }}

    @media (max-width: 820px) {{
      main {{ width: min(100% - 22px, 680px); padding-top: 22px; }}
      .hero {{ grid-template-columns: 1fr; gap: 18px; }}
      form {{ grid-template-columns: 1fr; }}
      button {{ width: 100%; }}
    }}
  </style>
</head>
<body>
  <main>
    <section class="hero">
      <div>
        <div class="heart" aria-hidden="true">♥</div>
        <h1>Research Matchmaker</h1>
        <p class="subcopy">Pair two researchers and let the programme look for the intellectual chemistry: shared methods, open questions, stakes, and collaboration hypotheses.</p>
      </div>
      <div class="panel">
        <form method="post" action="/run">
          <label>
            Researcher one
            <input name="researcher_a" list="researchers" value="{html.escape(researcher_a)}" placeholder="csanyi" required>
          </label>
          <label>
            Researcher two
            <input name="researcher_b" list="researchers" value="{html.escape(researcher_b)}" placeholder="pellegrini" required>
          </label>
          <button type="submit">Make match</button>
          <datalist id="researchers">{researcher_options}</datalist>
        </form>
        <p class="hint">Use the researcher slugs that match folders in <code>papers/</code> and files in <code>prompts_input/</code>.</p>
        <div class="chips">{"".join(f'<span class="chip">{html.escape(name)}</span>' for name in researchers)}</div>
      </div>
    </section>
    {result_block}
  </main>
</body>
</html>"""
    return body.encode("utf-8")


class MatchmakerWebHandler(BaseHTTPRequestHandler):
    server_version = "MatchmakerWeb/0.1"

    def do_GET(self) -> None:  # noqa: N802 - http.server API
        if self.path not in {"/", "/index.html"}:
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        self._send_html(_page())

    def do_HEAD(self) -> None:  # noqa: N802 - http.server API
        if self.path not in {"/", "/index.html"}:
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()

    def do_POST(self) -> None:  # noqa: N802 - http.server API
        if self.path != "/run":
            self.send_error(HTTPStatus.NOT_FOUND)
            return

        length = int(self.headers.get("Content-Length", "0"))
        raw_body = self.rfile.read(length).decode("utf-8")
        form = parse_qs(raw_body)
        researcher_a = self._field(form, "researcher_a")
        researcher_b = self._field(form, "researcher_b")

        if not researcher_a or not researcher_b:
            self._send_html(_page(error="Please enter both researcher names.", researcher_a=researcher_a, researcher_b=researcher_b))
            return

        run_id = f"web_{uuid.uuid4().hex[:8]}"
        try:
            from matchmaker.runner import run_match_async

            report_path = asyncio.run(
                run_match_async(
                    researcher_a=researcher_a,
                    researcher_b=researcher_b,
                    prompts_dir=None,
                    backend=None,
                    papers_dir=None,
                    outputs_dir=None,
                    run_id=run_id,
                )
            )
            report = report_path.read_text(encoding="utf-8")
            self._send_html(_page(result=report, researcher_a=researcher_a, researcher_b=researcher_b))
        except ModuleNotFoundError as exc:
            result = _render_local_overview_match(researcher_a, researcher_b)
            result += f"\n\n## Local mode note\n\nFull pipeline dependency missing: `{exc.name}`."
            self._send_html(_page(result=result, researcher_a=researcher_a, researcher_b=researcher_b))
        except Exception as exc:  # pragma: no cover - exercised manually by browser use
            details = f"{exc}\n\n{traceback.format_exc()}"
            self._send_html(_page(error=details, researcher_a=researcher_a, researcher_b=researcher_b), status=HTTPStatus.INTERNAL_SERVER_ERROR)

    @staticmethod
    def _field(form: dict[str, list[str]], name: str) -> str:
        return form.get(name, [""])[0].strip()

    def _send_html(self, body: bytes, status: HTTPStatus = HTTPStatus.OK) -> None:
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: Any) -> None:
        print(f"{self.address_string()} - {format % args}")


def run_web_server(host: str = "127.0.0.1", port: int = 8000) -> None:
    server = ThreadingHTTPServer((host, port), MatchmakerWebHandler)
    print(f"Matchmaker web UI running at http://{host}:{port}")
    print("Press Ctrl+C to stop.")
    server.serve_forever()


__all__ = ["run_web_server", "MatchmakerWebHandler"]


if __name__ == "__main__":
    run_web_server()
