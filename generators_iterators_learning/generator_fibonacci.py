import time
from typing import Generator

from utils.common import get_basic_logger

logger = get_basic_logger(__name__)


def generator_fibonacci() -> Generator[int, None, None]:
    """
        Infinite generator that yields elements of the Fibonacci sequence.

        The Fibonacci sequence is defined as a sequence of numbers
        where each number is the sum of the two preceding ones,
        starting from 0 and 1.

        Returns:
            int: The next number in the Fibonacci sequence.
    """

    current_element = 0
    next_element = 1
    while True:
        yield current_element
        element_sum = current_element + next_element
        current_element = next_element
        next_element = element_sum


def main():
    element = generator_fibonacci()
    try:
        count_element = 0
        while True:
            logger.info(f'element #{count_element}: Fibonacci {next(element)}')
            count_element += 1
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nbreak generator")


if __name__ == '__main__':
    main()
