#
#
#
import sys
import signal

from src.opthread import OperationThread
from src.simple_logger import log, LogLevel


def main() -> int:

    operation = OperationThread()

    # シグナルハンドラに処理終了メソッドを設定
    signal.signal(signal.SIGINT, lambda signum, frame: operation.terminate())

    # 処理開始
    log(LogLevel.INFO, "処理を開始し、終了を待機します")
    operation.start()
    operation.join()
    return 0


if __name__ == "__main__":
    sys.exit(main())
