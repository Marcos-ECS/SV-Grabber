import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import threading
import os
from downloader import descargar_video

carpeta_destino = os.getcwd()  # Carpeta por defecto

def seleccionar_carpeta():
    global carpeta_destino
    carpeta = filedialog.askdirectory()
    if carpeta:
        carpeta_destino = carpeta
        ruta_carpeta.set(f"📂 Carpeta destino: {carpeta}")

def iniciar_descarga():
    url = entrada_url.get().strip()
    if not url:
        messagebox.showwarning("Advertencia", "Por favor, ingresa una URL de Twitter.")
        return

    calidad = combo_calidad.get()
    if calidad not in ["Máxima calidad", "Descarga rápida"]:
        messagebox.showwarning("Advertencia", "Selecciona una opción de calidad.")
        return

    boton_descargar.config(state=tk.DISABLED)
    estado.set("⏳ Iniciando descarga...")
    barra['value'] = 0

    def callback_progreso(porcentaje, etapa):
        barra['value'] = porcentaje
        estado.set(f"{etapa} - {porcentaje:.1f}%")
        ventana.update_idletasks()

    def tarea():
        try:
            descargar_video(
                url,
                carpeta_destino,
                callback_progreso,
                calidad="maxima" if calidad == "Máxima calidad" else "rapida"
            )
            estado.set("✅ Descarga completada.")
        except Exception as e:
            estado.set("❌ Error en la descarga.")
            messagebox.showerror("Error", str(e))
        finally:
            boton_descargar.config(state=tk.NORMAL)

    threading.Thread(target=tarea).start()

# --- GUI ---
ventana = tk.Tk()
ventana.title("SV-Grabber")
ventana.geometry("550x450")

tk.Label(ventana, text="Ingresa la URL del tweet con video:").pack(pady=10)

entrada_url = tk.Entry(ventana, width=65)
entrada_url.pack(pady=5)

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

# Barra de progreso
barra = ttk.Progressbar(ventana, orient="horizontal", length=450, mode="determinate")
barra.pack(pady=15)

estado = tk.StringVar()
estado.set("Esperando URL...")
tk.Label(ventana, textvariable=estado, fg="blue").pack(pady=10)

ventana.mainloop()
