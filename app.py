import os
import json
from datetime import datetime
from fastapi import FastAPI, File, UploadFile
from dotenv import load_dotenv
from utils.ocr import extract_korean_text
from utils.translate import translate_to_english
from utils.parser import parse_ingredients, detect_allergens
from utils.classifier import ProductClassifier

load_dotenv()

app = FastAPI(title="Food OCR Translator", version="1.0")

@app.get("/")
def home():
    return {"message": "Food OCR Translator API is running. Go to /docs to upload an image."}

@app.post("/process-ingredients/")
async def process_ingredients(file: UploadFile = File(...)):
    # Save uploaded file temporarily
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    upload_dir = "./uploads"
    os.makedirs(upload_dir, exist_ok=True)
    temp_path = os.path.join(upload_dir, f"{timestamp}_{file.filename}")

    with open(temp_path, "wb") as f:
        f.write(await file.read())

    try:
        # Step 1: OCR
        korean_text = extract_korean_text(temp_path)

        # Step 2: Translate
        english_text = translate_to_english(korean_text)

        # Step 3: Parse ingredients and allergens
        ingredients = parse_ingredients(english_text)
        allergens = detect_allergens(english_text)

        # ✅ Step 4: Save minimal clean output for AI model
        save_path = temp_path.rsplit(".", 1)[0] + "_data.json"
        data = {
            "ingredients": ingredients,
            "allergens": allergens
        }

        # Step 4: Classify dietary compatibility
        classification_result = classifier.process_ingredients(ingredients, allergens)

        # Step 5: Save complete output
        save_path = temp_path.rsplit(".", 1)[0] + "_data.json"
        data = {
            "raw_korean": korean_text,
            "translated_english": english_text,
            "ingredients": classification_result["ingredients"],
            "allergens": classification_result["allergens"],
            "product_classification": classification_result["product_classification"],
            "friendly_summary": classification_result["friendly_summary"]
        }

        with open(save_path, "w", encoding="utf-8") as jf:
            json.dump(data, jf, ensure_ascii=False, indent=2)

        return {
            "status": "success",
            "saved_file": save_path,
            "ingredients_count": len(ingredients),
            "allergens_count": len(allergens)
        }

    finally:
        # Optional: remove image after processing
        if os.path.exists(temp_path):
            os.remove(temp_path)