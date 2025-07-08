from setuptools import setup, find_packages

# leer requirements.txt
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="idksim",
    version="0.1.0",
    description="Orquestador de ROM, DOE, OPTIMIZACION.",
    author="Ander Alvarez Sanz",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        *requirements
    ],
    python_requires=">=3.11",
)
