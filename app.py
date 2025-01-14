from flask import Flask, render_template, jsonify
import nbformat
from nbconvert import HTMLExporter

app = Flask(__name__)

# Suponiendo que tienes una lista de notebooks
notebooks = ["01_Numpy_3501.ipynb","2.1_Suport_Vector_Machine_3501.ipynb","3501_Creacion_de_Transformadores_y_Pipelines_Personalizados.ipynb","3501_Evaluacion-de-Resultados.ipynb",
             "3501_Matplotlib.ipynb","3501_Pandas.ipynb","3501_Preparacion-del-DataSet.ipynb","3501_Regresion_Lineal.ipynb","3501_SVM.ipynb","3501_Visualizacion-de-Datos.ipynb","Arboles_de_Decision.ipynb","Regresion_Logistica.ipynb",
             "Regresion_logistica_Diabetes.ipynb"]
# Función para cargar un notebook y convertirlo a HTML
def convert_notebook_to_html(notebook_path):
    try:
        # Leer el archivo del notebook
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook_content = nbformat.read(f, as_version=4)

        # Usar nbconvert para convertir el notebook a HTML
        html_exporter = HTMLExporter()
        body, resources = html_exporter.from_notebook_node(notebook_content)
        
        return body
    except Exception as e:
        print(f"Error al convertir el notebook {notebook_path}: {str(e)}")
        return None

@app.route('/')
def index():
    return render_template('index.html', notebooks=notebooks)

@app.route('/notebook/<notebook_name>')
def view_notebook(notebook_name):
    # Aquí puedes elegir cómo obtener el archivo del notebook
    notebook_path = f"notebooks/{notebook_name}"

    try:
        # Convertir el notebook a HTML
        notebook_html = convert_notebook_to_html(notebook_path)
        return render_template('notebook_viewer.html', notebook_html=notebook_html)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
