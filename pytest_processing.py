import unittest
from unittest.mock import patch
from src.processing import wordLevelPaddleOCR
from src.convert import FileConverter
class TestProcessing(unittest.TestCase):
    def setUp(self):
        self.converter = FileConverter
    def test_export_pdf(self):
        # Mock FileConverter.convert_to_image to return output directory
        with patch.object(FileConverter, 'convert_to_image') as mock_convert:
            mock_convert.return_value = "output_dir"
            # Create wordLevelPaddleOCR instance
            ocr = wordLevelPaddleOCR()
            # Call export with test PDF path
            output_dir = ocr.export("UnitTest/test_processing/pdf_sample.pdf")
            # Assertions
            self.assertEqual(output_dir, "output_dir")
            # Additional assertions for processed JSON data (if applicable)
    def test_export_docx(self):
        # Similar structure as test_export_pdf, replace PDF with DOCX
        with patch.object(FileConverter, 'convert_to_image') as mock_convert:
            mock_convert.return_value = "output_dir"
            ocr = wordLevelPaddleOCR()
            output_dir = ocr.export("UnitTest/test_processing/docx_sample.docx")
            self.assertEqual(output_dir, "output_dir")
            # Additional assertions for processed JSON data (if applicable)
    def test_export_heic(self):
        # Similar structure as test_export_pdf, replace PDF with HEIC
        with patch.object(FileConverter, 'convert_to_image') as mock_convert:
            mock_convert.return_value = "output_dir"
            ocr = wordLevelPaddleOCR()
            output_dir = ocr.export("UnitTest/test_processing/heic_sample.heic")
            self.assertEqual(output_dir, "output_dir")
            # Additional assertions for processed JSON data (if applicable)
    def test_export_tiff(self):
        # Similar structure as test_export_pdf, replace PDF with TIFF
        with patch.object(FileConverter, 'convert_to_image') as mock_convert:
            mock_convert.return_value = "output_dir"
            ocr = wordLevelPaddleOCR()
            output_dir = ocr.export("UnitTest/test_processing/tiff_sample.tiff")
            self.assertEqual(output_dir, "output_dir")
            # Additional assertions for processed JSON data (if applicable)
    def test_export_image(self):
        # Similar structure as test_export_pdf, replace PDF with image
        with patch.object(FileConverter, 'convert_to_image') as mock_convert:
            mock_convert.return_value = "output_dir"
            ocr = wordLevelPaddleOCR()
            output_dir = ocr.export("UnitTest/test_processing/image_sample.png")
            self.assertEqual(output_dir, "output_dir")
            # Additional assertions for processed JSON data (if applicable)
if __name__ == '__main__':
    unittest.main()