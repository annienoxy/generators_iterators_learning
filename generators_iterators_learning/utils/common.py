import logging
from pathlib import Path

import cv2


def ensure_dir(path: Path):
    if path.is_file():
        raise FileExistsError
    if not path.is_dir():
        path.mkdir(parents=True, exist_ok=True)


def set_basic_logging(level=logging.INFO, **kwargs):
    params = dict(
        filename=None,
        level=level,
        datefmt='%H:%M:%S',
        format='%(asctime)s / %(levelname)s / %(message)s'
    )
    params.update(kwargs)
    logging.basicConfig(**params)


def get_basic_logger(name, level=logging.INFO):
    set_basic_logging(level=level)
    logger = logging.getLogger(name)
    return logger


def display_images(generator, winname):
    for image in generator:
        cv2.imshow(winname, image)
        key = cv2.waitKey(0)
        if key == 27:
            break
        elif key == ord(' '):
            continue
    cv2.destroyAllWindows()
