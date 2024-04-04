import logging
import os
from datetime import datetime
import pytz


def setup_logging():
    """로그 초기화"""

    # 로그 디렉터리 설정
    log_directory = "./log"
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    # 한국 시간대 설정 (UTC+9)
    KST = pytz.timezone("Asia/Seoul")

    # 현재 시간을 한국 시간으로 설정
    now_kst = datetime.now(KST)

    # 로그 파일 이름 설정: 'YYYY-MM-DD.log'
    log_filename = now_kst.strftime("%Y-%m-%d") + ".log"
    log_file_path = os.path.join(log_directory, log_filename)

    # 로그 설정
    logging.basicConfig(
        filename=log_file_path,
        format="%(asctime)s %(levelname)s:%(message)s",
        level=logging.ERROR,
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # 로거에 시간대 설정을 추가합니다. 이는 로그 메시지에 시간대 정보(KST)를 포함시키기 위함입니다.
    logging.Formatter.converter = lambda *args: datetime.now(tz=KST).timetuple()
