from caption import (
    get_caption_from_youtube,
    get_info_from_youtube,
    get_audio_from_youtube,
)
from transalatorGoogle import get_translated_text
from tokenizer import get_tokenized_words
from logger import setup_logging
from flask import Flask, jsonify, request, abort, send_file, Response
from flask_cors import CORS
from dotenv import load_dotenv
import traceback
import random
import ast
import os

# 로그 설정
setup_logging()

# load env
load_dotenv()

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS (모든 경로 "/*"에 대해서 cors적용)
CORS(app, resources={r"/*": {"origins": [os.environ.get("FRONT_URL")]}})


@app.route("/caption", methods=["GET"])
def get_caption():
    targetLanguage = request.args.get("language", "ko")
    targetRange = request.args.get("range", 10)  # 1 to 50
    targetUrl = request.args.get("url")  # KM4Xe6Dlp0Y

    if targetLanguage not in ["ko"]:
        abort(400, description="Currently, translation is only available in Korean")

    if 10 < targetRange > 50:
        abort(400, description="The search range cannot exceed 50")

    if targetUrl is None:
        abort(400, description="Missing 'url' parameter")

    captionList = get_caption_from_youtube(targetUrl, 10)
    youtubeInfo = get_info_from_youtube(targetUrl)
    captionList = random.sample(captionList, (targetRange * 2))

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
            "title": youtubeInfo["title"],
            "thumbnailUrl": youtubeInfo["thumbnailUrl"],
            "duration": youtubeInfo["duration"],
            "desc": youtubeInfo["desc"],
            "captionList": resultCaptionList,
        }
    )


@app.route("/download", methods=["GET"])
def get_caption_download():
    targetUrl = request.args.get("url")  # KM4Xe6Dlp0Y

    if targetUrl is None:
        abort(400, description="Missing 'url' parameter")

    captionList = get_caption_from_youtube(targetUrl)
    youtubeInfo = get_info_from_youtube(targetUrl)

    return jsonify(
        {
            "title": youtubeInfo["title"],
            "thumbnailUrl": youtubeInfo["thumbnailUrl"],
            "duration": youtubeInfo["duration"],
            "captionList": captionList,
        }
    )


@app.route("/audio", methods=["GET"])
def get_caption_audio():
    targetUrl = request.args.get("url")  # KM4Xe6Dlp0Y

    if targetUrl is None:
        abort(400, description="Missing 'url' parameter")

    audioData, mineType, fileName = get_audio_from_youtube(targetUrl)

    return send_file(
        audioData,
        as_attachment=True,
        mimetype=mineType,
        download_name=fileName,
    )


@app.errorhandler(400)
def user_custom_error(error):
    return jsonify({"message": error.description}), 400


@app.errorhandler(404)
def not_found_error():
    return jsonify({"message": "404 Not Page founded"}), 404


@app.errorhandler(Exception)
def internal_error(error):
    app.logger.critical(traceback.format_exc())
    return jsonify({"message": "500 Server Internal error"}), 500


if __name__ == "__main__":
    app.run()
