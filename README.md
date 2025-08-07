# clean_pdf

一個用於清洗 PDF 檔案中潛在惡意內容的 Python 工具，提供兩種清洗模式：內容提取重建和列印重建，可以移除 JavaScript、表單、嵌入檔案等危險元素，並生成安全的 PDF 檔案。

## 功能特點

- **雙重清洗模式**: 
  - 內容提取模式 (`pdf_cleaner.py`) - 保持格式的安全清洗
  - 列印重建模式 (`print.py`) - 最高安全等級的完全重建
- **安全性分析**: 檢測 PDF 中的潛在風險（JavaScript、表單、嵌入檔案等）
- **內容提取**: 安全地提取文字和圖像內容
- **列印重建**: 透過視覺化渲染完全重建PDF結構
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

將 `pdf_cleaner.py` 和 `print.py` 檔案下載到你的電腦上。

### 3. 賦予執行權限（Linux/macOS）

```bash
chmod +x pdf_cleaner.py
chmod +x print.py
```

## 使用方法

### 模式一：內容提取清洗 (pdf_cleaner.py)

適用於需要保持原始格式和文字可選取的情況。

**基本用法**：
```bash
python pdf_cleaner.py suspicious.pdf clean_document.pdf
```

**詳細模式**：
```bash
python pdf_cleaner.py suspicious.pdf clean_document.pdf -v
```

### 模式二：列印重建清洗 (print.py) ⭐ 推薦

提供最高安全等級，適用於高風險PDF檔案。

**基本用法**：
```bash
python print.py suspicious.pdf secure_document.pdf
```

**高品質模式**：
```bash
python print.py suspicious.pdf secure_document.pdf --dpi 600
```

**詳細輸出**：
```bash
python print.py suspicious.pdf secure_document.pdf --dpi 300 -v
```

## 清洗模式比較

| 特性 | 內容提取模式 | 列印重建模式 |
|------|------------|------------|
| 安全等級 | 高 | 最高 ⭐ |
| 格式保留 | 部分保留 | 視覺完全保留 |
| 文字可選取 | 是 | 否（圖像化） |
| 處理速度 | 快 | 較慢 |
| 檔案大小 | 較小 | 較大 |
| 適用場景 | 日常文檔處理 | 高風險檔案處理 |

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

#### 內容提取模式
1. **分析階段**: 掃描原始 PDF 檔案，識別潛在風險
2. **提取階段**: 安全地提取文字和圖像內容
3. **清理階段**: 移除危險字符和代碼片段
4. **重建階段**: 使用清理後的內容創建新的 PDF

#### 列印重建模式 🔒
1. **渲染階段**: 將每頁PDF渲染為高解析度圖像
2. **安全轉換**: 將圖像轉為安全的RGB格式
3. **重建階段**: 從純圖像重新組成PDF
4. **驗證階段**: 確保所有原始結構已完全移除

### 輸出檔案

**內容提取模式輸出**：
- 原始文檔的文字內容（已清理）
- 提取的圖像（重新編碼）
- 清洗處理的說明
- 原始頁面的結構（重新格式化）

**列印重建模式輸出**：
- 完全重建的PDF結構
- 高品質視覺化內容
- 零程式碼、零威脅的純圖像PDF
- 完整的頁面佈局保留

## 日誌檔案

工具會自動創建日誌檔案，記錄：
- `pdf_cleaner.log` - 內容提取模式日誌
- `pdf_print_cleaner.log` - 列印重建模式日誌
- 處理過程詳情和發現的安全性風險
- 錯誤和警告信息
- 執行時間和結果

## 參數說明

### pdf_cleaner.py 參數
```bash
python pdf_cleaner.py <輸入檔案> <輸出檔案> [-v|--verbose]
```

### print.py 參數
```bash
python print.py <輸入檔案> <輸出檔案> [--dpi DPI值] [-v|--verbose]
```

- `--dpi`: 渲染解析度 (72-1200，預設300)
  - 150 DPI: 快速處理，適中品質
  - 300 DPI: 平衡模式，推薦使用
  - 600 DPI: 高品質模式，檔案較大

## 限制說明

### 內容提取模式限制
- **格式變更**: 清洗後的檔案可能失去原始格式
- **互動功能**: 所有互動元素（表單、按鈕等）將被移除
- **複雜排版**: 複雜的版面配置可能需要手動調整
- **字型支援**: 某些特殊字型可能無法完美保留

### 列印重建模式限制
- **檔案大小**: 輸出檔案通常較大
- **文字選取**: 內容將圖像化，無法選取文字
- **處理時間**: 高解析度渲染需要更多時間
- **記憶體需求**: 大型檔案需要較多記憶體

## 安全性考量

- 工具在隔離的臨時目錄中處理檔案
- 自動清理臨時檔案
- 不會修改原始檔案
- 所有處理過程都有詳細日誌記錄
- **列印重建模式提供軍用級安全性** 🔒

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
- 對於大型 PDF 檔案，降低 DPI 設定
- 考慮使用內容提取模式
- 確保有足夠的可用記憶體

### 檢查安裝

驗證所有依賴套件是否正確安裝：

```python
python -c "import PyPDF2, fitz, reportlab, PIL; print('所有套件安裝成功')"
```

## 進階用法

### 整合到其他程式

**內容提取模式**：
```python
from pdf_cleaner import PDFCleaner

cleaner = PDFCleaner()
result = cleaner.clean_pdf('input.pdf', 'output.pdf')
if result['success']:
    print("清洗完成")
```

**列印重建模式**：
```python
from print import PDFPrintCleaner

cleaner = PDFPrintCleaner()
result = cleaner.print_clean_pdf('input.pdf', 'output.pdf', dpi=300)
if result['success']:
    print("列印重建完成")
```

### 批次處理腳本

**混合模式批次處理**：
```bash
#!/bin/bash
for file in *.pdf; do
    echo "處理檔案: $file"
    # 高風險檔案使用列印重建
    if [[ "$file" == *"suspicious"* ]]; then
        python print.py "$file" "secure_${file}" --dpi 300
    else
        python pdf_cleaner.py "$file" "clean_${file}"
    fi
done
```

## 使用建議

### 選擇適當的清洗模式

1. **一般文檔** → 使用內容提取模式 (`pdf_cleaner.py`)
2. **可疑檔案** → 使用列印重建模式 (`print.py`)
3. **機密文檔** → 使用列印重建模式高DPI設定
4. **快速處理** → 使用內容提取模式
5. **最高安全** → 使用列印重建模式

### DPI 設定建議

- **文字為主的文檔**: 150-300 DPI
- **圖像豐富的文檔**: 300-600 DPI
- **技術圖表/工程圖**: 600 DPI
- **快速預覽**: 150 DPI

## 版本更新

- v1.0: 初始版本，內容提取清洗功能
- v1.1: 新增列印重建模式，提供最高安全等級
- 後續版本將加入更多安全檢測和處理選項

## 技術支援

如遇到問題或需要功能建議，請檢查對應的日誌檔案獲取詳細錯誤信息。

## 免責聲明

此工具僅用於提升 PDF 檔案安全性，無法保證 100% 移除所有潛在威脅。建議：
- 對高風險檔案使用列印重建模式
- 謹慎處理來源不明的檔案
- 保持防毒軟體更新
- 在隔離環境中測試可疑檔案