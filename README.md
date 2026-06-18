# MarkItDown Web

A web app that converts files and text to Markdown using [Microsoft's MarkItDown](https://github.com/microsoft/markitdown) library, with a Flask backend deployed on Vercel.

**Live:** https://markitdown-web-rho.vercel.app

## Features

- **File conversion** — upload or drag-and-drop a file to convert it to Markdown
- **Text & HTML paste** — paste raw text or HTML directly into the input box
- **Drag and drop** — drag a file anywhere on the page to attach it
- **Clipboard paste** — Ctrl+V a copied file or image directly
- **Chat-style UI** — results appear as cards; each has Copy and Save .md buttons
- **Ctrl+Enter** shortcut to convert

## Supported formats

PDF · Word (.docx) · Excel (.xlsx) · PowerPoint (.pptx) · Images · HTML · CSV · JSON · plain text

## Stack

- **Frontend** — vanilla HTML + Tailwind CSS
- **Backend** — Python / Flask + MarkItDown
- **Deployment** — Vercel (serverless Python)

## Local development

```bash
pip install -r requirements.txt
python app.py
```

Then open `http://localhost:5000`.

## API

| Method | Endpoint | Body | Description |
|--------|----------|------|-------------|
| POST | `/api/convert` | `multipart/form-data` — `file` | Convert an uploaded file |
| POST | `/api/convert-text` | `application/json` — `{ "content": "..." }` | Convert pasted text or HTML |
