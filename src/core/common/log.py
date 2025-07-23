import logging
import os
import inspect
from pathlib import Path

detailed = Path(os.getcwd()) / "detailed.log"
brief = Path(os.getcwd()) / "brief.log"

_is_logging_initialized = False

def setup_logging():
    global _is_logging_initialized
    if _is_logging_initialized:
        return
    _is_logging_initialized = True

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)-25s - %(levelname)-6s - %(message)s')

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    detailed_handler = logging.FileHandler(detailed, mode='w', encoding='utf-8')
    detailed_handler.setLevel(logging.DEBUG)
    detailed_handler.setFormatter(formatter)
    logger.addHandler(detailed_handler)

    brief_handler = logging.FileHandler(brief, mode='w', encoding='utf-8')
    brief_handler.setLevel(logging.INFO)
    brief_handler.setFormatter(formatter)
    logger.addHandler(brief_handler)

def get_logger():
    frame = inspect.stack()[1]
    module = inspect.getmodule(frame[0])
    module_name = module.__name__ if module else "unknown"
    return logging.getLogger(module_name)