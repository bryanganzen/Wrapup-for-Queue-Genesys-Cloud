# Wrapup-for-Queue-Genesys-Cloud
Este desarrollo otorga un excel con los id y nombre de wrapups de las queues buscadas en genesys cloud por organización

# Wrap-up Codes Downloader para Genesys Cloud

## Descripción

Esta aplicación web permite a los usuarios cargar un archivo Excel con IDs de colas (Queues) y obtener los códigos de finalización (Wrap-up Codes) asociados desde Genesys Cloud. Los resultados se pueden visualizar en una tabla y descargar en formato Excel.

### Características principales

- **Carga de Archivo Excel**: Permite cargar un archivo Excel con los IDs de las colas que se desean consultar.
- **Selección de Organización**: Los usuarios pueden seleccionar la organización correspondiente para filtrar los resultados de Genesys Cloud.
- **Visualización de Resultados**: Muestra una tabla con los códigos de finalización encontrados.
- **Descarga de Resultados**: Los resultados se pueden descargar en un archivo Excel para su análisis posterior.

## Requisitos

- Python 3.x
- Librerías necesarias (ver `requirements.txt`):
  - `Flask`
  - `pandas`
  - `openpyxl`
  - `PureCloudPlatformClientV2`
- Un entorno de Genesys Cloud configurado con permisos para acceder a las colas y sus códigos de finalización.

## Uso

- Inicia la aplicación Flask: `python app.py`
- Abre `http://localhost:5000` en tu navegador.
- En la página principal `index.html`:
  - Carga un archivo Excel con los IDs de las colas que deseas consultar.
  - Selecciona la organización correspondiente.
  - Haz clic en "Cargar" para obtener los códigos de finalización.
- Visualiza los resultados en la tabla y haz clic en "Descargar Wrap-up Codes en Excel" para obtener el archivo con los resultados.

## Estructura del Proyecto

- `app.py`: Script principal que maneja la lógica de la aplicación Flask y la integración con Genesys Cloud.
- `index.html`: Página principal donde se carga el archivo Excel y se selecciona la organización.
- `download.html`: Página de resultados donde se muestran los códigos de finalización y se permite la descarga.
- `example.xlsx`: Archivo de ejemplo que contiene el formato esperado para el archivo de carga.
- `requirements.txt`: Archivo de dependencias necesarias para el proyecto.

## Personalización

Puedes personalizar el estilo de la aplicación modificando los archivos CSS dentro de los archivos `index.html` y `download.html`.
Asegúrate de actualizar las credenciales y la configuración de la API en `app.py` para conectarte al entorno adecuado de Genesys Cloud.

## Contacto

Si tienes alguna pregunta o sugerencia, no dudes en ponerte en contacto.

- Bryan Ganzen
- 55 75 45 65 81
