import argparse
from typing import List

import numpy as np
from utils.common import display_images, get_basic_logger

logger = get_basic_logger(__name__)


class WhiteNoiseIterator:
    """
        An iterator class that generates white noise images of a specified size.

        Attributes:
        -----------
        width : int
            The width of the generated noise image.
        height : int
            The height of the generated noise image.

        Methods:
        --------
        __iter__():
            Returns the iterator object itself.

        __next__():
            Generates and returns the next white noise image.
    """
    def __init__(self, picture_size: List[int]):
        self.width, self.height = picture_size

    def __iter__(self):
        return self

    def __next__(self):
        noise = np.random.randint(
            0, 256, (self.height, self.width), dtype=np.uint8
        )
        return noise


def main():
    parser = argparse.ArgumentParser('White noise generator')
    parser.add_argument(
        '--picture_size', type=str, default='100x100',
        help='Size of picture for white noise. Format WIDTHxHEIGHT'
    )
    args = parser.parse_args()

    white_noise_generator(args.picture_size)


def white_noise_generator(picture_size: str) -> None:
    """
        Check the input size and start white noise generation

        Args:
            picture_size: Size of picture with white noise.
    """

    picture_sizes = picture_size.split('x')
    assert len(picture_sizes) == 2, (
        f"Enter two args. Your args: {picture_sizes}")
    for size in picture_sizes:
        assert size.isdigit(), (
            f'Size {size} is not a valid integer'
        )
    target_sizes = [int(size) for size in picture_sizes]

    noise_generator = iter(WhiteNoiseIterator(target_sizes))
    display_images(noise_generator, 'White Noise')


if __name__ == '__main__':
    main()
