# i18n.py

translations = {
    "es": {
        "title": "Descargador Multi-Plataforma",
        "label_urls": "Ingresa las URLs (separadas por espacio o salto de línea):",
        "button_validate": "Validar links",
        "button_start": "Descargar",
        "button_folder": "Cambiar carpeta",
        "label_dest": "Carpeta destino:",
        "label_quality": "Selecciona la calidad:",
        "quality_max": "Máxima calidad",
        "quality_fast": "Descarga rápida",
        "waiting": "Esperando...",
        "warning": "Advertencia",
        "error": "Error",
        "done": "Finalizado",
        "validate_first": "Primero valida los links para continuar.",
        "select_quality": "Selecciona una opción de calidad.",
        "no_urls": "No se detectaron URLs.",
        "urls_detected": "Links detectados:",
        "all_done": "Todas las descargas completadas."
    },
    "en": {
        "title": "Multi-Platform Downloader",
        "label_urls": "Enter URLs (separated by space or newline):",
        "button_validate": "Validate links",
        "button_start": "Download",
        "button_folder": "Change folder",
        "label_dest": "Destination folder:",
        "label_quality": "Select quality:",
        "quality_max": "Best quality",
        "quality_fast": "Fast download",
        "waiting": "Waiting...",
        "warning": "Warning",
        "error": "Error",
        "done": "Completed",
        "validate_first": "Validate links first to continue.",
        "select_quality": "Select a quality option.",
        "no_urls": "No URLs detected.",
        "urls_detected": "Links detected:",
        "all_done": "All downloads completed."
    }
}

current_lang = "es"

def set_language(lang_code):
    global current_lang
    if lang_code in translations:
        current_lang = lang_code
    else:
        raise ValueError(f"Idioma no soportado: {lang_code}")

def t(key):
    return translations[current_lang].get(key, key)
