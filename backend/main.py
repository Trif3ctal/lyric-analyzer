# will use POST, which creates a new resource
# takes request, returns response
# basic api stuff

import os
import tempfile
import spacy
import pronouncing
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
            nouns = [token.text.lower()
                     for token in doc if token.pos_ == "NOUN"]
            verbs = [token.text.lower()
                     for token in doc if token.pos_ == "VERB"]
            last_word = content.split()[-1]
            rhymes_list = pronouncing.rhymes(last_word)
            if not rhymes_list:
                rhymes_list = "No rhymes found."
            else:
                rhymes_list = ", ".join(rhymes_list)

        # delete the temporary file after reading its content
        os.remove(temp_file.name)

        return jsonify({
            "filename": filename,
            "content": content,
            "wordCount": word_count,
            "lineCount": line_count,
            "nouns": ", ".join(nouns),
            "verbs": ", ".join(verbs),
            "rhymes_last": rhymes_list,
        }), 200

    except Exception as e:
        return jsonify({"message": f"An error occurred while uploading the file: {str(e)}"}), 500


@app.route('/user-submit', methods=['POST'])
def analyze_text():
    data = request.get_json()
    content = data.get('content', '')
    try:
        nlp = spacy.load("en_core_web_sm")
        word_count = len(content.split())
        line_count = len(content.splitlines())
        no_space = content.replace('\n', ' ')
        spacy_content = no_space.replace('\r', ' ')
        doc = nlp(spacy_content)
        nouns = [token.text.lower() for token in doc if token.pos_ == "NOUN"]
        verbs = [token.text.lower() for token in doc if token.pos_ == "VERB"]
        if not nouns:
            nouns = "No nouns found."
        if not verbs:
            verbs = "No verbs found."
        last_word = content.split()[-1]
        rhymes_list = pronouncing.rhymes(last_word)
        if not rhymes_list:
            rhymes_list = "No rhymes found."
        else:
            rhymes_list = ", ".join(rhymes_list)


        return jsonify({
            "filename": None,
            "content": content,
            "wordCount": word_count,
            "lineCount": line_count,
            "nouns": ", ".join(nouns),
            "verbs": ", ".join(verbs),
            "rhymes_last": rhymes_list,
        }), 200

    except Exception as e:
        return jsonify({"message": f"An error occurred while analyzing the file: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True)
