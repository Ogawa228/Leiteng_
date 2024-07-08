import datetime
import logging

import portalocker


class ConcurrentTimedRotatingFileHandler(logging.Handler):

    def __init__(self, filename: str, terminator="\n", lockfile: str = None, *args, **kwargs):
        logging.Handler.__init__(self, *args, **kwargs)

        self.log_file_stream = None
        self.lock_file_stream = None

        self.filename = filename
        self.terminator = terminator
        if isinstance(lockfile, str):
            self.lock_file_name = lockfile
        else:
            self.lock_file_name = "concurrent.lock"

    def do_write(self, record: logging.LogRecord):
        self.log_file_stream = open(
            self.filename + "-" + datetime.datetime.fromtimestamp(record.created).strftime("%Y-%m-%d") + ".txt", "a",
            encoding="utf8")
        try:
            self.log_file_stream.write(self.format(record) + self.terminator)
        finally:
            self.log_file_stream.close()
            self.log_file_stream = None

    def emit(self, record: logging.LogRecord) -> None:
        try:
            self.request_lock()

            self.do_write(record)
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception:
            self.handleError(record)
        finally:
            self.release_lock()

    def request_lock(self):
        if self.lock_file_stream is None:
            self.lock_file_stream = open(self.lock_file_name, "w")
        portalocker.lock(self.lock_file_stream, portalocker.LOCK_EX)

    def release_lock(self):
        if self.lock_file_stream is not None:
            portalocker.unlock(self.lock_file_stream)
            self.lock_file_stream.close()
            self.lock_file_stream = None
