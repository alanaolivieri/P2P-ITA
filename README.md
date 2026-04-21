# P2P and Activities ITA

Este proyecto muestra de forma clara y actualizada **quién está habilitado para realizar el P2P** dentro del itinerario de **Data Analytics – IT Academy** y la **Organización de las Actividades** que se realizarán en las aulas a 30 días.

La información se obtiene a partir de los archivos corporativos de calificaciones y se presenta mediante una **[aplicación Streamlit](https://p2p-ita-dataanalytics.streamlit.app/)** de solo lectura que se actualiza automáticamente de forma diaria a inicio de la mañana.

---

## Objetivos

- Mostrar el **estado de habilitación P2P** de estudiantes y mentores
- Dar a conocer las actividades planteadas en las aulas
- Garantizar que la información esté **siempre actualizada**
- Cumplir con las **restricciones de seguridad corporativas**
- Ofrecer una visualización clara, filtrable y ordenable

---

## Estructura del proyecto

```text
P2P-ITA/
│
├── README.md                # Documentación principal del proyecto
├── .gitignore               # Exclusión de archivos sensibles
│
├── data/
|   ├── actividades.xlsx     # Excel generado automáticamente (lectura)
|   ├── infografia.jpg       # Imagen generada automáticamente (lectura)
│   └── p2p_latest.xlsx      # Excel generado automáticamente (lectura)
│
├── src/
|   ├── app.py               # Aplicación Streamlit
│   └── sync_p2p_excel.py    # Script de sincronización desde OneDrive
│
└── requirements.txt         # Librerías a instalar necesarias para ejecutar
```
---

## Ejecución

En el .env deben existir las siguientes variables

`ORIGEN`: es el path donde se encuentra el archivo origen que consume los datos del p2p
`ORGANIZACION`: es el path donde se encuentra el archivo origen que consume los datos para las actividades
`INFOGRAFIA`: es el path donde se encuentra la imagen de origen que muestra la organización y rotación
`REPO`: es el path donde se crean los excel dentro de la carpeta data de este repositorio

### Sincronización

- Programar una tarea de windows que monte el environment, ejecute el sincronizador de los datos y cargue a github

### Ejecución manual

- Crear un entorno virtual (recomendado)

Desde una terminal:

```bash
py -3.11 -m venv sync_env
```

- Instalar dependencias
```bash
sync_env\Scripts\python.exe -m pip install -r requirements_sync.txt
```

- Configurar variables de entorno

Crear un archivo .env en la misma carpeta que el script:
```env
ORIGEN="C:/ruta/al/excel/original/datos/p2p.xlsx"
ORGANIZACION="C:/ruta/al/excel/original/datos/organizacion.xlsx"
INFOGRAFIA="C:/ruta/a/imagen/original/infografia.jpg"
REPO="C:/ruta/al/repositorio/P2P-ITA"
```
- Ejecutar la sincronización manualmente
```bash
sync_env\Scripts\python.exe sync_p2p_excel.py
```