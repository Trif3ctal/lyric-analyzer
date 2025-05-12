from config import db

class Lyrics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(100), unique=False, nullable=False)
    content = db.Column(db.Text, unique=False, nullable=False)
    word_count = db.Column(db.Integer, unique=False, nullable=False)
    line_count = db.Column(db.Integer, unique=False, nullable=False)
    # add more fields later for rhyme score, syllables, etc.

    def to_json(self):
        return {
            "id": self.id,
            "fileName": self.file_name,
            "content": self.content,
            "word_count": self.word_count,
            "line_count": self.line_count,
            # add more fields later for rhyme score, syllables, etc.
        }