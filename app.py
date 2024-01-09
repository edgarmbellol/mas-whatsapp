from flask import Flask, render_template, request, session
import pandas as pd
import pywhatkit
import os

app = Flask(__name__)
app.secret_key = 'Sopo2023*'

@app.route("/")
def hello_world():
    return render_template('index.html')

# FUNCION PARA LEER LOS ENCABEZADOS DEL ARCHIVO EXCEL
def leer_encabezados(archivo_excel):
    # Lee solo las primeras filas del archivo Excel
    encabezados = pd.read_excel(archivo_excel, nrows=1).columns.tolist()
    # Guarda los encabezados en la session
    session['encabezados'] = encabezados

    return encabezados

# FUNCION PARA ENVIAR MENSAJE WHATSAPP
def tomar_info():
    # Recupera los encabezados del archivo excel
    encabezados = session['encabezados']
    # Tomar nombre del archivo de la sesion
    nombreArchivo = session['nombreArchivo']
    # Tomar informacion de columnas 
    df = pd.read_excel(nombreArchivo)
    # Crear un diccionario vacío
    info = {}
    # Guarda en un diccionario con su clave correspondiente la info de la columna
    for columna in encabezados:
        info[str(columna)] = df[str(columna)].tolist()
    # print(info['Profesional'][0])

    return info

def eliminar_archivo():
    # Tomar nombre del archivo de la sesion
    nombreArchivo = session['nombreArchivo']
    # Eliminar archivo 
    os.remove(nombreArchivo)
    return

# ESTA SECCION PROCESA EL ARCHIVO EN EXCEL
@app.route("/mensaje",methods=['POST'])
def carga():
    if 'file' not in request.files:
        return "No se seleccionó ningún archivo."

    file = request.files['file']
    ruta_archivo = file.filename
    session['nombreArchivo'] = ruta_archivo

    if file.filename == '':
        return "No se seleccionó ningún archivo."

    if file:
        # Aquí puedes procesar el archivo en el lado del servidor (parsing, manipulación, etc.)
        # En este ejemplo, simplemente imprimimos el contenido del archivo
        
        # Guardar archvo excel de forma temporal
        file.save(ruta_archivo)
        
        # SE TRAEN LOS ENCABEZADOS DEL DOCUMENTO 
        encabezados = leer_encabezados(file)

        return render_template('mensaje.html',encabezados=encabezados)

# AQUI ENTRA EL MENSAJE DE WHATSAPP QUE SE DESA ENVIAR Y EL ARCHIVO DE EXCEL
@app.route("/enviar",methods=['POST'])
def enviar():
    if request.method == 'POST':
        texto = request.form['mensaje'] # Toma el valor del mensaje
        # OBTENER INFORMACION DE LAS COLUMNAS
        info = tomar_info()
        encabezados = session['encabezados']

        # Formatear mensaje
        for index,numero in enumerate(info['Numeros']):
            if request.method == 'POST':
                print('ingrese al post interior')
            msj = texto
            for enca in encabezados:
                buscar = "{"+str(enca)+"}"
                remplazar = str(info[str(enca)][index])
                msj = msj.replace(buscar,remplazar)

            numero = '+57' + str(numero)
            # print(numero)
            # Enviar mensaje
            pywhatkit.sendwhatmsg_instantly(numero,msj,16,True,3)
            print (msj)
        # Eliminar archivo de excel para liberar memoria
        eliminar_archivo()
        return 'Ya entre a la pagina enviar'

if __name__=='__main__':
    app.run(debug='true')