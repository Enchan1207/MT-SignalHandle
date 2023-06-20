#
# 標準出力にいい感じの出力を持たせるロガー(ChatGPT製)
#

import logging
from enum import Enum


class LogLevel(Enum):
    """ログレベル
    """
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


# ロガー初期設定
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)


def log(level: LogLevel, message: str):
    """レベルと内容を指定してロガーに出力

    Args:
        level (LogLevel): メッセージのレベル
        message (str): 記録するメッセージ
    """
    logging.log(level.value, message)
