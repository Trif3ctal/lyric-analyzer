# will use POST, which creates a new resource
# takes request, returns response
# basic api stuff

from flask import request, jsonify
from config import app, db
from models import Lyrics

@app.route("/lyrics", methods=["GET"]) # grab the lyrics just uploaded
def get_lyrics():
    lyrics = Lyrics.query.all()
    json_lyrics = list(map(lambda x: x.to_json(), lyrics)) # advanced function, thanks youtube
    return jsonify({"lyrics": json_lyrics}) # return the lyrics as a json object

@app.route("/create", methods=["POST"]) # upload the lyrics
def create_lyrics():
    file_name = request.json.get("fileName")
    content = request.json.get("content")

    if not file_name or not content:
        return (
            jsonify({"message": "You must provide a file name and content."}),
            400,
        )
    
    user_lyrics = Lyrics(file_name=file_name, content=content) # create a new Lyrics object
    try:
        db.session.add(user_lyrics) # add the new Lyrics object to the database
        db.session.commit() # commit the changes to the database
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
    return jsonify({"message": "Lyrics created successfully."}), 201 # return success/created

@app.route("/update_lyrics/<int:user_id>", methods=["PATCH"])
def update_lyrics(user_id):
    lyrics = Lyrics.query.get(user_id) # get user id from the database

    if not lyrics:
        return jsonify({"message": "Lyrics not found."}), 404 # if user id not found, return error
    
    data = request.json
    lyrics.file_name = data.get("fileName", lyrics.file_name) # update file name if changed, otherwise keep the same
    lyrics.content = data.get("content", lyrics.content) # update content if changed, otherwise keep the same

    db.session.commit()

    return jsonify({"message": "Lyrics updated successfully."}), 200 # return success

@app.route("/delete_lyrics/<int:user_id>", methods=["DELETE"])
def delete_lyrics(user__id):
    lyrics = Lyrics.query.get(user__id)

    if not lyrics:
        return jsonify({"message": "User not found."}), 404
    
    db.session.delete(lyrics) # delete the Lyrics object from the database
    db.session.commit()

    return jsonify({"message": "Lyrics deleted successfully."}), 200 # return success

if __name__ == "__main__":
    with app.app_context(): # still not sure what this does lol
        db.create_all() # "spin up" (create) the database
    
    app.run(debug=True)