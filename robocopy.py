import os, sys, threading, subprocess, shutil, tempfile
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox, ttk
from tkinter.scrolledtext import ScrolledText
from cryptography.fernet import Fernet
from comandos import RobocopyFlags
from estilos import Estilos, estilo_botones_tk
from tooltip import ToolTip


WIN = os.name == "nt"

BASE_ARGS = ["/COPY:DATSO", "/DCOPY:T", "/R:3", "/W:5", "/MT:16", "/FFT", "/XJ", "/NP", "/TEE"]

def which_robocopy():
    return shutil.which("robocopy.exe") or shutil.which("robocopy")

def build_cmd(src, dst, *extra):
    return ["robocopy", src, dst, *BASE_ARGS, *extra]

def run_in_thread(func):
    def wrapper(*a, **kw):
        t = threading.Thread(target=func, args=a, kwargs=kw, daemon=True)
        t.start()
    return wrapper

def generate_and_save_key(key_path):
    key = Fernet.generate_key()
    with open(key_path, "wb") as f:
        f.write(key)
    return key

def load_key(key_path):
    with open(key_path, "rb") as f:
        return f.read()

def encrypt_folder_to_file(folder_path, out_dir, key_path=None):
    """
    Comprime la carpeta a ZIP y cifra el ZIP con Fernet.
    Devuelve ruta del .enc y del .key (si se generó).
    """
    os.makedirs(out_dir, exist_ok=True)
    base_name = os.path.basename(os.path.normpath(folder_path)) or "backup"
    zip_path = os.path.join(tempfile.gettempdir(), f"{base_name}.zip")
    enc_path = os.path.join(out_dir, f"{base_name}.zip.enc")

    # Crear ZIP temporal
    if os.path.exists(zip_path):
        os.remove(zip_path)
    shutil.make_archive(zip_path[:-4], "zip", folder_path)

    # Cargar o generar clave
    key_created = False
    if not key_path:
        key_path = os.path.join(out_dir, f"{base_name}.key")
    if not os.path.exists(key_path):
        key = generate_and_save_key(key_path)
        key_created = True
    else:
        key = load_key(key_path)

    # Cifrar
    f = Fernet(key)
    with open(zip_path, "rb") as zf:
        data = zf.read()
    token = f.encrypt(data)
    with open(enc_path, "wb") as ef:
        ef.write(token)

    # Limpiar ZIP temporal
    try:
        os.remove(zip_path)
    except OSError:
        pass

    return enc_path, (key_path if key_created else None)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        Estilos(self)
        self.title("Valkyria")
        self.geometry("1280x720")
        # Crear pestañas (notebook)
        notebook = ttk.Notebook(self)
        notebook.pack(padx=10, pady=10, fill="x")

        # Estilo común para botones
        style = estilo_botones_tk()
        

        # --- Pestaña: Copias ---
        frame_copias = tk.Frame(notebook, bg="black")
        notebook.add(frame_copias, text="Copias")

        btnSimple = tk.Button(frame_copias, text="Simple", command=self.simple_copy, **style)
        btnSimple.grid(row=0, column=0, padx=6, pady=6) 
        ToolTip(btnSimple, "Copia simple de directorios: {Origen} - {Destino}")

        btnSubdirectory = tk.Button(frame_copias, text="Subdirectorios (salvo vacíos)", command=self.subdirectory_copy, **style)
        btnSubdirectory.grid(row=0, column=1, padx=6, pady=6) 
        ToolTip(btnSubdirectory, "Copia de subdirectorios salvo los vacíos: {Origen} - {Destino} /S")

        btnSubdirectoryIncl = tk.Button(frame_copias, text="Subdirectorios (incluído vacíos)", command=self.subdirectory_copy, **style)
        btnSubdirectoryIncl.grid(row=0, column=2, padx=6, pady=6) 
        ToolTip(btnSubdirectoryIncl, "Copia de subdirectorios salvo los vacíos: {Origen} - {Destino} /E")

        btnIncrementalNoPurge = tk.Button(frame_copias, text="Incremental Sin Borrado Excluye Ant.", command=self.copia_incremental, **style)
        btnIncrementalNoPurge.grid(row=0, column=3, padx=6, pady=6)
        ToolTip(btnIncrementalNoPurge, "Copia incremental sin borrar archivos: {Origen} - {Destino} /E /XO")

        btnMirror = tk.Button(frame_copias, text="Espejo", command=self.copia_mirror, **style)
        btnMirror.grid(row=1, column=0, padx=6, pady=6)
        ToolTip(btnMirror, "Copia espejo (borra en destino lo que no existe en origen): {Origen} - {Destino} /MIR")

        btnSinceDate = tk.Button(frame_copias, text="A partir de fecha", command=self.copia_recientes, **style)
        btnSinceDate.grid(row=1, column=1, padx=6, pady=6)
        ToolTip(btnSinceDate, "Copia a partir de una cantidad de días: {Origen} - {Destino} /E  /MAXAGE:{días}")

        btnCreateStructure = tk.Button(frame_copias, text="Crear estructura", command=self.create_structure, **style)
        btnCreateStructure.grid(row=1, column=2, padx=6, pady=6)
        ToolTip(btnCreateStructure, "Copia simplemente la estructura de carpetas: {Origen} - {Destino} /CREATE")
        

        # --- Pestaña: Restaurar ---
        frame_restore = tk.Frame(notebook, bg="black")
        notebook.add(frame_restore, text="Restaurar")

        btnIncrementalNoPurge = tk.Button(frame_restore, text="Restaurar", command=self.copia_incremental, **style)
        btnIncrementalNoPurge.grid(row=0, column=1, padx=6, pady=6)
        ToolTip(btnIncrementalNoPurge, "Copia incremental sin borrar archivos: {Origen} - {Destino} /E /XO")

        btnPurge = tk.Button(frame_restore, text="Purgar", command=self.purge_destination, **style)
        btnPurge.grid(row=0, column=2, padx=6, pady=6)
        ToolTip(btnPurge, "Elimina archivos del destino que ya no existen en el origen: {Origen} - {Destino} /PURGE")



        # --- Pestaña: Avanzado ---
        frame_avanzado = tk.Frame(notebook, bg="black")
        notebook.add(frame_avanzado, text="Avanzado")

        tk.Button(frame_avanzado, text="Purgar", command=self.purge_destination, **style).grid(row=0, column=0, padx=6, pady=6)
        tk.Button(frame_avanzado, text="Otro", command=self.purge_destination, **style).grid(row=0, column=1, padx=6, pady=6)

        # --- Pestaña: Salir ---
        frame_salir = tk.Frame(notebook, bg="black")
        notebook.add(frame_salir, text="Salir")

        tk.Button(frame_salir, text="Salir", command=self.destroy, **style).grid(row=0, column=0, padx=6, pady=6)

        # Log
        self.log = ScrolledText(self, height=28, bg="#111", fg="#ddd", insertbackground="white")
        self.log.pack(fill="both", expand=True, padx=10, pady=10)
        self.log.tag_config("err", foreground="#ff6666")
        self.log.tag_config("ok", foreground="#66ff99")
        self.log.tag_config("cmd", foreground="#66aaff")

        # Comprobaciones
        if not WIN:
            self.append("Este programa está pensado para Windows (Robocopy).\n", "err")
        if not which_robocopy():
            self.append("No encuentro robocopy en PATH. ¿Estás en Windows? ¿Está disponible?\n", "err")

    def ask_src_dst(self, title_src="Selecciona carpeta de ORIGEN", title_dst="Selecciona carpeta de DESTINO"):
        src = filedialog.askdirectory(title=title_src)
        if not src: return None, None
        dst = filedialog.askdirectory(title=title_dst)
        if not dst: return None, None
        return src, dst
    
    def validator(self, src, dst):
        #Validamos que no estén vacío el string de origen y destino
        if not src or not dst:
            print("Error: ruta de origen o destino vacía")
            return
        #Validamos que el origen exista dentro del sistema de archivos y no sea una ruta falsa (el destino se crea si no existe)
        if not os.path.exists(src):
            print(f"Error: el directorio origen no existe: {src}")
            return
        
    def append(self, text, tag=None):
        self.log.insert("end", text, tag)
        self.log.see("end")
        self.update_idletasks()

    @run_in_thread
    def run_cmd(self, cmd):
        self.append("\n$ " + subprocess.list2cmdline(cmd) + "\n", "cmd")
        try:
            # Popen para no bloquear la UI y stream de salida
            with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1) as p:
                for line in p.stdout:
                    self.append(line)
            rc = p.wait()
            msg = f"\n[RC={rc}] {'OK (<8)' if rc < 8 else 'FALLO (>=8)'}\n"
            self.append(msg, "ok" if rc < 8 else "err")
        except Exception as e:
            self.append(f"\nERROR: {e}\n", "err")

    def confirm_mirror(self, src, dst):
        return messagebox.askyesno(
            "Confirmar /MIR",
            f"Vas a ejecutar un ESPEJO (/MIR):\n\nORIGEN: {src}\nDESTINO: {dst}\n\n"
            "Esto BORRARÁ en destino lo que no exista en origen.\n\n¿Continuar?"
        )

    def copia_mirror(self):
        src, dst = self.ask_src_dst()
        if not src or not dst: return
        if not self.confirm_mirror(src, dst): return
        cmd = build_cmd(src, dst, "/MIR")
        self.run_cmd(cmd)

    def copia_incremental(self):
        src, dst = self.ask_src_dst()
        if not src or not dst: return
        # /E (con vacías) + /XO (excluir más antiguos) → copia más nuevos/cambiados, NO borra
        cmd = build_cmd(src, dst, "/E", "/XO")
        self.run_cmd(cmd)

        # Cifrar copia (opcional)
        if messagebox.askyesno("Cifrar copia", "¿Quieres cifrar la copia en un archivo .enc (ZIP + Fernet) en el DESTINO?"):
            try:
                enc_path, key_created = encrypt_folder_to_file(dst, out_dir=dst)
                self.append(f"\nCopia cifrada en: {enc_path}\n", "ok")
                if key_created:
                    self.append(f"Clave guardada en: {key_created}\nGuárdala en lugar seguro.\n", "ok")
            except Exception as e:
                self.append(f"\nERROR cifrando copia: {e}\n", "err")

    def copia_recientes(self):
        src, dst = self.ask_src_dst()
        if not src or not dst: return
        days = simpledialog.askinteger("Últimos N días", "¿Cuántos días hacia atrás (entero)?", minvalue=1, initialvalue=1)
        if not days: return
        # /MAXAGE:n excluye archivos más viejos que n → solo recientes
        cmd = build_cmd(src, dst, "/E", f"/MAXAGE:{days}")
        self.run_cmd(cmd)

    def restore(self):
        # Restaurar SIN BORRAR (seguro): /E /XO (no pisa con más antiguos)
        backup, target = self.ask_src_dst("Selecciona carpeta de BACKUP", "Selecciona carpeta de DESTINO a restaurar")
        if not backup or not target: return
        cmd = build_cmd(backup, target, "/E", "/XO")
        self.run_cmd(cmd)

    def purge_destination(self):
        # Elimina archivos del destino que ya no existen en el origen.
        src, dst = self.ask_src_dst()
        self.validator(src, dst)
        cmd = build_cmd(src, dst, RobocopyFlags.PURGE)
        self.run_cmd(cmd)

    def simple_copy(self):
        # Hace una copia de archivos simple, sin meterse en subcarpetas
        src, dst = self.ask_src_dst()
        self.validator(src, dst)
        cmd = build_cmd(src, dst)
        self.run_cmd(cmd)
        
    def subdirectory_copy(self):
        # Hace una copia de archivos incluyendo subdirectorios pero no los vacíos
        self.validator(src, dst)
        cmd = build_cmd(src, dst, RobocopyFlags.COPY_SUBDIRS_NEMPTY)
        self.run_cmd(cmd)
    
    def subdirectory_copy_included(self):
        # Hace una copia de archivos incluyendo subdirectorios vacíos
        self.validator(src, dst)
        cmd = build_cmd(src, dst, RobocopyFlags.COPY_SUBDIRS)
        self.run_cmd(cmd)
    
    def create_structure(self):
        # Crea estructura de carpetas y archivos vacíos (sin contenido)
        self.validator(src, dst)
        cmd = build_cmd(src, dst, RobocopyFlags.CREATE_DIRS)
        self.run_cmd(cmd)
    


if __name__ == "__main__":
    app = App()
    app.mainloop()