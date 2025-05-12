# will use POST, which creates a new resource
# takes request, returns response
# basic api stuff

import os
import tempfile
import spacy
from flask import request, jsonify
from werkzeug.utils import secure_filename
from config import app

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'instance', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"message": "No file part in the request."}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "No file selected for uploading."}), 400

    try:
        with tempfile.NamedTemporaryFile(delete=False, dir=UPLOAD_FOLDER) as temp_file:
            nlp = spacy.load("en_core_web_sm")
            
            file.save(temp_file.name)
            filename = secure_filename(file.filename)
            temp_file.seek(0)
            content = temp_file.read().decode('utf-8')
            word_count = len(content.split())
            line_count = len(content.splitlines())
            no_space = content.replace('\n', ' ')
            spacy_content = no_space.replace('\r', ' ')
            doc = nlp(spacy_content)
            print([chunk.text for chunk in doc.noun_chunks])
            nouns = len([chunk.text for chunk in doc.noun_chunks])

        # delete the temporary file after reading its content
        os.remove(temp_file.name)

        return jsonify({"filename": filename, "content": content, "wordCount": word_count, "lineCount": line_count, "nouns": nouns}), 200

    except Exception as e:
        return jsonify({"message": f"An error occurred while uploading the file: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)