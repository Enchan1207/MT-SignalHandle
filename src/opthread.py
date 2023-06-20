#
#
#
import threading
import time
from src.simple_logger import log, LogLevel


class TerminationRequestInterrupt(Exception):
    """処理の待機中に終了リクエストを受け取った
    """


class OperationThread(threading.Thread):
    """処理を行うスレッド
    """

    def __init__(self) -> None:
        super().__init__()
        self._term_event = threading.Event()

    def run(self) -> None:
        """処理の実体
        """

        try:
            log(LogLevel.INFO, "処理開始")

            log(LogLevel.INFO, "時間のかかる処理 1 (ブロック可能)")
            self._sleep(2)
            log(LogLevel.INFO, "時間のかかる処理 1 終了")

            # I/Oバウンド等を想定
            log(LogLevel.INFO, "時間のかかる処理 2 (ブロック不能)")
            time.sleep(2)
            log(LogLevel.INFO, "時間のかかる処理 2 終了")

            log(LogLevel.INFO, "時間のかかる処理 3 (ブロック可能, 強制待機)")
            self._sleep(2, True)
            log(LogLevel.INFO, "時間のかかる処理 3 終了")

            log(LogLevel.INFO, "処理完了")

        except TerminationRequestInterrupt:
            log(LogLevel.CRITICAL, "処理中断、修了処理…")

    def terminate(self):
        """処理中のスレッドを中断する
        """
        self._term_event.set()

    def _sleep(self, secs: float, force: bool = False):
        """処理内で指定時間待機する

        Args:
            secs (float): 待機時間
            force (bool): 強制的に待機するかどうか

        Raises:
            TerminationRequestInterrupt: 待機中に終了要求を受け取った場合。

        Note:
            force=Trueの場合、それ以前でシグナルが立ち上がっていても強制的に一定時間待機します。
        """

        if force:
            # 待機してから考える
            time.sleep(secs)
            if self._term_event.is_set():
                raise TerminationRequestInterrupt()
        else:
            # threading.Event.waitはタイムアウトになった場合のみFalseが返る
            # この関数では意図的にタイムアウトを引き起こすことで待機を実現している
            if self._term_event.wait(secs):
                raise TerminationRequestInterrupt()
