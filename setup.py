from setuptools import setup, find_packages

setup(
    name="my_package",
    version="0.1.0",
    author="Your Name",
    author_email="your_email@example.com",
    description="A Python package for LLM reasoning, summarization, text-to-speech, and more.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/my_package",
    packages=find_packages(),
    install_requires=[
        "requests",
        "transformers",
        "gtts",
        "markitdown",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
