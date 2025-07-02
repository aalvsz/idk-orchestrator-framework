from setuptools import setup, find_packages

# leer requirements.txt
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="idksim",
    version="0.1.0",
    description="Orquestador de ROM, DOE, OPT y FEM",
    author="Ander Alvarez Sanz",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        *requirements,
        "idkfem @ git+https://kodea.danobatgroup.com/dip/precision/ideko/simulation/idkFEM.git@test-package",
        "idkrom @ git+https://kodea.danobatgroup.com/dip/precision/ideko/simulation/idkROM.git@test-package",
        "idkdoe @ git+https://kodea.danobatgroup.com/dip/precision/ideko/simulation/idkdoe.git@test-package",
        "idkopt @ git+https://kodea.danobatgroup.com/dip/precision/ideko/simulation/idkopt.git@test-package",
    ],
    python_requires=">=3.11",
)
