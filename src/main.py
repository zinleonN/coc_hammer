from core.common.file import resource_path
from core.common.log import setup_logging, get_logger
from core.process.initial import t

setup_logging()

logger = get_logger()

logger.info("this is a info message")
logger.debug("this is a debug message")

t()