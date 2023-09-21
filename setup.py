import pathlib
import pkg_resources
from setuptools import setup

with pathlib.Path("requirements.txt").open() as requirements_txt:
    install_requires = [
        str(requirement)
        for requirement in pkg_resources.parse_requirements(requirements_txt)
    ]

setup(
    name="evalquiz_material_server",
    version="1.0",
    author_email="st170001@stud.uni-stuttgart.de",
    packages=["evalquiz_material_server"],
    install_requires=install_requires,
)
