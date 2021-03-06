import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

# with open("requirements.txt", "r") as fh:
#     requirements = fh.read().splitlines()

setuptools.setup(
    name="MESAPC", # Replace with your own username
    version="0.0.1",
    author="Thomas Steindl",
    author_email="thomas.steindl95@gmx.at",
    description="Python package to calculate any grid of models with MESA",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOs, Linux",
    ],
    python_requires='>=3.6',
)
