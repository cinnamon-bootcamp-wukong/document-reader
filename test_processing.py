import os
import unittest
import json
from PIL import Image
from src.processing import wordLevelPaddleOCR


class TestWordLevelPaddleOCR(unittest.TestCase):
    def setUp(self):
        # Set up any necessary data or resources for each test case
        self.ocr_processor = wordLevelPaddleOCR()

    def tearDown(self):
        # Clean up any resources after each test case runs
        pass

    def test_pdf_to_json(self):
        pdf_file = 'UnitTest/test_processing/pdf_sample.pdf'
        output_dir = self.ocr_processor.export(pdf_file)
        json_file = os.path.join(output_dir, 'pdf_sample.json')

        self.assertTrue(os.path.exists(json_file), f"JSON file not found: {json_file}")

        # Validate JSON structure and content
        with open(json_file, encoding='utf-8') as f:
            result = json.load(f)
            self.assertIsInstance(result, list)
            self.assertTrue(len(result) > 0)

    def test_docx_to_json(self):
        docx_file = 'UnitTest/test_processing/docx_sample.docx'
        output_dir = self.ocr_processor.export(docx_file)
        json_file = os.path.join(output_dir, 'docx_sample.json')

        self.assertTrue(os.path.exists(json_file), f"JSON file not found: {json_file}")

        # Validate JSON structure and content
        with open(json_file, encoding='utf-8') as f:
            result = json.load(f)
            self.assertIsInstance(result, list)
            self.assertTrue(len(result) > 0)

    def test_heic_to_json(self):
        heic_file = 'UnitTest/test_processing/heic_sample.heic'
        output_dir = self.ocr_processor.export(heic_file)
        json_file = os.path.join(output_dir, 'heic_sample.json')

        self.assertTrue(os.path.exists(json_file), f"JSON file not found: {json_file}")

        # Validate JSON structure and content
        with open(json_file, encoding='utf-8') as f:
            result = json.load(f)
            self.assertIsInstance(result, list)
            self.assertTrue(len(result) > 0)

    def test_tiff_to_json(self):
        tiff_file = 'UnitTest/test_processing/tiff_sample.tiff'
        output_dir = self.ocr_processor.export(tiff_file)
        json_file = os.path.join(output_dir, 'tiff_sample.json')

        self.assertTrue(os.path.exists(json_file), f"JSON file not found: {json_file}")

        # Validate JSON structure and content
        with open(json_file, encoding='utf-8') as f:
            result = json.load(f)
            self.assertIsInstance(result, list)
            self.assertTrue(len(result) > 0)

    def test_png_to_json(self):
        png_file = 'UnitTest/test_processing/image_sample.png'
        output_dir = self.ocr_processor.export(png_file)
        json_file = os.path.join(output_dir, 'image_sample.json')

        self.assertTrue(os.path.exists(json_file), f"JSON file not found: {json_file}")

        # Validate JSON structure and content
        with open(json_file, encoding='utf-8') as f:
            result = json.load(f)
            self.assertIsInstance(result, list)
            self.assertTrue(len(result) > 0)


if __name__ == '__main__':
    unittest.main()
