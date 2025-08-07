#!/usr/bin/env python3
"""
clean_pdf 安裝腳本
"""

import pathlib

from setuptools import find_packages, setup

# 讀取 README
HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text(encoding="utf-8")

# 讀取 requirements
REQUIREMENTS = []
req_file = HERE / "requirements_txt.txt"
if req_file.exists():
    with open(req_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                REQUIREMENTS.append(line)

setup(
    name="clean_pdf",
    version="1.0",
    description="PDF 安全清洗工具 - 移除 PDF 中的潛在惡意內容",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=REQUIREMENTS,
    entry_points={
        "console_scripts": [
            "clean_pdf=clean_pdf.clean_pdf_main:main",
        ]
    },
    python_requires=">=3.7",
)
