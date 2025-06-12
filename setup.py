#!/usr/bin/env python3
"""
Setup script para Audio Splitter Suite
"""

from setuptools import setup, find_packages
from pathlib import Path

# Leer README
readme_path = Path(__file__).parent / "docs" / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

# Leer requirements
requirements_path = Path(__file__).parent / "requirements.txt"
with open(requirements_path, 'r', encoding='utf-8') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="audio-splitter-suite",
    version="2.0.0",
    author="Audio Splitter Team",
    author_email="contact@audiosplitter.dev",
    description="Sistema completo de procesamiento de audio: división, conversión y edición de metadatos",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/Audio-Splitter",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Sound/Audio :: Conversion",
        "Topic :: Multimedia :: Sound/Audio :: Editors",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
        ],
        "docs": [
            "sphinx>=5.0.0",
            "sphinx-rtd-theme>=1.0.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "audio-splitter=audio_splitter.ui.cli:main_cli",
            "audio-splitter-gui=audio_splitter.ui.interactive:interactive_menu",
        ]
    },
    include_package_data=True,
    zip_safe=False,
    keywords="audio, splitter, converter, metadata, mp3, wav, flac",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/Audio-Splitter/issues",
        "Source": "https://github.com/yourusername/Audio-Splitter",
        "Documentation": "https://github.com/yourusername/Audio-Splitter/docs",
    }
)
