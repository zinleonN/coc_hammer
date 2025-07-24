from ui.app import MyApp
from core.common.log import setup_logging, get_logger

logger = get_logger()

def main():
    setup_logging()
    app = MyApp()
    app.run()

if __name__ == "__main__":
    logger.info("开始")
    main()