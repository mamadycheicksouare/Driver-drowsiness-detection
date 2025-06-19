from ultralytics import YOLO
import torch

device = 'cuda' if torch.cuda.is_available() else 'cpu'

model = YOLO('best.pt')
model.to(device)

def classify_face(image):

    results = model(image,verbose=False)
    return results[0].probs.top1

