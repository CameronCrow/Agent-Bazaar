"""Setup script for the Agent Bazaar package."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="agent-bazaar",
    version="1.0.0",
    author="Seth Karten, Cameron Crow, Chi Jin",
    author_email="sethkarten@princeton.edu",
    description="Agent Bazaar: a multi-agent LLM marketplace simulator for benchmarking economic alignment",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sethkarten/AI-Bazaar",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
    python_requires=">=3.10",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "pytest-cov>=2.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "isort>=5.0.0",
        ],
        "flash-attn": ["flash-attn>=2.0.0"],  # Uncomment if needed for vLLM performance
    },
    entry_points={
        "console_scripts": [
            "agent-bazaar=agent_bazaar.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "agent_bazaar": ["data/*.csv"],
    },
    zip_safe=False,
)