from ui.app import MyApp
from core.process.initial import initial
from core.common.log import setup_logging, get_logger

import core.gui.custom_gui as gui

setup_logging()
logger = get_logger()

def main():
    app = MyApp()
    logger.info("程序开始运行")
    app.run()

def text():
    initial()

if __name__ == "__main__":
    # main()
    text()