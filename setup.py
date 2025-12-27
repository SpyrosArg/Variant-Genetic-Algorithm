"""Setup script for Variant package."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="variant",
    version="1.0.0",
    author="Spyros Argyrakos",
    author_email="spyros.argyrakos@outlook.com",
    description="Genetic algorithm library for AI security testing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SpyrosArg/Variant-Genetic-Algorithm",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Security",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.10",
    install_requires=[
        "deap>=1.4.0",
        "openai>=1.0.0",
        "anthropic>=0.18.0",
        "numpy>=1.20.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "mypy>=0.950",
            "flake8>=5.0.0",
        ],
    },
)
