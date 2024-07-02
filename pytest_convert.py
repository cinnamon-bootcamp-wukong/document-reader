import os
import pytest
from src.convert import FileConverter


@pytest.mark.parametrize(
    "file_path, file_type, expected_extension",
    [
        ("UnitTest/test_convert/pdf_sample.pdf", "pdf", "pdf"),
        ("UnitTest/test_convert/docx_sample.docx", "docx", "png"),
        ("UnitTest/test_convert/heic_sample.heic", "heic", "png"),
        ("UnitTest/test_convert/tiff_sample.tiff", "tiff", "png"),
        ("UnitTest/test_convert/image_sample.png", "png", "png"),
    ],
)
def test_input_file(file_path, file_type, expected_extension):
    if file_path:
        converter = FileConverter(file_path)
        output_dir = converter.convert_to_image()
        assert os.path.exists(output_dir)
        files_in_output_dir = os.listdir(output_dir)
        assert len(files_in_output_dir) > 0
        output_file_path = os.path.join(output_dir, files_in_output_dir[0])
        assert output_file_path.endswith('png')
