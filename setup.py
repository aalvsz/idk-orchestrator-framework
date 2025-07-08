from setuptools import setup, find_packages
import os
import sys

def is_running_in_colab():
    return 'google.colab' in sys.modules

# leer requirements.txt
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

# Dependencias privadas solo si NO estamos en Colab
extra_dependencies = []
if not is_running_in_colab():
    extra_dependencies = [
        "idkrom @ git+https://kodea.danobatgroup.com/dip/precision/ideko/simulation/idkROM.git@test-package",
        "idkdoe @ git+https://kodea.danobatgroup.com/dip/precision/ideko/simulation/idkdoe.git@test-package",
        "idkopt @ git+https://kodea.danobatgroup.com/dip/precision/ideko/simulation/idkopt.git@test-package",
    ]

setup(
    name="idksim",
    version="0.1.0",
    description="Orquestador de ROM, DOE, OPTIMIZACION.",
    author="Ander Alvarez Sanz",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=requirements + extra_dependencies,
    python_requires=">=3.11",
)
