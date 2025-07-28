from ui.app import MyApp
from core.common.log import setup_logging, get_logger

logger = get_logger()

def main():
    setup_logging()
    app = MyApp()
    logger.info("程序开始运行")
    app.run()


if __name__ == "__main__":
    main()