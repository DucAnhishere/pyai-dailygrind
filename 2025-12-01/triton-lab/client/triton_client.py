#!/usr/bin/env python3
"""
Triton Inference Client for Car Corner Classification Model
Tests all images in the data/img folder
"""

import os
import sys
import json
import numpy as np
from PIL import Image
import requests
import glob
from pathlib import Path

# Triton server configuration
TRITON_URL = "http://localhost:8000"
MODEL_NAME = "CarCorner.Classification.MobileNetV3.imgsz384.trt2208.fp16"
MODEL_VERSION = "1"

def preprocess_image(image_path, target_size=(384, 384)):
    """
    Preprocess image for model input
    - Resize to target_size
    - Convert to RGB
    - Normalize to [0, 1]
    - Convert to float32
    - Flatten to [1, 3, H, W] shape
    """
    try:
        # Load image
        img = Image.open(image_path).convert('RGB')

        # Resize
        img = img.resize(target_size, Image.Resampling.LANCZOS)

        # Convert to numpy array and normalize
        img_array = np.array(img, dtype=np.float32) / 255.0

        # Transpose to [C, H, W] and add batch dimension [1, C, H, W]
        img_array = np.transpose(img_array, (2, 0, 1))
        img_array = np.expand_dims(img_array, axis=0)

        # Flatten to 1D array for JSON
        img_flat = img_array.flatten().tolist()

        return img_flat, img_array.shape

    except Exception as e:
        print(f"Error preprocessing {image_path}: {e}")
        return None, None

def infer_with_triton(image_data):
    """
    Send inference request to Triton server
    """
    payload = {
        "inputs": [
            {
                "name": "input",
                "shape": [1, 3, 384, 384],
                "datatype": "FP32",
                "data": image_data
            }
        ],
        "outputs": [
            {
                "name": "output"
            }
        ]
    }

    try:
        response = requests.post(
            f"{TRITON_URL}/v2/models/{MODEL_NAME}/infer",
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=30
        )

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def get_class_prediction(outputs):
    """
    Extract class prediction from model outputs
    """
    if not outputs or len(outputs) == 0:
        return None

    output_data = outputs[0]['data']
    predicted_class = np.argmax(output_data)
    confidence = output_data[predicted_class]

    return {
        'class': int(predicted_class),
        'confidence': float(confidence),
        'all_scores': output_data
    }

def main():
    # Get data directory path
    script_dir = Path(__file__).parent
    data_dir = script_dir.parent.parent.parent / "data" / "img"

    if not data_dir.exists():
        print(f"Data directory not found: {data_dir}")
        sys.exit(1)

    # Get all image files
    image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.tiff']
    image_files = []
    for ext in image_extensions:
        image_files.extend(data_dir.glob(ext))

    if not image_files:
        print(f"No image files found in {data_dir}")
        sys.exit(1)

    print(f"Found {len(image_files)} images to test")
    print(f"Model: {MODEL_NAME}")
    print(f"Triton URL: {TRITON_URL}")
    print("-" * 60)

    results = []

    for image_path in sorted(image_files):
        print(f"Processing: {image_path.name}")

        # Preprocess image
        image_data, shape = preprocess_image(image_path)
        if image_data is None:
            continue

        print(f"  Input shape: {shape}")

        # Send to Triton
        response = infer_with_triton(image_data)
        if response is None:
            print("  Inference failed")
            continue

        # Get prediction
        prediction = get_class_prediction(response['outputs'])
        if prediction:
            print(f"  Predicted class: {prediction['class']}")
            print(".4f")
            print(f"  Top 3 scores: {np.argsort(prediction['all_scores'])[-3:][::-1]}")
            print(f"  Top 3 confidences: {np.sort(prediction['all_scores'])[-3:][::-1]}")

            results.append({
                'image': image_path.name,
                'prediction': prediction
            })
        else:
            print("  Failed to parse prediction")

        print()

    # Save results to JSON
    if results:
        output_file = script_dir / "inference_results.json"
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"Results saved to: {output_file}")

    print(f"Processed {len(results)}/{len(image_files)} images successfully")

if __name__ == "__main__":
    main()