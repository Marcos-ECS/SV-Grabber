import yt_dlp

def descargar_videos(urls, carpeta_destino=".", callback_progreso=None, calidad="maxima"):
    """Descarga múltiples videos, detectando automáticamente la plataforma."""

    for index, url in enumerate(urls, start=1):
        def hook(d):
            if d['status'] == 'downloading' and callback_progreso:
                total = d.get('total_bytes') or d.get('total_bytes_estimate')
                descargado = d.get('downloaded_bytes', 0)
                if total:
                    porcentaje = descargado / total * 100
                    callback_progreso(porcentaje, etapa, index, len(urls))
            elif d['status'] == 'finished' and callback_progreso:
                callback_progreso(100, etapa, index, len(urls))

        # formato
        formato = "bestvideo+bestaudio/best" if calidad == "maxima" else "best"

        etapas = ["Descargando video", "Descargando audio", "Fusionando"] if calidad == "maxima" else ["Descargando archivo"]
        etapa_actual = {"index": 0}

        def callback_interno(d):
            nonlocal etapa
            if d['status'] == 'downloading':
                etapa = etapas[etapa_actual["index"]]
            elif d['status'] == 'finished':
                etapa_actual["index"] += 1
                if etapa_actual["index"] < len(etapas):
                    etapa = etapas[etapa_actual["index"]]
            hook(d)

        etapa = etapas[0]
        opciones = {
            "outtmpl": f"{carpeta_destino}/%(title).100s.%(ext)s",
            "format": formato,
            "progress_hooks": [callback_interno],
        }

        with yt_dlp.YoutubeDL(opciones) as ydl:
            try:
                ydl.download([url])
            except Exception as e:
                if callback_progreso:
                    callback_progreso(0, f"Error: {e}", index, len(urls))
