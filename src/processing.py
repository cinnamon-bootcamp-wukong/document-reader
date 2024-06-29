from paddleocr import PaddleOCR, draw_ocr
import os
import json
import glob
from PIL import Image
from convert import FileConverter


class wordLevelPaddleOCR:
    """
    A class to perform word-level Optical Character Recognition (OCR) using PaddleOCR.

    Attributes:
        det_lang (str): The language to be used for detection (default is 'ml').
        use_gpu (bool): Whether to use GPU for OCR (default is False).
        lang (str): The language for OCR (default is 'en').
        use_angle_cls (bool): Whether to use angle classification (default is True).
        det_algorithm (str): The detection algorithm to use (default is "DB").
        ocr (PaddleOCR): An instance of PaddleOCR initialized with the given parameters.

    Methods:
        get_result(img_path):
            Performs OCR on the given image and returns the result.

        process_result(img_path):
            Processes the OCR result to extract word-level text and positions.

        export(input_dir, output_dir):
            Processes all images in the input directory, saves results as JSON, and annotated images in the output directory.
    """

    def __init__(
        self, det_lang='ml', use_gpu=False, lang='en', use_angle_cls=True, det_algorithm="DB"
    ):
        self.det_lang = det_lang
        self.use_gpu = use_gpu
        self.lang = lang
        self.use_angle_cls = use_angle_cls
        self.det_algorithm = det_algorithm
        self.ocr = PaddleOCR(
            det_lang=self.det_lang,
            use_gpu=self.use_gpu,
            lang=self.lang,
            use_angle_cls=self.use_angle_cls,
            det_algorithm=self.det_algorithm,
        )

    def __get_result(self, img_path):
        """
        Performs OCR on the given image and returns the result.

        Args:
            img_path (str): The path to the image file.

        Returns:
            list: The OCR result.
        """

        result = self.ocr.ocr(img_path, cls=self.use_angle_cls)
        return result

    def __process_result(self, img_path):
        """
        Processes the OCR result to extract word-level text and positions.

        Args:
            img_path (str): The path to the image file.

        Returns:
            list: A list of tuples containing the text and its corresponding positions.
        """

        result = self.__get_result(img_path)[0]
        cur_text = []
        cur_pos = []
        for line in result:
            boxes = line[0]
            txts = line[1][0]

            topLeft, topRight, bottomRight, bottomLeft = boxes

            dxTop = (topRight[0] - topLeft[0]) / len(txts)
            dxBottom = (bottomRight[0] - bottomLeft[0]) / len(txts)
            dyTop = (topRight[1] - topLeft[1]) / len(txts)
            dyBottom = (bottomRight[1] - bottomLeft[1]) / len(txts)

            new_txt = txts.split()
            top, bottom = topLeft, bottomLeft

            for txt in new_txt:
                newTop = [top[0], top[1]]
                newBottom = [bottom[0], bottom[1]]
                possition = [[top[0], top[1]], newTop, newBottom, [bottom[0], bottom[1]]]

                possition[1][0] += len(txt) * dxTop  # p[1][0]
                possition[1][1] += len(txt) * dyTop  # p[1][1]
                possition[2][0] += len(txt) * dxBottom  # p[2][0]
                possition[2][1] += len(txt) * dyBottom  # p[2][1]
                cur_pos.append(possition)
                cur_text.append(txt)

                top[1] += dyTop * (len(txt) + 1)
                top[0] += dxTop * (len(txt) + 1)
                bottom[1] += dyBottom * (len(txt) + 1)
                bottom[0] += dxBottom * (len(txt) + 1)

        return list(zip(cur_text, cur_pos))

    def export(self, path):
        """
        Export processed results as JSON files for each image in the specified directory.

        Args:
            path (str): The path to the directory where images are stored.

        Example:
            To export results for images in 'data/images/', use:
            >>> instance.export('data/images/')
        """
        converter = FileConverter(path)
        input_dir = converter.convert_to_image()
        file_paths = glob.glob(os.path.join(input_dir, '*'))

        for img_path in file_paths:
            result = self.__process_result(img_path)
            # Generate JSON output path based on image name
            img_name = os.path.basename(img_path)
            base_name, _ = os.path.splitext(img_name)
            output_json_path = os.path.join(input_dir, f"{base_name}.json")

            # Save results to JSON file
            with open(output_json_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=4)
