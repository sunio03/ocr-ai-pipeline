# OCR Ingredient Classifier

## Setup

### 1. Download the Model
Download the fine-tuned model from Google Drive:
[Download Model]
https://drive.google.com/drive/u/0/folders/1eQkL4id4MjxrrO94TJZZYqO5mm4h3a_r

Extract the zip file inside the folder models to achieve `./models/classifier_model/`

Your structure should look like:
```
ocr-ai-pipeline/
├─ models/
│   └─ classifier_model/
│       ├─ config.json
│       ├─ pytorch_model.bin
│       └─ ...
```

### 2. Install Dependencies
pip install -r requirements.txt

### 3. Set up Google Cloud Credentials
Add your `service_account.json` and update `.env`

### 4. Run
uvicorn app:app --reload

**3. Update your `.gitignore`**
models/