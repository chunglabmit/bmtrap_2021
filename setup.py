from setuptools import setup, find_packages

version = "0.1.0"

with open("./README.md") as fd:
    long_description = fd.read()

setup(
    name="bmtrap",
    version=version,
    description=
    "Co-positive cell registration of two volumes with antibody markers",
    long_description=long_description,
    install_requires=[
        "matplotlib",
        "scipy",
        "scikit-image",
        "zarr",
        "numpy",
        "tqdm",
        "scikit-learn",
        "pandas",
        "tifffile",
        "phathom"
    ],
    author="Chung Lab @ MIT",
    packages=["bmtrap",
              ],
    entry_points={'console_scripts': [
        'bmtrap=bmtrap.main:main'
    ]},
    url="https://github.com/chunglabmit/bmtrap_2021",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        'Programming Language :: Python :: 3.7',
    ]
)
