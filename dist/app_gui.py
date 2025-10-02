import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import threading
import os
from downloader import descargar_videos
from i18n import t, set_language  # 👈 Importamos las traducciones

set_language("en")

carpeta_destino = os.getcwd()
barras = []  
labels = []  
lista_detectada = []  

def seleccionar_carpeta():
    global carpeta_destino
    carpeta = filedialog.askdirectory()
    if carpeta:
        carpeta_destino = carpeta
        ruta_carpeta.set(f"📂 {t('label_dest')} {carpeta}")

def validar_urls():
    global lista_detectada
    raw_urls = entrada_urls.get("1.0", tk.END).strip()
    urls = raw_urls.replace("\n", " ").split()
    lista_detectada = urls

    # limpiar frame previo
    for widget in frame_validacion.winfo_children():
        widget.destroy()

    if not urls:
        tk.Label(frame_validacion, text="⚠️ " + t("no_urls"), fg="red").pack()
    else:
        tk.Label(frame_validacion, text="✅ " + t("urls_detected"), fg="green").pack(anchor="w")
        for i, url in enumerate(urls, start=1):
            tk.Label(frame_validacion, text=f"[{i}] {url}", fg="blue", anchor="w", justify="left").pack(anchor="w")

def iniciar_descarga():
    global barras, labels
    if not lista_detectada:
        messagebox.showwarning(t("warning"), t("validate_first"))
        return

    urls = lista_detectada
    calidad = combo_calidad.get()
    if calidad not in [t("quality_max"), t("quality_fast")]:
        messagebox.showwarning(t("warning"), t("select_quality"))
        return

    # limpiar descargas previas
    for widget in frame_descargas.winfo_children():
        widget.destroy()
    barras, labels = [], []

    # crear barra + label por cada URL
    for i, url in enumerate(urls, start=1):
        lbl = tk.Label(frame_descargas, text=f"[{i}/{len(urls)}] {t('waiting')}")
        lbl.pack(pady=2, anchor="w")
        labels.append(lbl)

        pb = ttk.Progressbar(frame_descargas, orient="horizontal", length=500, mode="determinate")
        pb.pack(pady=2)
        barras.append(pb)

    boton_descargar.config(state=tk.DISABLED)

    def callback_progreso(porcentaje, etapa, index, total_urls):
        barras[index-1]['value'] = porcentaje
        labels[index-1].config(text=f"[{index}/{total_urls}] {etapa} - {porcentaje:.1f}%")
        ventana.update_idletasks()

    def tarea():
        try:
            descargar_videos(
                urls,
                carpeta_destino,
                callback_progreso,
                calidad="maxima" if calidad == t("quality_max") else "rapida"
            )
            messagebox.showinfo(t("done"), "✅ " + t("all_done"))
        except Exception as e:
            messagebox.showerror(t("error"), str(e))
        finally:
            boton_descargar.config(state=tk.NORMAL)

    threading.Thread(target=tarea).start()

# --- Función para refrescar textos ---
def refrescar_textos():
    ventana.title(t("title"))
    label_urls.config(text=t("label_urls"))
    boton_validar.config(text=t("button_validate"))
    label_calidad.config(text=t("label_quality"))
    combo_calidad.config(values=[t("quality_max"), t("quality_fast")])
    combo_calidad.set(t("quality_max"))
    boton_descargar.config(text=t("button_start"))
    ruta_carpeta.set(f"📂 {t('label_dest')} {carpeta_destino}")
    boton_carpeta.config(text=t("button_folder"))

# --- Cambio de idioma ---
def cambiar_idioma(event):
    lang = combo_lang.get()
    if lang == "Español":
        set_language("es")
    elif lang == "English":
        set_language("en")
    refrescar_textos()

# --- GUI ---
ventana = tk.Tk()
ventana.title(t("title"))
ventana.geometry("700x700")

# Menú idioma
combo_lang = ttk.Combobox(ventana, values=["Español", "English"], state="readonly")
combo_lang.current(1)
combo_lang.bind("<<ComboboxSelected>>", cambiar_idioma)
combo_lang.pack(pady=5)

label_urls = tk.Label(ventana, text=t("label_urls"))
label_urls.pack(pady=10)

entrada_urls = tk.Text(ventana, width=80, height=6)
entrada_urls.pack(pady=5)

boton_validar = tk.Button(ventana, text=t("button_validate"), command=validar_urls)
boton_validar.pack(pady=5)

frame_validacion = tk.Frame(ventana, relief="groove", borderwidth=2)
frame_validacion.pack(pady=5, fill="x")

label_calidad = tk.Label(ventana, text=t("label_quality"))
label_calidad.pack(pady=5)

combo_calidad = ttk.Combobox(ventana, values=[t("quality_max"), t("quality_fast")], state="readonly")
combo_calidad.set(t("quality_max"))
combo_calidad.pack(pady=5)

boton_descargar = tk.Button(ventana, text=t("button_start"), command=iniciar_descarga)
boton_descargar.pack(pady=10)

ruta_carpeta = tk.StringVar()
ruta_carpeta.set(f"📂 {t('label_dest')} {carpeta_destino}")
tk.Label(ventana, textvariable=ruta_carpeta, fg="green").pack(pady=5)

boton_carpeta = tk.Button(ventana, text=t("button_folder"), command=seleccionar_carpeta)
boton_carpeta.pack(pady=5)

frame_descargas = tk.Frame(ventana)
frame_descargas.pack(pady=10, fill="x")

ventana.mainloop()
