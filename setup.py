from setuptools import setup, find_packages
import os
import sys

def detect_environment():
    if 'google.colab' in sys.modules:
        return 'colab'
    elif 'ipykernel' in sys.modules and 'JPY_PARENT_PID' in os.environ:
        return 'jupyter'
    else:
        return 'normal'

env = detect_environment()
print(f"Se ha detectado este entorno: {env}")

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

extra_dependencies = []
if env == 'normal':
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
