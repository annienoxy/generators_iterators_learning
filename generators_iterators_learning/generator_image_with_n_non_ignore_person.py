import argparse
from pathlib import Path
from typing import Dict, Generator, Tuple
from xml.etree.ElementTree import Element, fromstring

import cv2
import numpy as np
from utils.common import display_images, get_basic_logger
from utils.meta import ObjectLabel, PersonAttr

logger = get_basic_logger(__name__)


def main():
    parser = argparse.ArgumentParser('Generator image with N non ignore person')
    parser.add_argument(
        'dataset_path', type=Path,
        help='Path to Common Dataset'
    )
    parser.add_argument(
        'primary_count', type=int,
        help='Primary count of person on image'
    )

    args = parser.parse_args()

    assert isinstance(args.primary_count, int), f'Not int {args.primary_count}'
    assert args.dataset_path.is_dir(), f'Not dir {args.dataset_path}'

    n_person_generator = generator_image_with_n_non_ignore_person(
        args.primary_count,
        args.dataset_path
    )
    display_images(n_person_generator, 'generator N non ignore person')


def generator_image_with_n_non_ignore_person(
    primary_count: int,
    dataset_path: Path
) -> Generator[np.ndarray, None, None]:
    """
        This function iterates through the dataset directory and yields images
        that contain the specified number of non-ignored "person" labels.

        Args:
            primary_count: Number of non-ignored person labels in the image.
            dataset_path: Path to the dataset directory.

        Returns:
            np.ndarray: image with desired number of non-ignored person.
    """
    for location in dataset_path.iterdir():
        annotation, image_folder = _get_ann_img(location)
        images_element = _get_image_name_info_map(annotation)
        for image_name, element in images_element.items():
            count_non_person = count_non_ignore_person(element)
            if count_non_person == primary_count:
                image_with_n_non_person = cv2.imread(
                    str(image_folder / image_name)
                )
                yield image_with_n_non_person


def count_non_ignore_person(element) -> int:
    """
        This function counts the number of non-ignored person in an element.

        Args:
            element: An XML element representing an image annotation.

        Returns:
            int: The number of non-ignored person labels.
    """
    filter_person = f'.//box[@label="{ObjectLabel.PERSON}"]'
    count_non_person = 0
    for person in element.findall(filter_person):
        if _is_ignore(person):
            continue
        else:
            count_non_person += 1
    return count_non_person


def _get_ann_img(location: Path) -> Tuple[Element, Path]:
    """
        This function extracts the annotation XML and image folder.

        Args:
            location: Path to a subdirectory within the dataset directory.

        Returns:
            A tuple containing the annotation XML element and the image folder.
    """
    annotation, image_folder = None, None
    for file in location.iterdir():
        if file.is_dir() and file.name == 'images':
            image_folder = file
        elif file.suffix == '.xml':
            annotation = read_xml(file)
    if annotation is not None and image_folder is not None:
        return annotation, image_folder
    else:
        raise FileNotFoundError(
            f'Invalid files structure: annotation {annotation}, '
            f'image_folder {image_folder}')


def read_xml(path_to_xml: Path) -> Element:
    """
       Reads an XML file and parses it into an ElementTree Element.

       Args:
           path_to_xml: The path to the XML file to be read.

       Returns:
           Element: The root element of the parsed XML document.
    """
    with open(path_to_xml, 'r') as file:
        xml_file = file.read()
    tree = fromstring(xml_file)
    return tree


def _get_image_name_info_map(tree: Element) -> Dict[str, Element]:
    """
        This function searches the XML tree for 'image' elements and creates
        a dictionary where the keys are the values of the 'name' attribute
        of each 'image' element, and the values are the corresponding
        XML elements.

        Args:
            tree: The root element of the XML document.

        Returns:
            A dictionary mapping image names (str) to their XML elements.
    """

    images_elements = {}
    for image in tree.findall('.//image'):
        images_elements[image.get('name')] = image
    return images_elements


def _is_ignore(person: Element) -> bool:
    """
        Checks if the given XML element has an 'ignore' attribute
        with the value 'true'.

        Args:
            person: The XML element to check.

        Returns:
            bool: True if the element has an attribute 'name' with the value
            'ignore' and the attribute's text is 'true', else False.
    """
    for attr in person:
        if attr.get('name') == PersonAttr.IGNORE and attr.text == 'true':
            return True
    return False


if __name__ == '__main__':
    main()
