#!/usr/bin/env python3
"""答案之书: a tiny Book of Answers server. Standard library only.

Routes:
  GET /               the web page
  GET /api/answer     one random answer, {"question", "answer", "category", "total"}
  GET /api/answers    the full answer list
  GET /api/health     {"status": "ok"}
"""
import json
import os
import random
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

BASE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE, "answers.json"), encoding="utf-8") as fh:
    ANSWERS = json.load(fh)

with open(os.path.join(BASE, "index.html"), encoding="utf-8") as fh:
    INDEX = fh.read().encode("utf-8")


class Handler(BaseHTTPRequestHandler):
    def _send(self, body, ctype, status=200):
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _json(self, obj, status=200):
        self._send(json.dumps(obj, ensure_ascii=False).encode("utf-8"),
                   "application/json; charset=utf-8", status)

    def do_GET(self):  # noqa: N802 - http.server naming
        url = urlparse(self.path)
        if url.path == "/":
            self._send(INDEX, "text/html; charset=utf-8")
        elif url.path == "/api/answer":
            question = parse_qs(url.query).get("q", [""])[0]
            picked = random.choice(ANSWERS)
            self._json({"question": question, "answer": picked["text"],
                        "category": picked["category"], "total": len(ANSWERS)})
        elif url.path == "/api/answers":
            self._json({"total": len(ANSWERS), "answers": ANSWERS})
        elif url.path == "/api/health":
            self._json({"status": "ok"})
        else:
            self._json({"error": "not found"}, 404)

    def log_message(self, *args):  # noqa: N802 - keep the log quiet
        pass


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    ThreadingHTTPServer(("0.0.0.0", port), Handler).serve_forever()
