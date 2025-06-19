import os
import cv2

# Base dataset paths
base_path = '../'  # should contain 'train', 'val', 'test' subfolders
output_base = '../'
resize_shape = (224, 224)

# Define YOLO to bounding box conversion
def yolo_to_bbox(x_center, y_center, width, height, img_w, img_h):
    x_center *= img_w
    y_center *= img_h
    width *= img_w
    height *= img_h
    x1 = int(x_center - width / 2)
    y1 = int(y_center - height / 2)
    x2 = int(x_center + width / 2)
    y2 = int(y_center + height / 2)
    return x1, y1, x2, y2

# Process each split
for split in ['train', 'val', 'test']:
    img_dir = os.path.join(base_path, split, 'images')
    ann_dir = os.path.join(base_path, split, 'labels')
    output_split_dir = os.path.join(output_base, split)
    os.makedirs(output_split_dir, exist_ok=True)

    for ann_file in os.listdir(ann_dir):
        if not ann_file.endswith('.txt'):
            continue

        base_name = os.path.splitext(ann_file)[0]
        img_path = os.path.join(img_dir, base_name + '.jpg')
        if not os.path.exists(img_path):
            img_path = os.path.join(img_dir, base_name + '.png')
        if not os.path.exists(img_path):
            print(f"Image not found for {ann_file}")
            continue

        image = cv2.imread(img_path)
        if image is None:
            print(f"Failed to read image {img_path}")
            continue

        img_h, img_w = image.shape[:2]
        with open(os.path.join(ann_dir, ann_file), 'r') as file:
            lines = file.readlines()
            for idx, line in enumerate(lines):
                parts = line.strip().split()
                if len(parts) != 5:
                    continue
                class_id, x, y, w, h = map(float, parts)
                x1, y1, x2, y2 = yolo_to_bbox(x, y, w, h, img_w, img_h)

                cropped = image[max(0, y1):min(img_h, y2), max(0, x1):min(img_w, x2)]
                if cropped.size == 0:
                    continue

                # Resize crop
                resized_crop = cv2.resize(cropped, resize_shape)

                class_folder = os.path.join(output_split_dir, str(int(class_id)))
                os.makedirs(class_folder, exist_ok=True)
                out_filename = f"{base_name}_{idx}.jpg"
                cv2.imwrite(os.path.join(class_folder, out_filename), resized_crop)

print("✅ Classification dataset created with 224x224 crops.")
