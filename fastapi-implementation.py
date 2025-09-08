Read “TableNet: Deep Learning model for end-to-end table detection and tabular data extraction from…“ by Sadiva Madaan on Medium: https://sadiva-madaan9.medium.com/tablenet-deep-learning-model-for-end-to-end-table-detection-and-tabular-data-extraction-from-13cb56e93650

pip install torch torchvision opencv-python


from pdf2image import convert_from_path

pages = convert_from_path("sample.pdf", dpi=300)
pages[0].save("page1.png", "PNG")


import torch
import cv2
from model import TableNet  # custom class from repo

# Load pretrained model
model = TableNet()
model.load_state_dict(torch.load("tablenet_pretrained.pth"))
model.eval()

# Load image
img = cv2.imread("page1.png")
# preprocess (resize, normalize)
input_tensor = preprocess(img).unsqueeze(0)

# Predict
with torch.no_grad():
    table_mask, column_mask = model(input_tensor)

# Post-process masks → get bounding boxes
table_boxes = mask_to_boxes(table_mask)
column_lines = mask_to_lines(column_mask)




