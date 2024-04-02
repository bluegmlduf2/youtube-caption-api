import uuid
from caption import get_caption_from_youtube
from transalatorGoogle import get_translated_text
from tokenizer import get_tokenized_words
import random
import ast

from flask import Flask, jsonify, request, abort
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
    targetRange = request.args.get("range", 1)  # 1 to 10
    targetUrl = request.args.get("url")  # KM4Xe6Dlp0Y

    if targetUrl is None:
        # TODO 400 에러를 객체로 메세지를 전달
        abort(400, description="Missing 'url' parameter")

    captionList = get_caption_from_youtube(targetUrl)

    extractionRange = int(len(captionList) * int(targetRange) / 10)
    captionList = random.sample(captionList, extractionRange)

    tokenizedWords = get_tokenized_words(captionList)
    translatedText = get_translated_text(tokenizedWords, targetLanguage)

    resultCaptionList = []
    for text in translatedText:
        try:
            origin = text.origin
            target = ast.literal_eval(text.text)
            resultCaptionList.append(
                {
                    "origin": {"sentence": origin["1"], "words": origin["2"]},
                    "target": {"sentence": target["1"], "words": target["2"]},
                }
            )
        # 번역후의 문자열에 예상하지 못한 문자열이 포함되어 실행이 안되는 경우는 무시하고 다음 결과로 이동
        except SyntaxError:
            pass

    return jsonify(
        {
            "captionList": resultCaptionList,
        }
    )


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


@app.errorhandler(404)
def not_found_error(error):
    # TODO 로그추가
    return "404 error..", 404


@app.errorhandler(500)
def internal_error(error):
    # TODO 로그추가
    return "server error..", 500


if __name__ == "__main__":
    app.run()
