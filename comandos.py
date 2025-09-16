# comandos.py

class RobocopyFlags:
    # ============================================
    # COPIA DE ARCHIVOS Y DIRECTORIOS
    # ============================================

    COPY_SUBDIRS = "/E"                 # Copia subdirectorios, incluso vacíos
    COPY_SUBDIRS_NEMPTY = "/S"          # Copia subdirectorios, excluye los vacíos
    MIRROR = "/MIR"                     # Copia espejo (borra en destino lo que no existe en origen)
    CREATE_STRUCTURE_ONLY = "/CREATE"   # Crea estructura de carpetas y archivos vacíos (sin contenido)
    COPY_FLAGS = "/COPY:DATSO"          # Copia Datos, Atributos, Tiempos, Seguridad, y Propietario
    DCOPY_TIME = "/DCOPY:T"             # Copia fechas y atributos de carpetas

    # ============================================
    # RESTAURACIÓN / SINCRONIZACIÓN SEGURA
    # ============================================

    PURGE = "/PURGE"                    # Elimina archivos del destino que ya no existen en el origen
    EXCLUDE_EXTRA = "/XX"               # Excluye archivos "extra" en destino
    EXCLUDE_SAME = "/XC"                # Excluye archivos sin cambios
    EXCLUDE_CHANGED = "/X"              # Excluye archivos modificados
    EXCLUDE_NEWER = "/XN"               # Excluye archivos más nuevos en origen
    EXCLUDE_OLDER = "/XO"               # Excluye archivos más antiguos en origen

    # ============================================
    # FILTROS / EXCLUSIONES
    # ============================================

    EXCLUDE_FILES = "/XF"               # Excluir archivos por nombre/patrón
    EXCLUDE_DIRS = "/XD"                # Excluir carpetas por nombre/patrón
    MAXAGE = "/MAXAGE:"                 # Copia archivos modificados en los últimos N días
    MINAGE = "/MINAGE:"                 # Copia archivos más antiguos de N días
    MAXSIZE = "/MAX:"                   # Copia archivos menores a X bytes
    MINSIZE = "/MIN:"                   # Copia archivos mayores a X bytes

    # ============================================
    # RENDIMIENTO / CONCURRENCIA
    # ============================================

    MULTITHREAD = "/MT:16"              # Copia usando 16 hilos (ajustable)
    RETRIES = "/R:3"                    # Reintentos por archivo fallido
    WAIT = "/W:5"                       # Espera entre reintentos (segundos)
    FILE_TIME_TOLERANCE = "/FFT"        # Tolerancia de tiempo para FAT/NTFS

    # ============================================
    # SALIDA / LOGS / VERBOSIDAD
    # ============================================

    NO_PROGRESS = "/NP"                # No mostrar progreso de cada archivo
    NO_FILE_LIST = "/NFL"              # No mostrar lista de archivos copiados
    NO_DIR_LIST = "/NDL"               # No mostrar lista de directorios copiados
    TEE = "/TEE"                       # Muestra salida en consola además de log
    LOG = "/LOG:"                      # Log de salida a archivo (ej: /LOG:backup.log)
    LOG_APPEND = "/LOG+:"              # Añadir al log existente en lugar de sobrescribir

    # ============================================
    # SIMULACIÓN / PRUEBAS
    # ============================================

    LIST_ONLY = "/L"                   # Simula (no copia), solo muestra lo que haría

    # ============================================
    # ENLACES / ATRIBUTOS ESPECIALES
    # ============================================

    EXCLUDE_JUNCTIONS = "/XJ"          # Excluye puntos de unión (junctions)
    COPY_LINKS = "/SL"                 # Copia los archivos apuntados por enlaces simbólicos
