from flask import Flask, request, jsonify
from flask_cors import CORS
from markitdown import MarkItDown
import tempfile
import os

app = Flask(__name__)
CORS(app)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50 MB


@app.route('/api/convert', methods=['POST'])
def convert_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    temp_path = None
    try:
        ext = os.path.splitext(file.filename)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
            file.save(tmp.name)
            temp_path = tmp.name

        md = MarkItDown()
        result = md.convert(temp_path)
        return jsonify({"markdown": result.text_content})

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
