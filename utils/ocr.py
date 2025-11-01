from google.cloud import vision

def extract_korean_text(image_path: str) -> str:
    """Extract Korean text from an image using Google Vision API."""
    client = vision.ImageAnnotatorClient()
    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.text_detection(image=image)

    if response.error.message:
        raise Exception(response.error.message)

    annotations = response.text_annotations
    if not annotations:
        return ""

    korean_text = annotations[0].description.strip()
    return korean_text