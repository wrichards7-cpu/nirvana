import logging
import logging.config
import os
import yaml

from pathlib import Path

from app.factory import create_app
from app.config import Settings


logger = logging.getLogger(__name__)


def setup_logging() -> None:
    if os.getenv('LOGGING_CONFIG_FILE'):
        logging_file = Path(os.getenv('LOGGING_CONFIG_FILE'))
    else:
        logging_file = Path(__file__).resolve().parent / \
            "app/resources/config/logging.yaml"
    if not logging_file.is_file():
        logger.error(
            f'unable to find logging config file, {logging_file.as_posix()}')
    else:
        with logging_file.open() as logging_config_file:
            logging_config = yaml.safe_load(logging_config_file.read())
            if logging_config:
                logging.config.dictConfig(logging_config)


setup_logging()


app = create_app(Settings())


def main():
    import uvicorn
    port = int(os.getenv('SVC_PORT', 5007))
    uvicorn.run('main:app', host="0.0.0.0", port=port, reload=True)

if __name__ == '__main__':
    main()
