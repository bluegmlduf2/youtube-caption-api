from pytube import YouTube
import re


def get_caption_from_youtube():
    url = "http://youtube.com/watch?v=KM4Xe6Dlp0Y"  # Youtube URL
    targetLanguage = "ko"  # 번역어
    languageLength = 10  # 번역할 최소 문자길이

    try:
        yt = YouTube(url)
        yt.bypass_age_gate()  # caption bugfix ref:https://github.com/pytube/pytube/issues/1674

        if yt and yt.captions:
            captions = yt.captions
            if not captions["en"]:
                print("english cpation does not exist")
                return

            englishCaptions = captions["en"].json_captions["events"]
            captionList = []

            for englishCaption in englishCaptions:
                for seg in englishCaption["segs"]:
                    text = re.sub(r"[^\w\s]", "", seg["utf8"])  # 특문제거
                    text = text.replace("\n", " ").replace("\\", "")  # 역슬래시 제거
                    if len(text) > languageLength: # 10글자이상되는 문장만 포함
                        captionList.append(text)

            print(1)
    except Exception as err:
        print(err)
