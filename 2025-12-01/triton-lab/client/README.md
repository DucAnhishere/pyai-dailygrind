# Triton Inference Client

This client tests the Car Corner Classification model using images from the `data/img/` folder.

## Setup

1. Ensure Triton server is running:
   ```bash
   cd /Users/testadmin/Desktop/Desktop-Mac/Python/2025-12-01/triton-lab
   docker-compose up -d
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the client to test all images in the data folder:

```bash
python triton_client.py
```

## What it does

- Loads all images from `../../../data/img/` (relative to client folder)
- Preprocesses images to 384x384 RGB
- Sends inference requests to Triton server at `http://localhost:8000`
- Displays predictions for each image
- Saves results to `inference_results.json`

## Model Details

- **Model**: CarCorner.Classification.MobileNetV3.imgsz384.trt2208.fp16
- **Input**: [1, 3, 384, 384] FP32 (normalized to [0,1])
- **Output**: [1, 12] FP32 (classification scores)
- **Backend**: ONNX Runtime

## Output

For each image, the client shows:
- Predicted class (0-11)
- Confidence score
- Top 3 predictions with scores

Results are saved to `inference_results.json` with detailed scores for all classes.