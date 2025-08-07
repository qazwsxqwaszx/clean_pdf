#!/usr/bin/env python3
"""
clean_pdf 安裝腳本
PDF Security Cleaner Installation Script
"""

import pathlib

from setuptools import find_packages, setup

# 讀取 README
HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text(encoding="utf-8")

# 讀取 requirements (過濾內建模組和註解)
REQUIREMENTS = []
req_file = HERE / "requirements.txt"
if req_file.exists():
    with open(req_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            # 過濾空行、註解和內建模組
            if (
                line
                and not line.startswith("#")
                and not line.startswith("# ")
                and ">=" in line
            ):  # 只包含有版本號的外部套件
                REQUIREMENTS.append(line)

# 長描述
LONG_DESCRIPTION = """
# clean_pdf - PDF 安全清洗工具

一個專業的 PDF 安全清洗工具，提供兩種清洗模式：

## 🛡️ 雙重安全模式

### 內容提取模式 (pdf_cleaner.py)
- 適用於日常文檔處理
- 保持文字可選取性
- 快速處理
- 部分格式保留

### 列印重建模式 (print.py) ⭐
- 軍用級安全標準
- 完全重建PDF結構  
- 視覺化渲染技術
- 零程式碼威脅

## 🚀 主要特性

- 檢測 JavaScript、表單、嵌入檔案等威脅
- 支援高解析度渲染 (72-1200 DPI)
- 詳細安全分析報告
- 批次處理支援
- 跨平台相容 (Windows/macOS/Linux)

## 📦 安裝

```bash
pip install clean_pdf
```

## 🔧 快速開始

```bash
# 內容提取清洗
python pdf_cleaner.py suspicious.pdf clean.pdf

# 列印重建清洗 (最高安全)
python print.py suspicious.pdf secure.pdf --dpi 300
```

適用於網路安全、企業文檔處理、惡意軟體分析等場景。
"""

setup(
    name="clean_pdf",
    version="1.1.0",
    description="PDF 安全清洗工具 - 雙模式移除 PDF 中的潛在惡意內容",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author="Security Team",
    author_email="security@example.com",
    url="https://github.com/yourusername/clean_pdf",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/clean_pdf/issues",
        "Documentation": "https://github.com/yourusername/clean_pdf/wiki",
        "Source": "https://github.com/yourusername/clean_pdf",
    },
    classifiers=[
        # 開發狀態
        "Development Status :: 4 - Beta",
        # 目標使用者
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        # 主題分類
        "Topic :: Security",
        "Topic :: Utilities",
        "Topic :: Office/Business",
        "Topic :: Multimedia :: Graphics :: Graphics Conversion",
        "Topic :: Text Processing :: Markup",
        # 授權
        "License :: OSI Approved :: MIT License",
        # 程式語言
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        # 作業系統
        "Operating System :: OS Independent",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        # 自然語言
        "Natural Language :: Chinese (Traditional)",
        "Natural Language :: English",
    ],
    keywords=[
        "pdf",
        "security",
        "malware",
        "cleaner",
        "sanitizer",
        "document-security",
        "pdf-processing",
        "threat-removal",
        "安全",
        "PDF清洗",
        "惡意軟體",
        "文檔安全",
    ],
    packages=find_packages(exclude=["tests*", "docs*"]),
    include_package_data=True,
    install_requires=REQUIREMENTS,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=0.991",
        ],
        "windows": [
            "python-magic-bin>=0.4.14",  # Windows 專用的 magic library
        ],
    },
    entry_points={
        "console_scripts": [
            # 主要工具
            "clean_pdf=pdf_cleaner:main",
            "pdf_cleaner=pdf_cleaner:main",
            "pdf_print_cleaner=print:main",
            # 別名
            "clean-pdf=pdf_cleaner:main",
            "pdf-cleaner=pdf_cleaner:main",
            "pdf-print-cleaner=print:main",
        ]
    },
    python_requires=">=3.7",
    zip_safe=False,  # 確保檔案可以正常訪問
    # 套件元數據
    platforms=["any"],
    license="MIT",
    # 安全性和品質標記
    project_urls_label="Links",
)
