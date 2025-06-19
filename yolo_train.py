from ultralytics import YOLO

import torch

torch.cuda.empty_cache()

model = YOLO('yolov8n-cls.pt')


results = model.train(data= "../data",
    epochs=100,  
    imgsz = 224,
    batch=32,
    optimizer='Adam',
    pretrained=True,
    device=0

    )


model.export(format='onnx')