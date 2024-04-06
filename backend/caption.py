from pytube import YouTube
from flask import abort
import re


def get_caption_from_youtube(targetUrl):
    languageLength = 10  # 번역할 최소 문자길이

    yt = YouTube("https://www.youtube.com/watch?v=" + targetUrl)
    yt.bypass_age_gate()  # caption bugfix ref:https://github.com/pytube/pytube/issues/1674

    if yt and yt.captions:
        captions = yt.captions
        captionEn = captions.get("en") or captions.get("a.en")

        # english cpation does not exist
        if captionEn is None:
            abort(400, description="English cpation are not available")

        englishCaptions = captionEn.json_captions["events"]
        captionList = []

        for englishCaption in englishCaptions:
            if "segs" in englishCaption:
                # 세그먼트의 'utf8' 키를 기반으로 문자열을 합침
                combined_text = "".join(
                    segs["utf8"] for segs in englishCaption["segs"]
                )
                # 특수문자 제거 및 역슬래시 제거
                cleaned_text = re.sub(r"[^\w\s]|\\", "", combined_text)
                # 길이가 languageLength 이상인 경우에만 결과 리스트에 추가
                if len(cleaned_text) > languageLength:
                    captionList.append(cleaned_text)
        return captionList
    else:
        return None

