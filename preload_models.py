import easyocr

# This script is run only once when the Docker image is built.
# It forces EasyOCR to download its language models.
print("Downloading EasyOCR models...")
reader = easyocr.Reader(['en'])
print("Model download complete.")