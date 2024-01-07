import uuid
from caption import get_caption_from_youtube
from transalator import get_translated_text

from flask import Flask, jsonify, request
from flask_cors import CORS


BOOKS = [
    {
        "id": uuid.uuid4().hex,
        "title": "On the Road",
        "author": "Jack Kerouac",
        "read": True,
    },
    {
        "id": uuid.uuid4().hex,
        "title": "Harry Potter and the Philosopher's Stone",
        "author": "J. K. Rowling",
        "read": False,
    },
    {
        "id": uuid.uuid4().hex,
        "title": "Green Eggs and Ham",
        "author": "Dr. Seuss",
        "read": True,
    },
]

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r"/*": {"origins": "*"}})


def remove_book(book_id):
    for book in BOOKS:
        if book["id"] == book_id:
            BOOKS.remove(book)
            return True
    return False


# sanity check route
@app.route("/ping", methods=["GET"])
def ping_pong():
    return jsonify("pong!")


@app.route("/caption", methods=["GET"])
def get_caption():
    targetLanguage = request.args.get("language", "ko")

    captionList = get_caption_from_youtube()
    captionText = "/".join([captionList[0], captionList[1], captionList[2]])
    translatedText = get_translated_text(captionText, targetLanguage)
    translatedTextList = translatedText.split("/")
    result = [{"en": en, "ko": ko} for en, ko in zip(captionList, translatedTextList)]
    return jsonify({"captionList": result, "hi": "123"})


@app.route("/books", methods=["GET", "POST"])
def all_books():
    response_object = {"status": "success"}
    if request.method == "POST":
        post_data = request.get_json()
        BOOKS.append(
            {
                "id": uuid.uuid4().hex,
                "title": post_data.get("title"),
                "author": post_data.get("author"),
                "read": post_data.get("read"),
            }
        )
        response_object["message"] = "Book added!"
    else:
        response_object["books"] = BOOKS
    return jsonify(response_object)


@app.route("/books/<book_id>", methods=["PUT", "DELETE"])
def single_book(book_id):
    response_object = {"status": "success"}
    if request.method == "PUT":
        post_data = request.get_json()
        remove_book(book_id)
        BOOKS.append(
            {
                "id": uuid.uuid4().hex,
                "title": post_data.get("title"),
                "author": post_data.get("author"),
                "read": post_data.get("read"),
            }
        )
        response_object["message"] = "Book updated!"
    if request.method == "DELETE":
        remove_book(book_id)
        response_object["message"] = "Book removed!"
    return jsonify(response_object)


if __name__ == "__main__":
    app.run()
