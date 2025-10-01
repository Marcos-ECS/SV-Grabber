import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import threading
import os
from downloader import descargar_videos

carpeta_destino = os.getcwd()
barras = []  
labels = []  
lista_detectada = []  

def seleccionar_carpeta():
    global carpeta_destino
    carpeta = filedialog.askdirectory()
    if carpeta:
        carpeta_destino = carpeta
        ruta_carpeta.set(f"📂 Carpeta destino: {carpeta}")

def validar_urls():
    global lista_detectada
    raw_urls = entrada_urls.get("1.0", tk.END).strip()
    urls = raw_urls.replace("\n", " ").split()
    lista_detectada = urls

    # limpiar frame previo
    for widget in frame_validacion.winfo_children():
        widget.destroy()

    if not urls:
        tk.Label(frame_validacion, text="⚠️ No se detectaron URLs.", fg="red").pack()
    else:
        tk.Label(frame_validacion, text="✅ Links detectados:", fg="green").pack(anchor="w")
        for i, url in enumerate(urls, start=1):
            tk.Label(frame_validacion, text=f"[{i}] {url}", fg="blue", anchor="w", justify="left").pack(anchor="w")

def iniciar_descarga():
    global barras, labels
    if not lista_detectada:
        messagebox.showwarning("Advertencia", "Primero valida los links para continuar.")
        return

    urls = lista_detectada
    calidad = combo_calidad.get()
    if calidad not in ["Máxima calidad", "Descarga rápida"]:
        messagebox.showwarning("Advertencia", "Selecciona una opción de calidad.")
        return

    # limpiar descargas previas
    for widget in frame_descargas.winfo_children():
        widget.destroy()
    barras, labels = [], []

    # crear barra + label por cada URL
    for i, url in enumerate(urls, start=1):
        lbl = tk.Label(frame_descargas, text=f"[{i}/{len(urls)}] Esperando...")
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
                calidad="maxima" if calidad == "Máxima calidad" else "rapida"
            )
            messagebox.showinfo("Finalizado", "✅ Todas las descargas completadas.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            boton_descargar.config(state=tk.NORMAL)

    threading.Thread(target=tarea).start()

# --- GUI ---
ventana = tk.Tk()
ventana.title("Descargador Multi-Plataforma")
ventana.geometry("700x700")

tk.Label(ventana, text="Ingresa las URLs (separadas por espacio o salto de línea):").pack(pady=10)

entrada_urls = tk.Text(ventana, width=80, height=6)
entrada_urls.pack(pady=5)

# Botón validar
tk.Button(ventana, text="Validar links", command=validar_urls).pack(pady=5)

# Frame para mostrar URLs detectadas
frame_validacion = tk.Frame(ventana, relief="groove", borderwidth=2)
frame_validacion.pack(pady=5, fill="x")

# Selección de calidad
tk.Label(ventana, text="Selecciona la calidad:").pack(pady=5)
combo_calidad = ttk.Combobox(ventana, values=["Máxima calidad", "Descarga rápida"], state="readonly")
combo_calidad.set("Máxima calidad")
combo_calidad.pack(pady=5)

boton_descargar = tk.Button(ventana, text="Descargar", command=iniciar_descarga)
boton_descargar.pack(pady=10)

# Carpeta destino
ruta_carpeta = tk.StringVar()
ruta_carpeta.set(f"📂 Carpeta destino: {carpeta_destino}")
tk.Label(ventana, textvariable=ruta_carpeta, fg="green").pack(pady=5)
tk.Button(ventana, text="Cambiar carpeta", command=seleccionar_carpeta).pack(pady=5)

# Frame para barras dinámicas
frame_descargas = tk.Frame(ventana)
frame_descargas.pack(pady=10, fill="x")

ventana.mainloop()
