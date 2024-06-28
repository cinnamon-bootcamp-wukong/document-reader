from paddleocr import PaddleOCR,draw_ocr
import os
import json
from PIL import Image

class wordLevelPaddleOCR:
    def __init__(self, det_lang='ml', use_gpu=False, lang='en', use_angle_cls=True, det_algorithm="DB"):
        self.det_lang = det_lang
        self.use_gpu = use_gpu
        self.lang = lang
        self.use_angle_cls = use_angle_cls
        self.det_algorithm = det_algorithm
        self.ocr = PaddleOCR(det_lang=self.det_lang, use_gpu=self.use_gpu, lang=self.lang, use_angle_cls=self.use_angle_cls, det_algorithm=self.det_algorithm)

    def get_result(self, img_path):
        result = self.ocr.ocr(img_path, cls=self.use_angle_cls)
        return result
    
    def process_result(self, img_path):
        result = self.get_result(img_path)[0]
        cur_text = []
        cur_pos = []
        for line in result:
            boxes = line[0]
            txts = line[1][0]
            ##
            topLeft, topRight, bottomRight, bottomLeft = boxes 
            ##
            dxTop = (topRight[0] - topLeft[0]) / len(txts)
            dxBottom = (bottomRight[0] - bottomLeft[0]) / len(txts)
            dyTop = (topRight[1] - topLeft[1]) / len(txts)
            dyBottom = (bottomRight[1] - bottomLeft[1]) / len(txts)
            ##
            new_txt = txts.split()
            top, bottom = topLeft, bottomLeft
            
            for txt in new_txt:
                newTop = [top[0], top[1]]
                newBottom = [bottom[0], bottom[1]]
                possition = [[top[0], top[1]], newTop, newBottom, [bottom[0], bottom[1]]]

                possition[1][0] += len(txt) * dxTop # p[1][0]
                possition[1][1] += len(txt) * dyTop # p[1][1]
                possition[2][0] += len(txt) * dxBottom #p[2][0]
                possition[2][1] += len(txt) * dyBottom #p[2][1]
                cur_pos.append(possition)
                cur_text.append(txt)

                top[1] +=  dyTop * (len(txt) + 1)
                top[0] += dxTop * (len(txt) + 1)
                bottom[1] += dyBottom * (len(txt) + 1)
                bottom[0] += dxBottom * (len(txt) + 1)

        return list(zip(cur_text, cur_pos))
    
    def export(self, img_path, output_dir):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        result = self.process_result(img_path)

        # Generate JSON output path based on image name
        img_name = os.path.basename(img_path)
        base_name, _ = os.path.splitext(img_name)
        output_json_path = os.path.join(output_dir, f"{base_name}.json")
        output_img_path = os.path.join(output_dir, f"{base_name}_annotated.jpg")

        # Save results to JSON file
        with open(output_json_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=4)

        image = Image.open(img_path).convert('RGB')
        image.save(output_img_path)