from flask import Flask, request, jsonify
from flask_cors import CORS
from markitdown import MarkItDown
import tempfile
import os

app = Flask(__name__)
CORS(app)

@app.route('/api/convert', methods=['POST'])
def convert_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        ext = os.path.splitext(file.filename)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as temp_file:
            file.save(temp_file.name)
            temp_path = temp_file.name

        md = MarkItDown()
        result = md.convert(temp_path)
        os.remove(temp_path)

        return jsonify({"markdown": result.text_content})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/convert-text', methods=['POST'])
def convert_text():
    data = request.get_json()
    if not data or 'content' not in data:
        return jsonify({"error": "No content provided"}), 400

    content = data['content']
    try:
        ext = '.html' if content.strip().startswith('<') else '.txt'
        with tempfile.NamedTemporaryFile(delete=False, suffix=ext, mode='w', encoding='utf-8') as temp_file:
            temp_file.write(content)
            temp_path = temp_file.name

        md = MarkItDown()
        result = md.convert(temp_path)
        os.remove(temp_path)

        return jsonify({"markdown": result.text_content})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
