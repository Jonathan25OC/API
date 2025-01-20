from flask import Flask, render_template, jsonify
import os
import nbformat
from nbconvert import HTMLExporter

app = Flask(__name__)

# Ruta a la carpeta donde están los notebooks
NOTEBOOK_FOLDER = "notebooks"

# Función para listar los notebooks en la carpeta
def get_notebooks():
    try:
        return [
            f for f in os.listdir(NOTEBOOK_FOLDER)
            if f.endswith(".ipynb")
        ]
    except Exception as e:
        print(f"Error al listar notebooks: {str(e)}")
        return []

# Función para cargar un notebook y convertirlo a HTML
def convert_notebook_to_html(notebook_path):
    try:
        # Leer el archivo del notebook
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook_content = nbformat.read(f, as_version=4)

        # Usar nbconvert para convertir el notebook a HTML
        html_exporter = HTMLExporter()
        body, _ = html_exporter.from_notebook_node(notebook_content)
        
        return body
    except Exception as e:
        print(f"Error al convertir el notebook {notebook_path}: {str(e)}")
        return None

@app.route('/')
def index():
    notebooks = get_notebooks()
    return render_template('index.html', notebooks=notebooks)

@app.route('/notebook/<notebook_name>')
def view_notebook(notebook_name):
    notebook_path = os.path.join(NOTEBOOK_FOLDER, notebook_name)

    try:
        # Convertir el notebook a HTML
        notebook_html = convert_notebook_to_html(notebook_path)
        if notebook_html:
            return render_template('notebook_viewer.html', notebook_html=notebook_html)
        else:
            return jsonify({"error": "No se pudo convertir el notebook"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
