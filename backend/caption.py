from pytube import YouTube
from flask import abort
from pytube.exceptions import PytubeError
from pytube.innertube import _default_clients
from pytube import exceptions
import traceback
import logging
import re
import datetime
import io


def get_info_from_youtube(targetUrl):
    """유튜브로부터 상세정보 취득"""
    try:
        _default_clients["ANDROID_MUSIC"] = _default_clients[
            "ANDROID_EMBED"
        ]  # 연령제한 버그때문에 사용기기설정 변경
        yt = YouTube("https://www.youtube.com/watch?v=" + targetUrl)

        if yt:
            return {
                "title": yt.title,
                "thumbnailUrl": yt.thumbnail_url,
                "duration": str(datetime.timedelta(seconds=yt.length)),
                "desc": yt.description,
            }
        else:
            abort(400, description="There are no subtitles for this YouTube video")
    except exceptions.AgeRestrictedError:
        abort(400, description="Video is age restricted")
    except PytubeError:
        logging.getLogger().error(traceback.format_exc())
        abort(400, description="The YouTube video cannot be translated")


def get_audio_from_youtube(targetUrl):
    """유튜브로부터 오디오 취득"""
    try:
        _default_clients["ANDROID_MUSIC"] = _default_clients[
            "ANDROID_EMBED"
        ]  # 연령제한 버그때문에 사용기기설정 변경
        yt = YouTube("https://www.youtube.com/watch?v=" + targetUrl)

        if yt:
            # 메모리에 오디오 데이터를 저장
            buffer = io.BytesIO()
            selectedAudioStream = yt.streams.filter(only_audio=True).first()
            selectedAudioStream.stream_to_buffer(buffer)
            buffer.seek(0)

            # TODO 파일크기가 10mb이상일때(로컬스토리지 초과할때)삭제
            # 메모리에서 직접 읽어서 응답으로 반환
            return (
                buffer,
                selectedAudioStream.mime_type,
                selectedAudioStream.default_filename,
            )
        else:
            abort(400, description="There are no subtitles for this YouTube video")
    except exceptions.AgeRestrictedError:
        abort(400, description="Video is age restricted")
    except PytubeError:
        # RegexMatchError 수정
        # /python3.9/site-packages/pytube/cipher.py
        # - var_regex = re.compile(r"^\w+\W")
        # + var_regex = re.compile(r"^\$*\w+\W")
        logging.getLogger().error(traceback.format_exc())
        abort(400, description="The YouTube video cannot be translated")


def get_caption_from_youtube(targetUrl, languageLength=0):
    """유튜브로부터 자막리스트를 취득
    :param int languageLength: 번역할 최소 문자길이
    """
    try:
        _default_clients["ANDROID_MUSIC"] = _default_clients[
            "ANDROID_EMBED"
        ]  # 연령제한 버그때문에 사용기기설정 변경
        yt = YouTube("https://www.youtube.com/watch?v=" + targetUrl)

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
                    cleaned_text = re.sub(r"[^\w\s']|\\|\n", "", combined_text)
                    # 길이가 languageLength 이상인 경우에만 결과 리스트에 추가
                    if len(cleaned_text) > languageLength:
                        captionList.append(cleaned_text)
            return captionList
        else:
            abort(400, description="There are no subtitles for this YouTube video")
    except exceptions.AgeRestrictedError:
        abort(400, description="Video is age restricted")
    except PytubeError:
        logging.getLogger().error(traceback.format_exc())
        abort(400, description="The YouTube video cannot be translated")
