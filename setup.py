import os

from setuptools import find_packages, setup

# https://packaging.python.org/single_source_version/
base_dir = os.path.abspath(os.path.dirname(__file__))
about = {}
with open(os.path.join(base_dir, "gitfaces", "__about__.py"), "rb") as f:
    exec(f.read(), about)


setup(
    name="gitfaces",
    version=about["__version__"],
    packages=find_packages(),
    url="https://github.com/nschloe/gitfaces",
    author=about["__author__"],
    author_email=about["__email__"],
    install_requires=["GitPython", "Pillow", "requests"],
    python_requires=">=3.6",
    description="Fetch contributor avatars for a GitHub repository",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license=about["__license__"],
    classifiers=[
        about["__status__"],
        about["__license__"],
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Software Development :: Version Control",
    ],
    entry_points={"console_scripts": ["gitfaces = gitfaces.cli:main"]},
)
