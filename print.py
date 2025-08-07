#!/usr/bin/env python3
"""
PDF列印重建工具 - 透過虛擬列印方式清除PDF威脅
Print-based PDF Cleaner - Remove threats through virtual printing
"""

import argparse
import logging
import os
import sys
import tempfile
from pathlib import Path
from typing import Optional

try:
    import io

    import fitz  # PyMuPDF
    from PIL import Image
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.utils import ImageReader
    from reportlab.pdfgen import canvas
except ImportError as e:
    print(f"缺少必要函式庫: {e}")
    print("請執行: pip install PyMuPDF reportlab Pillow")
    sys.exit(1)


class PDFPrintCleaner:
    """PDF列印清洗器 - 透過渲染重建實現最高安全性"""

    def __init__(self):
        self.setup_logging()

    def setup_logging(self):
        """設定日誌"""
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler("pdf_print_cleaner.log", encoding="utf-8"),
                logging.StreamHandler(sys.stdout),
            ],
        )
        self.logger = logging.getLogger(__name__)

    def render_pdf_to_images(self, input_path: str, dpi: int = 300) -> list:
        """將PDF頁面渲染為圖像"""
        self.logger.info(f"開始渲染PDF: {input_path}")
        rendered_pages = []

        try:
            doc = fitz.open(input_path)

            for page_num in range(doc.page_count):
                self.logger.info(f"渲染第 {page_num + 1}/{doc.page_count} 頁")

                page = doc[page_num]

                # 設定渲染參數 - 高DPI確保品質
                mat = fitz.Matrix(dpi / 72, dpi / 72)  # 縮放係數
                pix = page.get_pixmap(matrix=mat)

                # 轉換為PIL圖像
                img_data = pix.tobytes("png")
                img = Image.open(io.BytesIO(img_data))

                # 確保為RGB模式
                if img.mode != "RGB":
                    img = img.convert("RGB")

                rendered_pages.append(
                    {
                        "image": img,
                        "width": pix.width,
                        "height": pix.height,
                        "page_num": page_num,
                    }
                )

                pix = None  # 釋放記憶體

            doc.close()
            self.logger.info(f"成功渲染 {len(rendered_pages)} 頁")

        except Exception as e:
            self.logger.error(f"渲染過程發生錯誤: {e}")
            raise

        return rendered_pages

    def create_pdf_from_images(self, rendered_pages: list, output_path: str) -> bool:
        """從渲染圖像創建新PDF"""
        self.logger.info(f"開始創建PDF: {output_path}")

        try:
            # 創建PDF畫布
            c = canvas.Canvas(output_path)

            for page_data in rendered_pages:
                img = page_data["image"]
                width = page_data["width"]
                height = page_data["height"]

                self.logger.info(f"處理第 {page_data['page_num'] + 1} 頁")

                # 將圖像轉換為可用於ReportLab的格式
                img_buffer = io.BytesIO()
                img.save(img_buffer, format="PNG", optimize=True)
                img_buffer.seek(0)

                # 設定頁面大小為原始尺寸
                page_width = width * 72 / 300  # 轉換為點 (points)
                page_height = height * 72 / 300

                c.setPageSize((page_width, page_height))

                # 將圖像放置到頁面上
                c.drawImage(
                    ImageReader(img_buffer),
                    0,
                    0,
                    page_width,
                    page_height,
                    preserveAspectRatio=True,
                )

                c.showPage()

            c.save()
            self.logger.info(f"PDF創建完成: {output_path}")
            return True

        except Exception as e:
            self.logger.error(f"創建PDF時發生錯誤: {e}")
            return False

    def print_clean_pdf(
        self, input_path: str, output_path: str, dpi: int = 300
    ) -> dict:
        """主要清洗功能 - 透過列印重建"""
        result = {
            "success": False,
            "message": "",
            "pages_processed": 0,
            "output_file": output_path,
        }

        try:
            # 檢查輸入檔案
            if not os.path.exists(input_path):
                result["message"] = "輸入檔案不存在"
                return result

            self.logger.info(f"開始列印清洗: {input_path} -> {output_path}")
            self.logger.info(f"使用DPI: {dpi}")

            # 第一階段：渲染PDF為圖像
            rendered_pages = self.render_pdf_to_images(input_path, dpi)

            if not rendered_pages:
                result["message"] = "無法渲染PDF頁面"
                return result

            result["pages_processed"] = len(rendered_pages)

            # 第二階段：從圖像重建PDF
            if self.create_pdf_from_images(rendered_pages, output_path):
                result["success"] = True
                result["message"] = f"列印清洗完成，處理了 {len(rendered_pages)} 頁"

                # 檢查輸出檔案大小
                if os.path.exists(output_path):
                    size_mb = os.path.getsize(output_path) / (1024 * 1024)
                    self.logger.info(f"輸出檔案大小: {size_mb:.2f} MB")
            else:
                result["message"] = "重建PDF失敗"

        except Exception as e:
            self.logger.error(f"列印清洗過程發生錯誤: {e}")
            result["message"] = f"處理失敗: {str(e)}"

        return result


def main():
    """主程式入口"""
    parser = argparse.ArgumentParser(
        description="PDF列印清洗工具 - 透過虛擬列印移除所有潛在威脅"
    )
    parser.add_argument("input", help="輸入PDF檔案路徑")
    parser.add_argument("output", help="輸出清潔PDF檔案路徑")
    parser.add_argument(
        "--dpi", type=int, default=300, help="渲染DPI (預設: 300, 建議範圍: 150-600)"
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="詳細輸出")

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # 驗證DPI範圍
    if args.dpi < 72 or args.dpi > 1200:
        print("警告: DPI應在72-1200範圍內，使用預設值300")
        args.dpi = 300

    # 創建清洗工具
    cleaner = PDFPrintCleaner()

    # 執行列印清洗
    result = cleaner.print_clean_pdf(args.input, args.output, args.dpi)

    # 輸出結果報告
    print("\n" + "=" * 60)
    print("PDF列印清洗結果報告")
    print("=" * 60)
    print(f"處理狀態: {'✅ 成功' if result['success'] else '❌ 失敗'}")
    print(f"處理訊息: {result['message']}")
    print(f"處理頁數: {result['pages_processed']}")

    if result["success"]:
        print(f"輸出檔案: {result['output_file']}")
        print("\n🔒 安全性說明:")
        print("- 所有原始PDF結構已完全移除")
        print("- JavaScript、表單、嵌入檔案等威脅已消除")
        print("- 檔案內容已透過視覺渲染重建")
        print("- 這是最高安全等級的PDF清洗方式")

    print("=" * 60)

    return 0 if result["success"] else 1


if __name__ == "__main__":
    sys.exit(main())
