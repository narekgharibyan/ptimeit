import setuptools


with open('README.md', 'r') as f_in:
    long_description = f_in.read()

setuptools.setup(
    name='ptimeit',
    version='0.1.2',
    author='Narek Gharibyan',
    author_email='narekgharibyan@gmail.com',
    description='Simple and pretty python code profiler for measuring execution time.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/narekgharibyan/ptimeit',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
