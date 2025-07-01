from setuptools import setup, find_packages

# leer requirements.txt
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="idkSIM",
    version="0.1.0",
    description="Orquestador de ROM, DOE, OPT y FEM",
    author="Ander Alvarez Sanz",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        *requirements,
        #"idkFEM @ git+https://kodea.danobatgroup.com/dip/precision/ideko/simulation/idkFEM.git@Integración-con-idkSIM",
        #"idkROM @ git+https://kodea.danobatgroup.com/dip/precision/ideko/simulation/idkROM.git@main",
        #"idkDOE @ git+https://kodea.danobatgroup.com/dip/precision/ideko/simulation/idkdoe.git@main",
        #"idkOPT @ git+https://kodea.danobatgroup.com/dip/precision/ideko/simulation/idkopt.git@main",
    ],
    python_requires=">=3.11",
)
