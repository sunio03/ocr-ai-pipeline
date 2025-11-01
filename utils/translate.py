from google.cloud import translate_v2 as translate
import html

def translate_to_english(text: str) -> str:
    """
    Translate Korean text to English using Google Cloud Translation API (v2).

    This version:
    ✅ Forces Korean as the source language to avoid auto-detection errors.
    ✅ Handles multi-line and mixed-language input gracefully.
    ✅ Unescapes HTML entities (like &quot;) in the final output.
    """

    if not text or not text.strip():
        return ""

    try:
        # Initialize Google Translate client
        client = translate.Client()

        # Call translation API
        result = client.translate(
            text,
            source_language="ko",   # Force Korean as source
            target_language="en"    # English target
        )

        # Some API responses include escaped HTML entities (e.g., &quot;)
        translated = html.unescape(result.get("translatedText", ""))

        return translated.strip()

    except Exception as e:
        # Handle errors gracefully for debugging and API stability
        print(f"[Translation Error] {e}")
        return "⚠️ Translation failed. Check credentials or API quota."