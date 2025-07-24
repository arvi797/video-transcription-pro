"""
Setup configuration for video-transcription-pro package.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# Read version from __init__.py
import re

def get_version():
    with open("src/video_transcription/__init__.py", "r", encoding='utf-8') as f:
        content = f.read()
        version_match = re.search(r'__version__ = [\'"]([^\'"]*)[\'"]', content)
        author_match = re.search(r'__author__ = [\'"]([^\'"]*)[\'"]', content)
        if version_match and author_match:
            return version_match.group(1), author_match.group(1)
        raise RuntimeError("Unable to find version/author string.")

version, author = get_version()

setup(
    name="video-transcription-pro",
    version=version,
    author=author,
    author_email="support@video-transcription-pro.com",
    description="Professional-grade video transcription with GPU-accelerated Whisper and speaker diarization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/video-transcription-pro",
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/video-transcription-pro/issues",
        "Documentation": "https://video-transcription-pro.readthedocs.io/",
        "Source Code": "https://github.com/yourusername/video-transcription-pro",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
        "Topic :: Multimedia :: Video",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[
        "torch>=1.9.0",
        "openai-whisper>=20231117",
        "librosa>=0.9.0",
        "numpy>=1.21.0",
        "scipy>=1.7.0",
        "soundfile>=0.10.0",
        "tqdm>=4.62.0",
        "ffmpeg-python>=0.2.0",
    ],
    extras_require={
        "gpu": [
            "torch>=1.9.0",
            "torchaudio>=0.9.0",
        ],
        "pyannote": [
            "pyannote.audio>=3.1.0",
            "huggingface_hub>=0.16.0",
        ],
        "all": [
            "torch>=1.9.0",
            "torchaudio>=0.9.0", 
            "pyannote.audio>=3.1.0",
            "huggingface_hub>=0.16.0",
            "matplotlib>=3.5.0",
            "seaborn>=0.11.0",
        ],
        "dev": [
            "pytest>=6.0.0",
            "pytest-cov>=2.12.0",
            "black>=21.0.0",
            "flake8>=3.9.0",
            "mypy>=0.910",
            "pre-commit>=2.15.0",
            "sphinx>=4.0.0",
            "sphinx-rtd-theme>=0.5.0",
            "twine>=3.4.0",
            "build>=0.7.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "video-transcribe=video_transcription.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "video_transcription": ["*.txt", "*.md"],
    },
    keywords=[
        "video transcription",
        "speech recognition", 
        "speaker diarization",
        "whisper",
        "pyannote",
        "gpu acceleration",
        "audio processing",
        "machine learning",
        "ai",
        "nlp"
    ],
    zip_safe=False,
)
