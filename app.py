from flask import Flask, request, jsonify
from flask_cors import CORS
from markitdown import MarkItDown
import tempfile
import os

app = Flask(__name__)
CORS(app)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50 MB

IMAGE_EXTS = {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp', '.tiff', '.tif', '.heic', '.heif'}

# EXIF tag IDs we care about (subset of PIL.ExifTags.TAGS)
_EXIF_LABELS = {
    271:   'Camera Make',
    272:   'Camera Model',
    306:   'Date/Time',
    270:   'Description',
    315:   'Artist',
    33432: 'Copyright',
    36867: 'Date Taken',
    40962: 'Image Width',
    40963: 'Image Height',
}


def _image_to_markdown(path, filename):
    from PIL import Image

    img = Image.open(path)
    w, h = img.size
    fmt = img.format or os.path.splitext(filename)[1].lstrip('.').upper()

    lines = [
        f"# {filename}",
        "",
        "| Property | Value |",
        "| --- | --- |",
        f"| Format | {fmt} |",
        f"| Dimensions | {w} × {h} px |",
        f"| Color mode | {img.mode} |",
    ]

    try:
        exif = img.getexif()
        rows = []
        for tag_id, label in _EXIF_LABELS.items():
            val = exif.get(tag_id)
            if val:
                rows.append(f"| {label} | {str(val)[:120]} |")
        if rows:
            lines += ["", "## EXIF Metadata", "| Property | Value |", "| --- | --- |"] + rows
    except Exception:
        pass

    return '\n'.join(lines)


@app.route('/api/convert', methods=['POST'])
def convert_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    temp_path = None
    try:
        ext = os.path.splitext(file.filename)[1].lower()
        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
            file.save(tmp.name)
            temp_path = tmp.name

        if ext in IMAGE_EXTS:
            markdown = _image_to_markdown(temp_path, file.filename)
        else:
            md = MarkItDown()
            result = md.convert(temp_path)
            markdown = result.text_content

        return jsonify({"markdown": markdown})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


@app.route('/api/convert-text', methods=['POST'])
def convert_text():
    data = request.get_json()
    if not data or 'content' not in data:
        return jsonify({"error": "No content provided"}), 400

    content = data['content']
    temp_path = None
    try:
        ext = '.html' if content.strip().startswith('<') else '.txt'
        with tempfile.NamedTemporaryFile(delete=False, suffix=ext, mode='w', encoding='utf-8') as tmp:
            tmp.write(content)
            temp_path = tmp.name

        md = MarkItDown()
        result = md.convert(temp_path)
        return jsonify({"markdown": result.text_content})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


if __name__ == '__main__':
    app.run(debug=True)
