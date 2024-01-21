import uuid
from caption import get_caption_from_youtube
from transalatorGoogle import get_translated_text
from tokenizer import get_tokenized_words
import random

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
    # TODO youtubeURL넘기도록 변경
    targetLanguage = request.args.get("language", "ko")
    targetRange = request.args.get("range", None)  # 1 to 10

    captionList = get_caption_from_youtube()

    if targetRange is not None:
        extractionRange = int(len(captionList) * int(targetRange) / 10)
        captionList = random.sample(captionList, extractionRange)

    # 해당 텍스트에서 핵심이 되는 단어리스트 추출기능
    tokenizedWords = get_tokenized_words(captionList)

    translatedText = get_translated_text(captionList, targetLanguage)
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
