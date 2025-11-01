"""
Setup configuration for APT Toolkit
"""

from pathlib import Path

from setuptools import setup, find_packages

BASE_DIR = Path(__file__).parent
README = (BASE_DIR / "README.md").read_text(encoding="utf-8")

setup(
    name="apt-toolkit",
    version="3.3.1",
    description="Advanced Persistent Threat offensive toolkit for authorized penetration testing",
    author="Security Research Team",
    long_description=README,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "rich>=13.7,<14",
    ],
    entry_points={
        'console_scripts': [
            'apt=apt_toolkit.cli_root:main',
            'apt-analyzer=apt_toolkit.cli:main',
            'apt-offensive=apt_toolkit.cli_enhanced:main_enhanced',
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Security",
        "Topic :: Education",
    ],
)
