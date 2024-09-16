# Generators Iterators Learning

Repo for learning generators and iterators

# Getting Started

**1. Install poetry**
   
   https://python-poetry.org/docs/#installing-with-the-official-installer

**2. Go to repo root**

`cd /path/to/person_reid_pre_labeling`

**3. Install deps**

`poetry install`

**4. Run virtual environment**

`poetry shell`

# Task 1. Generator fibonacci

The program is a generator of Fibonacci numbers. Inputs nothing and prints Fibonacci Element #X = Y on a separate line at 1 second intervals.

`python generators_iterators_learning/generator_fibonacci.py`

## Args

### *None*

# Task 2. White noise generator

White noise generator program. It takes as input the size of the picture, for example 100x100, and infinitely generates pictures with white noise of this size, shows in the window open cv, space - next picture, esc - finish. Implemented as an iterator

`python generators_iterators_learning/white_noise_generator.py 100x100`

## Args

### *picture_size* [str]

Size of picture with white noise. Format WIDTHxHEIGHT. Default='100x100'

# Task 3. Generator images with N non ignore persons

The program takes as input an integer N and the path to common datasets. Filters dataset pictures with N not ignored persons in the image. Shows in window open cv, space - next picture, esc - finish. Implemented on the generator

`python generators_iterators_learning/generator_image_with_n_non_ignore_person.py path/to/common/datset primary_count`

## Args

### *dataset_path* [Path]

Path to Common Dataset

### *primary_count* [int]

Number of non ignore persons on the image

# Task 4. Generator images with night

The program takes as input the path to the dataset lpr train (supervisely). Filters night pictures of the dataset. Shows in window open cv, space - next picture, esc - finish. Implemented on the iterator

`python generators_iterators_learning/generator_image_with_night.py path/to/lpr/datset`

## Args

### *dataset_path* [Path]

Path to LPR Train (supervisuly)
