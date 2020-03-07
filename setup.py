import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='keycumber',
    version="0.0.2",
    author="Louis Guitton",
    author_email="admin@guitton.co",
    description="A CLI tool to combine SEO keywords",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/louisguitton/keycumber",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'pandas>=1.0.1',
        'click>=7.0',
        'click-completion'
    ],
    entry_points='''
        [console_scripts]
        keycumber=keycumber:cli
    ''',
)
