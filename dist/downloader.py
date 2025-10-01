import yt_dlp

def descargar_video(url, carpeta_destino=".", callback_progreso=None, calidad="maxima"):
    """Descarga un video con opción de calidad y progreso detallado."""

    def hook(d):
        if d['status'] == 'downloading' and callback_progreso:
            total = d.get('total_bytes') or d.get('total_bytes_estimate')
            descargado = d.get('downloaded_bytes', 0)
            if total:
                porcentaje = descargado / total * 100
                callback_progreso(porcentaje, etapa)
        elif d['status'] == 'finished' and callback_progreso:
            callback_progreso(100, etapa)

    # Elegir formato según la calidad
    if calidad == "maxima":
        formato = "bestvideo+bestaudio/best"
    else:
        formato = "best"

    # Etapas (para GUI)
    etapas = ["Descargando video 1/3", "Descargando audio 2/3", "Fusionando 3/3"] if calidad == "maxima" else ["Descargando archivo"]
    etapa_actual = {"index": 0}  # mutable para closure

    def callback_interno(d):
        nonlocal etapa
        # Detectar cambios de estado
        if d['status'] == 'downloading':
            etapa = etapas[etapa_actual["index"]]
        elif d['status'] == 'finished':
            etapa_actual["index"] += 1
            if etapa_actual["index"] < len(etapas):
                etapa = etapas[etapa_actual["index"]]
        hook(d)

    etapa = etapas[0]  # Inicial
    opciones = {
        "outtmpl": f"{carpeta_destino}/%(title).100s.%(ext)s",
        "format": formato,
        "progress_hooks": [callback_interno],
    }

    with yt_dlp.YoutubeDL(opciones) as ydl:
        ydl.download([url])
