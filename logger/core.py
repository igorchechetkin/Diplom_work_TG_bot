import logging
from typing import Callable


def logged(func: Callable) -> Callable:

        logging.basicConfig(level=logging.DEBUG, filename="..\logger.log", filemode="a",
                                      format="%(asctime)s %(levelname)s %(message)s", encoding="utf-8")

        return func


if __name__ == "__main__":

    logged()
