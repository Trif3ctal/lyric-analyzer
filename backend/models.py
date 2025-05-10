from config import db

class Lyrics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(100), unique=False, nullable=False)
    content = db.Column(db.Text, unique=False, nullable=False)
    # add more fields later for rhyme score, syllables, etc.

    def to_json(self):
        return {
            "id": self.id,
            "fileName": self.file_name,
            "content": self.content,
            # add more fields later for rhyme score, syllables, etc.
        }