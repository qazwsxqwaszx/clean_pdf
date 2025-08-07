#!/usr/bin/env python3
"""
安全PDF清洗工具 - 移除潛在惡意內容
Security-focused PDF Cleaner - Remove potentially malicious content
"""

import argparse
import hashlib
import logging
import os
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Dict, List, Optional, Tuple

try:
    import fitz  # PyMuPDF
    import magic  # python-magic for file type detection
    import PyPDF2
    from PIL import Image
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.utils import ImageReader
    from reportlab.pdfgen import canvas
except ImportError as e:
    print(f"缺少必要的函式庫: {e}")
    print("請執行: pip install PyPDF2 reportlab PyMuPDF Pillow python-magic")
    sys.exit(1)


class PDFCleaner:
    """
    PDF清洗工具類別 - 實作最高安全標準的PDF清理功能
    """

    def __init__(self):
        self.setup_logging()
        self.dangerous_actions = [
            "/JavaScript",
            "/JS",
            "/Launch",
            "/ImportData",
            "/SubmitForm",
            "/GoTo",
            "/GoToR",
            "/Sound",
            "/Movie",
            "/Rendition",
            "/RichMedia",
            "/3D",
            "/EmbeddedFile",
            "/FileAttachment",
        ]

        # 允許的字體清單（白名單）
        self.allowed_fonts = [
            "Arial",
            "Helvetica",
            "Times",
            "Times-Roman",
            "Courier",
            "Symbol",
            "ZapfDingbats",
        ]

    def setup_logging(self):
        """設定日誌系統"""
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler("pdf_cleaner.log", encoding="utf-8"),
                logging.StreamHandler(sys.stdout),
            ],
        )
        self.logger = logging.getLogger(__name__)

    def verify_pdf_file(self, file_path: str) -> bool:
        """驗證檔案是否為有效PDF"""
        try:
            # 使用magic library檢查檔案類型
            if hasattr(magic, "from_file"):
                mime_type = magic.from_file(file_path, mime=True)
                if mime_type != "application/pdf":
                    self.logger.warning(f"檔案類型不正確: {mime_type}")
                    return False

            # 使用PyPDF2進行基本驗證
            with open(file_path, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                if reader.is_encrypted:
                    self.logger.warning("檔案已加密，需要解密")
                    return False

                # 檢查頁數
                if len(reader.pages) == 0:
                    self.logger.error("PDF檔案沒有頁面")
                    return False

        except Exception as e:
            self.logger.error(f"PDF驗證失敗: {e}")
            return False

        return True

    def scan_malicious_content(self, file_path: str) -> List[str]:
        """掃描惡意內容"""
        threats = []

        try:
            with open(file_path, "rb") as file:
                content = file.read()
                content_str = content.decode("utf-8", errors="ignore")

                # 檢查危險動作
                for action in self.dangerous_actions:
                    if action in content_str:
                        threats.append(f"發現危險動作: {action}")
                        self.logger.warning(f"發現威脅: {action}")

                # 檢查可疑的編碼內容
                if b"%PDF-" not in content[:50]:
                    threats.append("檔案標頭異常")

                # 檢查XFA表單（可能包含惡意腳本）
                if b"<xfa:" in content or b"/XFA" in content:
                    threats.append("發現XFA表單內容")

                # 檢查嵌入檔案
                if b"/EmbeddedFile" in content or b"/FileAttachment" in content:
                    threats.append("發現嵌入檔案")

        except Exception as e:
            self.logger.error(f"掃描過程中發生錯誤: {e}")
            threats.append(f"掃描錯誤: {e}")

        return threats

        # def extract_safe_content(self, input_path: str) -> Tuple[List[Dict], bool]:
        """提取安全內容"""
        safe_content = []
        has_threats = False

        try:
            # 使用PyMuPDF開啟文件
            doc = fitz.open(input_path)

            for page_num in range(doc.page_count):
                page = doc[page_num]

                # 提取純文字內容
                text = page.get_text()

                # 提取圖片（重新編碼以移除潛在威脅）
                # 提取圖片（重新編碼以移除潛在威脅）
            # 提取圖片（重新編碼以移除潛在威脅）
            images = []

            for img in page.get_images(full=True):
                xref = img[0]

                # ① 嘗試取得 bbox
                try:
                    bbox = page.get_image_bbox(xref)  # 只傳 xref
                except ValueError:
                    bbox = None

                pix = None  # 先宣告，避免 finally NameError
                try:
                    # ② 轉成 Pixmap
                    pix = fitz.Pixmap(doc, xref)

                    # ③ 只保留 RGB 圖片
                    if pix.n - pix.alpha < 4:
                        img_data = pix.tobytes("png")
                        images.append(
                            {
                                "data": img_data,
                                "bbox": bbox,
                                "format": "png",
                            }
                        )

                except Exception as e:
                    self.logger.warning(f"處理圖片時發生錯誤: {e}")
                    has_threats = True

                finally:
                    # ④ 釋放 native 記憶體
                    if pix is not None:
                        pix = None
                    # 如果 pix 建立失敗，略過

                # 獲取頁面尺寸
                page_rect = page.rect

                safe_content.append(
                    {
                        "page_num": page_num,
                        "text": text,
                        "images": images,
                        "width": page_rect.width,
                        "height": page_rect.height,
                    }
                )

            doc.close()

        except Exception as e:
            self.logger.error(f"提取內容時發生錯誤: {e}")
            has_threats = True

        return safe_content, has_threats

    def extract_safe_content(self, input_path: str) -> Tuple[List[Dict], bool]:
        safe_content = []
        has_threats = False

        try:
            doc = fitz.open(input_path)

            for page_num in range(doc.page_count):
                try:  # ★ 把風險鎖在單頁
                    page = doc[page_num]

                    # -------- 文字 --------
                    text = page.get_text()

                    # -------- 圖片 --------
                    images = []
                    for img in page.get_images(full=True):
                        xref = img[0]
                        try:
                            bbox = page.get_image_bbox(xref)
                        except ValueError:
                            bbox = None

                        pix = fitz.Pixmap(doc, xref)
                        if pix.n - pix.alpha < 4:
                            img_data = pix.tobytes("png")
                            images.append(
                                {
                                    "data": img_data,
                                    "bbox": bbox,
                                    "format": "png",
                                }
                            )
                        pix = None

                    # -------- 儲存頁面 --------
                    page_rect = page.rect
                    safe_content.append(
                        {
                            "page_num": page_num,
                            "text": text,
                            "images": images,
                            "width": page_rect.width,
                            "height": page_rect.height,
                        }
                    )

                except Exception as e:
                    # 單頁失敗只記錄警告，繼續下一頁
                    self.logger.warning(f"第 {page_num+1} 頁無法處理: {e}")
                    has_threats = True
                    continue

            doc.close()

        except Exception as e:
            self.logger.error(f"開檔或迴圈外層錯誤: {e}")
            has_threats = True

        return safe_content, has_threats

    def create_clean_pdf(self, content_data: List[Dict], output_path: str) -> bool:
        """建立清潔的PDF檔案"""
        try:
            from io import BytesIO

            from reportlab.lib.pagesizes import letter
            from reportlab.pdfgen import canvas

            # 建立新的PDF
            c = canvas.Canvas(output_path, pagesize=letter)

            for page_data in content_data:
                # 設定頁面尺寸
                page_width = page_data["width"] if page_data["width"] > 0 else letter[0]
                page_height = (
                    page_data["height"] if page_data["height"] > 0 else letter[1]
                )

                c.setPageSize((page_width, page_height))

                # 添加文字內容
                if page_data["text"].strip():
                    text_obj = c.beginText()
                    text_obj.setTextOrigin(50, page_height - 50)
                    text_obj.setFont("Helvetica", 12)

                    # 分行處理文字
                    lines = page_data["text"].split("\n")
                    for line in lines:
                        if line.strip():
                            text_obj.textLine(line)

                    c.drawText(text_obj)

                    # 添加安全的圖片
                    # for img in page_data["images"]:
                    try:
                        img_stream = BytesIO(img["data"])
                        # 使用PIL重新處理圖片以確保安全
                        pil_img = Image.open(img_stream)

                        # 轉換為RGB格式（移除可能的威脅）
                        if pil_img.mode != "RGB":
                            pil_img = pil_img.convert("RGB")

                        # 保存為安全的格式
                        safe_img_stream = BytesIO()
                        pil_img.save(safe_img_stream, format="PNG")
                        safe_img_stream.seek(0)

                        # 添加到PDF（如果有邊界框信息）
                        if "bbox" in img and img["bbox"]:
                            bbox = img["bbox"]
                            c.drawImage(
                                ImageReader(safe_img_stream),
                                bbox[0],
                                page_height - bbox[3],
                                bbox[2] - bbox[0],
                                bbox[3] - bbox[1],
                            )
                        else:
                            # 預設位置
                            c.drawImage(ImageReader(safe_img_stream), 50, 50, 200, 200)

                    except Exception as e:
                        self.logger.warning(f"處理圖片時發生錯誤: {e}")
                        continue
                first_img_drawn = False
                for img in page_data["images"]:
                    try:
                        img_stream = BytesIO(img["data"])
                        pil_img = Image.open(img_stream)

                        # 轉成 RGB，確保安全
                        if pil_img.mode != "RGB":
                            pil_img = pil_img.convert("RGB")

                        safe_img_stream = BytesIO()
                        pil_img.save(safe_img_stream, format="PNG")
                        safe_img_stream.seek(0)

                        # ===== ① 如果這頁沒有文字，且還沒畫過背景，就把圖片鋪滿整頁 =====
                        if not page_data["text"].strip() and not first_img_drawn:
                            c.drawImage(
                                ImageReader(safe_img_stream),
                                0,
                                0,
                                width=page_width,
                                height=page_height,
                                preserveAspectRatio=True,
                                anchor="c",  # 置中
                            )
                            first_img_drawn = True
                            continue  # 背景畫好就看下一張圖

                        # ===== ② 其他情況還是依 bbox 疊圖 =====
                        if "bbox" in img and img["bbox"]:
                            bbox = img["bbox"]
                            c.drawImage(
                                ImageReader(safe_img_stream),
                                bbox[0],
                                page_height - bbox[3],
                                bbox[2] - bbox[0],
                                bbox[3] - bbox[1],
                            )
                        else:
                            # 沒 bbox 時，預設縮放 80% 置中
                            scale = 0.8
                            draw_w = page_width * scale
                            draw_h = page_height * scale
                            c.drawImage(
                                ImageReader(safe_img_stream),
                                (page_width - draw_w) / 2,
                                (page_height - draw_h) / 2,
                                draw_w,
                                draw_h,
                                preserveAspectRatio=True,
                                anchor="c",
                            )

                    except Exception as e:
                        self.logger.warning(f"處理圖片時發生錯誤: {e}")
                        continue
                c.showPage()

            c.save()
            self.logger.info(f"清潔PDF已建立: {output_path}")
            return True

        except Exception as e:
            self.logger.error(f"建立清潔PDF時發生錯誤: {e}")
            return False

    def calculate_file_hash(self, file_path: str) -> str:
        """計算檔案雜湊值"""
        hash_sha256 = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_sha256.update(chunk)
        except Exception as e:
            self.logger.error(f"計算雜湊值時發生錯誤: {e}")
            return ""

        return hash_sha256.hexdigest()

    def clean_pdf(self, input_path: str, output_path: str) -> Dict:
        """主要的PDF清洗功能"""
        result = {
            "success": False,
            "threats_found": [],
            "original_hash": "",
            "clean_hash": "",
            "message": "",
        }

        try:
            self.logger.info(f"開始清洗PDF: {input_path}")

            # 1. 驗證輸入檔案
            if not os.path.exists(input_path):
                result["message"] = "輸入檔案不存在"
                return result

            if not self.verify_pdf_file(input_path):
                result["message"] = "檔案驗證失敗"
                return result

            # 2. 計算原始檔案雜湊值
            result["original_hash"] = self.calculate_file_hash(input_path)

            # 3. 掃描威脅
            threats = self.scan_malicious_content(input_path)
            result["threats_found"] = threats

            # 4. 提取安全內容
            content_data, extraction_threats = self.extract_safe_content(input_path)

            if extraction_threats:
                result["threats_found"].append("內容提取過程中發現威脅")

            # 5. 建立清潔的PDF
            if self.create_clean_pdf(content_data, output_path):
                result["clean_hash"] = self.calculate_file_hash(output_path)
                result["success"] = True
                result["message"] = f"PDF清洗完成。發現 {len(threats)} 個威脅並已移除"

                self.logger.info(f"清洗完成: {output_path}")
                self.logger.info(f"原始檔案雜湊: {result['original_hash']}")
                self.logger.info(f"清潔檔案雜湊: {result['clean_hash']}")

            else:
                result["message"] = "建立清潔PDF失敗"

        except Exception as e:
            self.logger.error(f"清洗過程中發生錯誤: {e}")
            result["message"] = f"清洗失敗: {e}"

        return result


def main():
    """主程式入口"""
    parser = argparse.ArgumentParser(description="安全PDF清洗工具")
    parser.add_argument("input", help="輸入PDF檔案路徑")
    parser.add_argument("output", help="輸出清潔PDF檔案路徑")
    parser.add_argument("-v", "--verbose", action="store_true", help="詳細輸出")

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # 建立清洗工具實例
    cleaner = PDFCleaner()

    # 執行清洗
    result = cleaner.clean_pdf(args.input, args.output)

    # 輸出結果
    print("\n" + "=" * 50)
    print("PDF清洗結果報告")
    print("=" * 50)
    print(f"狀態: {'成功' if result['success'] else '失敗'}")
    print(f"訊息: {result['message']}")
    print(f"發現威脅數量: {len(result['threats_found'])}")

    if result["threats_found"]:
        print("\n發現的威脅:")
        for threat in result["threats_found"]:
            print(f"  - {threat}")

    if result["original_hash"]:
        print(f"\n原始檔案雜湊: {result['original_hash']}")
    if result["clean_hash"]:
        print(f"清潔檔案雜湊: {result['clean_hash']}")

    print("=" * 50)

    return 0 if result["success"] else 1


if __name__ == "__main__":
    sys.exit(main())
