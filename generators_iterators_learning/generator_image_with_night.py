import argparse
import json
from pathlib import Path
from typing import Dict

import cv2
from utils.common import display_images, get_basic_logger

logger = get_basic_logger(__name__)


class NightImageIterator:
    """
        Iterator for retrieving images tagged with 'night' from a dataset.

        This iterator rounds a dataset organized into folders, where each folder
        contains 'img' and 'ann' subdirectories. It yields images from the 'img'
        directory if their corresponding annotation files in the 'ann' directory
        contain a tag indicating 'night'.

        Attributes:
        -----------
        dataset_path : Path
            The root path of the dataset.
        _folders_iter : iter
            An iterator over the folders in the dataset.
        _images_path : Path or None
            The path to the 'img' directory.
        _annotations_paths : iter or None
            An iterator over the annotation files in the 'ann' directory.

        Methods:
        --------
        __iter__():
            Returns the iterator object itself.

        __next__():
            Gets and returns the next image with a 'night' tag.

        read_json(path_to_json: Path) -> Dict:
            Reads a JSON file and returns its content as a dictionary.

        _is_night(json_file: Dict) -> bool:
            Checks if there is a 'night' tag in the annotation.
    """
    def __init__(self, dataset_path: Path):
        self.dataset_path = dataset_path
        self._folders_iter = iter(dataset_path.iterdir())
        self._images_path = None
        self._annotations_paths = None

    def __iter__(self):
        return self

    def __next__(self):
        while True:
            if self._annotations_paths is None:
                current_folder = next(self._folders_iter, None)
                if current_folder is None:
                    raise StopIteration
                self._images_path = current_folder / 'img'
                annotations_path = current_folder / 'ann'
                self._annotations_paths = iter(annotations_path.iterdir())

            for ann in self._annotations_paths:
                json_file = self.read_json(ann)
                if self._is_night(json_file):
                    image_path = self._images_path / ann.stem
                    night_image = cv2.imread(str(image_path))
                    if night_image is not None:
                        return night_image
            self._annotations_paths = None

    @staticmethod
    def read_json(path_to_json: Path) -> Dict:
        with open(path_to_json, 'r', encoding='utf-8') as file:
            json_file = json.load(file)
        return json_file

    @staticmethod
    def _is_night(json_file: Dict) -> bool:
        for tag in json_file.get("tags", []):
            if tag.get("name") == "time" and tag.get("value") == "night":
                return True
        return False


def main():
    parser = argparse.ArgumentParser('Generator image with night')
    parser.add_argument(
        'dataset_path', type=Path,
        help='Path to LPR Train (supervisuly)'
    )
    args = parser.parse_args()

    assert args.dataset_path.is_dir(), f'Not a directory: {args.dataset_path}'

    night_image_generator = NightImageIterator(args.dataset_path)
    display_images(night_image_generator, 'Night generator')


if __name__ == '__main__':
    main()
