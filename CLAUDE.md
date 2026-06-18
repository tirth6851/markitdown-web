# MarkItDown Web — Project Rules

## Stack
- **Frontend**: Vanilla HTML + Tailwind CSS (CDN) — single file `index.html`
- **Backend**: Python 3.12 / Flask + MarkItDown — `app.py`
- **Deployment**: Vercel serverless Python via `@vercel/python` + `@vercel/static`; configured in `vercel.json` (legacy `builds` + `routes` format)
- **Python version**: pinned to 3.12 via `.python-version`

## API Rules
- All frontend API calls **must** use relative `/api/*` paths — never hardcoded `localhost` or absolute URLs
- Endpoints: `POST /api/convert` (multipart file upload) and `POST /api/convert-text` (JSON `{ "content": "..." }`)

## Supported Formats
Determined by MarkItDown optional extras installed via `requirements.txt`:

| Format | Extra | Key packages |
|--------|-------|-------------|
| PDF | `[pdf]` | `pdfminer-six`, `pdfplumber` |
| Word (.docx) | `[docx]` | `mammoth`, `lxml` |
| PowerPoint (.pptx) | `[pptx]` | `python-pptx` |
| Excel (.xlsx) | `[xlsx]` | `openpyxl`, `pandas` |
| Excel (.xls) | `[xls]` | `pandas`, `xlrd` |
| Images | built-in | metadata/EXIF (no OCR without LLM client) |
| HTML, CSV, JSON, plain text | built-in | — |

**Rule**: if a format extra is removed from `requirements.txt`, also remove it from the UI labels and README.

## Dependency Rule
- Pin `markitdown` to an exact version (e.g. `==0.1.6`) so Vercel builds are reproducible
- Use `markitdown[extras]` extras syntax, not bare package names, so MarkItDown's converters register correctly
- Do **not** add `markitdown[audio-transcription]`, `markitdown[az-doc-intel]`, or `markitdown[az-content-understanding]` — they pull in large/heavy packages that risk exceeding Vercel's 250 MB unzipped function limit

## Backend Rules
- `app.config['MAX_CONTENT_LENGTH']` is set to 50 MB in `app.py`
- Temp files are **always** deleted in a `try/finally` block — never only on the happy path
- No secrets, tokens, or credentials may be committed to this repo

## Privacy / Consent Gate
- A consent modal **must** appear on first load (backed by `localStorage` key `markitdown_consent_v1`)
- The convert button must be `disabled` and `convert()` must refuse to run until consent is granted
- Three required acknowledgments in the modal:
  1. Uploaded files or pasted content may contain sensitive data
  2. The user has the right to upload and process the content
  3. Files are processed on the server and the user accepts responsibility
- On accept: set `localStorage.markitdown_consent_v1 = '1'`, hide modal, enable UI

## Testing Flow
1. After any backend or dependency change, start the app with `python app.py` and confirm it starts cleanly
2. For frontend changes, verify the full golden path in a browser: consent gate → attach/paste → convert → copy/save result
3. **After every push to `main`**, use **Playwright MCP** to validate the deployed app at `https://markitdown-web-rho.vercel.app`:
   - Consent/privacy gate blocks UI until all three boxes are checked and Accept is clicked
   - Text paste → Convert returns non-empty Markdown
   - At least one file format (PDF or DOCX preferred) converts successfully

## Live URL
`https://markitdown-web-rho.vercel.app`
