from pytube import YouTube
from flask import abort
import re


def get_caption_from_youtube(targetUrl):
    languageLength = 10  # 번역할 최소 문자길이

    try:
        yt = YouTube("https://www.youtube.com/watch?v=" + targetUrl)
        yt.bypass_age_gate()  # caption bugfix ref:https://github.com/pytube/pytube/issues/1674

        if yt and yt.captions:
            captions = yt.captions
            # english cpation does not exist
            if not captions["en"]:
                abort(400, description="English cpation are not available")

            englishCaptions = captions["en"].json_captions["events"]
            captionList = []

            for englishCaption in englishCaptions:
                for seg in englishCaption["segs"]:
                    text = re.sub(r"[^\w\s]", "", seg["utf8"])  # 특문제거
                    text = text.replace("\n", " ").replace("\\", "")  # 역슬래시 제거
                    if len(text) > languageLength:  # 10글자이상되는 문장만 포함
                        captionList.append(text)
            return captionList
        else:
            return None
    except Exception as err:
        print(err) # TODO 로그처리
        raise err
