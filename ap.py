import streamlit as st
import cv2
import numpy as np
import pandas as pd
import json
from PIL import Image

# Global variables
annotations = []
image = None

# Function to annotate points
def annotate(event, x, y, flags, param):
    global annotations, image
    if event == cv2.EVENT_LBUTTONDOWN:
        label = st.text_input(f"Enter label for point ({x},{y}):", key=len(annotations))
        if label:
            annotations.append({"x": x, "y": y, "label": label})

# Streamlit UI
st.title("🖍 Image Annotation Tool")
uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    # Convert image for OpenCV
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    # Show image with OpenCV annotations
    st.image(image, caption="Click to annotate", use_column_width=True)

    if st.button("Start Annotation"):
        cv2.imshow("Annotate Image", image)
        cv2.setMouseCallback("Annotate Image", annotate)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # Save annotations
    if st.button("Save Annotations"):
        file_format = st.selectbox("Save as:", ["json", "csv"])
        if file_format == "json":
            with open("annotations.json", "w") as f:
                json.dump(annotations, f, indent=4)
            st.success("Annotations saved as JSON.")
        elif file_format == "csv":
            df = pd.DataFrame(annotations)
            df.to_csv("annotations.csv", index=False)
            st.success("Annotations saved as CSV.")

    # Display saved annotations
    if annotations:
        st.write("Annotations:", annotations)
