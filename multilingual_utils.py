
from deep_translator import GoogleTranslator
from langdetect import detect, DetectorFactory

# Ensures consistent detection results
DetectorFactory.seed = 0  

# ----------------------------
# Language Detection
# ----------------------------
def detect_language(text: str) -> str:
    '''
    Detects the language of a given text.
    Returns ISO 639-1 codes (e.g., 'en', 'ta', 'hi', 'te').
    '''
    try:
        lang = detect(text)
        return lang
    except Exception:
        return "en"  # fallback to English if detection fails


# ----------------------------
# Translation Functions
# ----------------------------
def translate_to_english(text: str) -> str:
    '''Translate any language text to English.'''
    try:
        return GoogleTranslator(source="auto", target="en").translate(text)
    except Exception as e:
        return f"[Translation Error to English: {str(e)}]"

def translate_from_english(text: str, target_lang: str) -> str:
    '''Translate English text to the given target language.'''
    try:
        if target_lang == "en":
            return text
        return GoogleTranslator(source="en", target=target_lang).translate(text)
    except Exception as e:
        return f"[Translation Error to {target_lang}: {str(e)}]"


