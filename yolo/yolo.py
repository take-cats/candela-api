from collections import Counter
import torch
from yolov5.models.common import AutoShape
from uitl_enums import AnalyseType


model: AutoShape = torch.hub.load("ultralytics/yolov5", "yolov5s")

class YoLo:
    @staticmethod
    def analyser(filename: str, type: AnalyseType):
        if type == AnalyseType.IMAGE:
            model(filename).crop()
        elif type == AnalyseType.TEXT:
            res = model(filename).pandas().xyxy[0].values.tolist()
            
            object = []

            for i in res:
                object.append(i[6])

            count = {}

            for i in object:
                try:
                    count[i] += 1
                except:
                    count[i] = 1

            print(count)

            return object