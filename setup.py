from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent

with open(this_directory / "requirements.txt", 'r', encoding='utf-8') as f:
    requirements = [line.strip() for line in f.readlines() if line.strip()]

setup(
    name = "datasonar",
    version = "1.0",
    author = "Neyzu",
    packages = find_packages(),
    install_requires = requirements,    
    long_description = (this_directory / "README.md").read_text("utf-8"),
    long_description_content_type = 'text/markdown',
    url = "https://github.com/Neyzv/DataSonar"
)