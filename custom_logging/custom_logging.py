import structlog
import logging
from pathlib import Path
from datetime import datetime
import inspect


class CustomLogging:
    def generate_session_file_id(self):
        format = datetime.now().strftime("%Y-%b-%d-%H")
        frame = inspect.stack()[1]
        filename = Path(frame.filename).name
        return f"session_{format}_{filename}.log"

    def __init__(self, logs_dir: str = "logs"):
        log_base = Path(logs_dir)
        log_base.mkdir(parents=True, exist_ok=True)

        self.session_file = log_base / self.generate_session_file_id()

    def custom_logger(self):

        std_logger = logging.getLogger()

        if std_logger.hasHandlers():
            return structlog.get_logger()

        std_logger.setLevel(level=logging.INFO)

        file_handler = logging.FileHandler(filename=str(self.session_file))
        console_handler = logging.StreamHandler()

        std_logger.addHandler(file_handler)
        std_logger.addHandler(console_handler)

        structlog.configure(
            processors=[
                structlog.stdlib.filter_by_level,
                structlog.processors.TimeStamper(fmt="iso", utc=True, key="timestamp"),
                structlog.stdlib.add_log_level,
                structlog.processors.dict_tracebacks,
                structlog.processors.EventRenamer(to="msg"),
                structlog.processors.JSONRenderer(indent=4),
            ],
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
        )

        return structlog.get_logger()
