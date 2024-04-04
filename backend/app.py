import uuid
from caption import get_caption_from_youtube
from transalatorGoogle import get_translated_text
from tokenizer import get_tokenized_words
import random
import ast

from flask import Flask, jsonify, request, abort
from flask_cors import CORS

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r"/*": {"origins": "*"}})


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


@app.errorhandler(400)
def user_custom_error(error):
    return jsonify({"message": error.description}), 400


@app.errorhandler(404)
def not_found_error(error):
    # TODO 로그추가
    app.logger.info("%s failed to log in", user.username)
    return jsonify({"message": "404 Not Page founded"}), 404


@app.errorhandler(500)
def internal_error(error):
    # TODO 로그추가
    return jsonify({"message": "500 Server Internal error"}), 500


if __name__ == "__main__":
    app.run()
