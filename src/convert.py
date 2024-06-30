import os
from PIL import Image
import fitz  # PyMuPDF
import mammoth
from weasyprint import HTML, CSS
import pyheif
import pymupdf


class FileConverter:
    """
    FileConverter class converts various file types (images, PDFs, documents) into images.

    Static Methods:
    - __detect_file_type(): Detects the type of file based on its extension.
    - __convert_docx_to_pdf(): Converts DOCX files to PDF.
    - __convert_pdf_to_image(): Converts PDF pages to images.
    - __convert_heic_to_png(): Converts HEIC files to PNG.
    - __convert_tiff_to_png(): Converts TIFF files to PNG.
    """

    def __init__(self, input_file):
        if not input_file:
            raise ValueError("Input file path cannot be null.")
        self.path = input_file

    @staticmethod
    def __detect_file_type(file_path):
        """
        Detects the type of the input file (image, PDF, or document).

        Args:
            file_path (str): The path to the input file.

        Returns:
            str: The detected file type ("image", "pdf", "document", or "unknown").
        """
        file_extension = os.path.splitext(file_path)[1].lower()
        if file_extension in [".jpg", ".png", ".heic", ".tiff", ".tif"]:
            return "image"
        elif file_extension == ".pdf":
            return "pdf"
        elif file_extension in [".doc", ".docx"]:
            return "document"
        else:
            return "unknown"

    @staticmethod
    def __convert_docx_to_pdf(docx_file_path, pdf_file_path):
        """
        Converts a Microsoft Word (DOCX) file to a PDF file, preserving images.
        Args:
            docx_file_path (str): The path to the DOCX file.
            pdf_file_path (str): The path where the PDF file will be saved.
        """
        try:
            with open(docx_file_path, "rb") as docx_file:
                result = mammoth.convert_to_html(docx_file)
                html = result.value
            script_dir = os.path.dirname(os.path.abspath(__file__))
            script_dir = os.path.join(script_dir, 'style')
            custom_css = CSS(filename=os.path.join(script_dir, 'custom.css'))
            HTML(string=html).write_pdf(
                pdf_file_path,
                page_size='A4',
                page_orientation='portrait',
                margin={'top': '1in', 'right': '1in', 'bottom': '1in', 'left': '1in'},
                zoom=0.9,
                stylesheets=[custom_css],
            )
            print(f"Conversion successful: {docx_file_path} -> {pdf_file_path}")
        except Exception as e:
            print(f"Conversion failed: {docx_file_path} -> {pdf_file_path}")
            print(f"Error: {e}")

    @staticmethod
    def __convert_pdf_to_image(file_path, save_dir):
        """
        Converts a PDF file to images and saves them in the output directory.

        Args:
            file_path (str): The path to the PDF file.
            save_dir (str): The directory where the images will be saved.
        """
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        with fitz.open(file_path) as pdf:
            for i, page in enumerate(pdf):
                mat = fitz.Matrix(1, 1)
                pm = page.get_pixmap(matrix=mat, alpha=False)
                img = Image.frombytes("RGB", [pm.width, pm.height], pm.samples)
                img_path = os.path.join(save_dir, f'{file_name}_result_page_{i+1}.png')
                img.save(img_path)
                print(f"Saved image: {img_path}")

    @staticmethod
    def __convert_heic_to_png(heic_file_path, output_file_path):
        """
        Converts a HEIC file to PNG and saves it.

        Args:
            heic_file_path (str): The path to the HEIC file.
            output_file_path (str): The path where the PNG file will be saved.
        """
        try:
            heif_file = pyheif.read(heic_file_path)
            image = Image.frombytes(
                heif_file.mode,
                heif_file.size,
                heif_file.data,
                "raw",
                heif_file.mode,
                heif_file.stride,
            )
            image.save(output_file_path, "PNG")
            print(f"Conversion successful: {heic_file_path} -> {output_file_path}")
        except Exception as e:
            print(f"Conversion failed: {heic_file_path} -> {output_file_path}")
            print(f"Error: {e}")

    @staticmethod
    def __convert_tiff_to_png(tiff_file_path, output_file_path):
        """
        Converts a TIFF file to PNG and saves it.

        Args:
            tiff_file_path (str): The path to the TIFF file.
            output_file_path (str): The path where the PNG file will be saved.
        """
        try:
            image = Image.open(tiff_file_path)
            image.save(output_file_path, "PNG")
            print(f"Conversion successful: {tiff_file_path} -> {output_file_path}")
        except FileNotFoundError:
            print(f"Error: File not found - {tiff_file_path}")
        except Exception as e:
            print(f"Conversion failed: {tiff_file_path} -> {output_file_path}")
            print(f"Error: {e}")

    def convert_to_image(self):
        try:
            path = self.path
            base_name = os.path.splitext(os.path.basename(path))[0]
            cur_dir = os.path.dirname(path)
            out_dir = os.path.join(cur_dir, base_name)
            os.makedirs(out_dir, exist_ok=True)

            file_type = self.__detect_file_type(self.path)

            if file_type == "image":
                file_extension = os.path.splitext(path)[1].lower()
                output_file_path = os.path.join(out_dir, base_name + ".png")

                if file_extension == ".heic":
                    self.__convert_heic_to_png(path, output_file_path)
                elif file_extension in [".tiff", ".tif"]:
                    self.__convert_tiff_to_png(path, output_file_path)
                else:
                    Image.open(path).save(output_file_path)
                    print(f"Conversion successful: {path} -> {output_file_path}")

            elif file_type == "pdf":
                self.__convert_pdf_to_image(path, out_dir)

            elif file_type == "document":
                temp_pdf_path = os.path.join(out_dir, base_name + ".pdf")
                self.__convert_docx_to_pdf(path, temp_pdf_path)
                self.__convert_pdf_to_image(temp_pdf_path, out_dir)
                os.remove(temp_pdf_path)
            else:
                print(f"Unsupported file type: {file_type}")
                return
            return out_dir
        except Exception as e:
            print(f"Conversion failed: {self.path} -> {out_dir}")
            print(f"Error: {e}")
            os.rmdir(out_dir)
