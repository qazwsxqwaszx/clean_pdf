# clean_pdf

一個用於清洗 PDF 檔案中潛在惡意內容的 Python 工具，可以移除 JavaScript、表單、嵌入檔案等危險元素，並生成安全的 PDF 檔案。

## creat_clean_save_pdf

## 功能特點

- **安全性分析**: 檢測 PDF 中的潛在風險（JavaScript、表單、嵌入檔案等）
- **內容提取**: 安全地提取文字和圖像內容
- **清洗重建**: 生成不含惡意內容的新 PDF 檔案
- **詳細日誌**: 記錄處理過程和發現的風險
- **批次處理**: 支援命令列操作

## 系統需求

- Python 3.7 或更高版本
- 支援 Windows、macOS、Linux

## 安裝步驟

### 1. 安裝 Python 依賴套件

```bash
pip install PyPDF2 pymupdf reportlab pillow
```

### 2. 下載工具

將 `pdf_cleaner.py` 檔案下載到你的電腦上。

### 3. 賦予執行權限（Linux/macOS）

```bash
chmod +x pdf_cleaner.py
```

## 使用方法

### 基本用法

清洗單一 PDF 檔案：

```bash
python pdf_cleaner.py suspicious.pdf
```

這將創建一個名為 `suspicious_cleaned.pdf` 的清洗後檔案。

### 指定輸出檔案

```bash
python pdf_cleaner.py suspicious.pdf -o clean_document.pdf
```

### 僅進行安全性分析

如果只想分析檔案風險而不生成清洗後的檔案：

```bash
python pdf_cleaner.py suspicious.pdf -a
```

### 詳細模式

顯示詳細的處理過程：

```bash
python pdf_cleaner.py suspicious.pdf -v
```

### 完整參數範例

```bash
python pdf_cleaner.py input.pdf -o output.pdf -v
```

## 功能說明

### 安全性檢測

工具會檢測以下潛在風險：

- **JavaScript 代碼**: 可能執行惡意腳本
- **互動式表單**: 可能收集敏感信息
- **嵌入檔案**: 隱藏的可執行檔案
- **外部連結**: 可能導向惡意網站
- **註解和標記**: 可能包含惡意內容
- **加密保護**: 可能隱藏惡意內容

### 清洗過程

1. **分析階段**: 掃描原始 PDF 檔案，識別潛在風險
2. **提取階段**: 安全地提取文字和圖像內容
3. **清理階段**: 移除危險字符和代碼片段
4. **重建階段**: 使用清理後的內容創建新的 PDF

### 輸出檔案

清洗後的 PDF 檔案將包含：
- 原始文檔的文字內容（已清理）
- 提取的圖像（如果有）
- 清洗處理的說明
- 原始頁面的結構（重新格式化）

## 日誌檔案

工具會自動創建 `pdf_cleaner.log` 日誌檔案，記錄：
- 處理過程詳情
- 發現的安全性風險
- 錯誤和警告信息
- 執行時間和結果

## 限制說明

- **格式變更**: 清洗後的檔案可能失去原始格式
- **互動功能**: 所有互動元素（表單、按鈕等）將被移除
- **複雜排版**: 複雜的版面配置可能需要手動調整
- **字型支援**: 某些特殊字型可能無法完美保留

## 安全性考量

- 工具在隔離的臨時目錄中處理檔案
- 自動清理臨時檔案
- 不會修改原始檔案
- 所有處理過程都有詳細日誌記錄

## 故障排除

### 常見錯誤

**ImportError: 缺少必要的函式庫**
```bash
pip install PyPDF2 pymupdf reportlab pillow
```

**PermissionError: 權限不足**
- 確保有讀取輸入檔案的權限
- 確保有寫入輸出目錄的權限

**Memory Error: 記憶體不足**
- 對於大型 PDF 檔案，確保有足夠的可用記憶體
- 考慮分批處理大型檔案

### 檢查安裝

驗證所有依賴套件是否正確安裝：

```python
python -c "import PyPDF2, fitz, reportlab, PIL; print('所有套件安裝成功')"
```

## 進階用法

### 整合到其他程式

```python
from pdf_cleaner import PDFCleaner

cleaner = PDFCleaner()
success = cleaner.clean_pdf('input.pdf', 'output.pdf')
if success:
    print("清洗完成")
```

### 批次處理腳本

```bash
#!/bin/bash
for file in *.pdf; do
    python pdf_cleaner.py "$file" -o "clean_${file}"
done
```

## 版本更新

- v1.0: 初始版本，基本清洗功能
- 後續版本將加入更多安全檢測和處理選項

## 技術支援

如遇到問題或需要功能建議，請檢查日誌檔案獲取詳細錯誤信息。

## 免責聲明

此工具僅用於提升 PDF 檔案安全性，無法保證 100% 移除所有潛在威脅。請仍需謹慎處理來源不明的檔案，並保持防毒軟體更新。
