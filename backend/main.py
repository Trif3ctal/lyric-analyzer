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


def get_last_words_rhymes(content):
    lines = [line for line in content.splitlines() if line.strip()]
    last_words = []
    for line in lines:
        words = line.strip().split()
        if words:
            last_word = words[-1]
            last_words.append(last_word)
    rhyme_pairs = []
    for i in range(len(last_words) - 1):
        for j in range(i + 1, len(last_words)):
            if last_words[j] in pronouncing.rhymes(last_words[i]):
                rhyme_pairs.append((last_words[i], last_words[j]))
    return rhyme_pairs


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
            if not nouns:
                nouns = "No nouns found."
            if not verbs:
                verbs = "No verbs found."

            # Get last words and their rhymes
            last_words_rhymes = get_last_words_rhymes(content)
            if not last_words_rhymes:
                rhymes_list = "No rhymes found."
            else:
                rhymes_list = ", ".join(
                    [f"{pair[0]}: {pair[1]}" for pair in last_words_rhymes])

            def grade_rhymes():
                rhyme_score = 0
                if word_count > 500:
                    rhyme_score += 1
                if line_count > 30:
                    rhyme_score += 1

                if rhyme_score == 0:
                    rhyme_score = "D+"
                elif rhyme_score == 1:
                    rhyme_score = "B"
                elif rhyme_score == 2:
                    rhyme_score = "A"
                return rhyme_score

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
            "rhyme_score": grade_rhymes(),
            "rhyme_pairs": rhymes_list.replace(", ", "\n"),
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

        def grade_rhymes():
            rhyme_score = 0
            if word_count > 500:
                rhyme_score += 1
            if line_count > 30:
                rhyme_score += 1

            if rhyme_score == 0:
                rhyme_score = "D+"
            elif rhyme_score == 1:
                rhyme_score = "B"
            elif rhyme_score == 2:
                rhyme_score = "A"
            return rhyme_score

        return jsonify({
            "filename": None,
            "content": content,
            "wordCount": word_count,
            "lineCount": line_count,
            "nouns": ", ".join(nouns),
            "verbs": ", ".join(verbs),
            "rhymes_last": rhymes_list,
            "rhyme_score": grade_rhymes(),
        }), 200

    except Exception as e:
        return jsonify({"message": f"An error occurred while analyzing the file: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True)
