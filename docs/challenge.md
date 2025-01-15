VERSION DE PYTHON UTILIZADO: 3.9.21
## Part1
* ejecucion de book
* realice correccion al momento de plotear los datos, faltaba especificar los ejes.
* modelo seleccionado: XGBClassifier con balanceo de datos y con top 10 de features
* * si bien este modelo entrega el mejor resultado para el ejercicio, los features utilizados estan orientados a cierto tipo de aerolinea y meses en especifico, podria estar sesgado para algunas predicciones.
* * este modelo esta limitado a que los datos de entrenamiento sean siempre los mismos, debido a el top 10 de features seleccionados(si no existen las columnas, se caera al momento de obtener los features-preprocess).
* * Seleccione el balanceo de los datos debido a la cantidad de data para delay 0 es mucho menor que para 1, generando una precicion muy baja.
* * seleccione XGBClassifier debido a la cantidad de datos, el mejor manejo para el balanceo y mejor pronostico para variables relacionadas no linealmente.

## Part2
* cree modelo para uso de api y modifique el archivo api para mantener el modelo en memoria.
* cree modelAPI para mejor manejo de validacion de data y uso de prediccion.
* cree modeloPrediccion para el manejo de entrada de datos para fastapi

## Part 3
* Cree archivo dockerfile para generar contenedor de api
* compilacion: docker build -t lmlatam .
* run: docker run -d -p 8000:8000 lmlatam
* monte contenedor en gcp a traves de cloud run
* url: https://mllatam-379742316336.us-central1.run.app