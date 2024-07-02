# Document Reader

This project facilitates document processing and Optical Character Recognition (OCR) using Python. It includes functionalities to convert various file types to images and perform word-level OCR using PaddleOCR.

## Features

- **File Conversion**: Convert images, PDFs, and documents (DOCX) to PNG images.
- **OCR**: Perform word-level OCR on images using PaddleOCR.
- **Export**: Save OCR results as JSON files.


## Files

### convert.py

Contains methods to convert various file types to PNG images:
- **__detect_file_type**: Detects file type (image, PDF, document).
- **__convert_docx_to_pdf**: Converts DOCX to PDF.
- **__convert_pdf_to_image**: Converts PDF to images.
- **__convert_heic_to_png**: Converts HEIC to PNG.
- **__convert_tiff_to_png**: Converts TIFF to PNG.
- **convert_to_image**: Orchestrates file conversion based on type.

### processing.py

Provides word-level OCR using PaddleOCR:
- **wordLevelPaddleOCR**: Class for OCR operations.
- **__get_result**: Performs OCR and returns results.
- **__process_result**: Processes OCR results into JSON format.
- **export**: Processes images in a directory and saves OCR results as JSON.

### main.py

Main script to run OCR on files and optionally upload results to cloud storage.

### upload.py

Uploads a folder to cloud services using `rclone`.

## Usage

To perform OCR on files in a directory and save results locally:

```bash
python main.py --input_file <path_to_directory>
```


To upload results to cloud storage:
```bash
python main.py --input_file <path_to_directory> --upload --rclone_remote_name <remote_name> --remote_dir_path <remote_path>
```

## Requirements

Install dependencies using `requirements.txt`:
```bash
pip install -r requirements.txt
```

## Testing

Unit tests are located in `UnitTest/test_processing/` and `UnitTest/test_convert/`. Use pytest to run tests:
```bash
pytest test_processing.py
```



