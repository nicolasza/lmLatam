## Part1
* ejecucion de book
* realice correccion al momento de plotear los datos, faltaba especificar los ejes.
* modelo seleccionado: XGBClassifier con balanceo de datos y con top 10 de features
* * si bien este modelo entrega el mejor resultado para el ejercicio, los features utilizados estan orientados a cierto tipo de aerolinea y meses en especifico, podria estar sesgado para algunas predicciones.
* * Seleccione el balanceo de los datos debido a la cantidad de data para delay 0 es mucho menor que para 1, generando una precicion muy baja.
* * seleccione XGBClassifier debido a la cantidad de datos, el mejor manejo para el balanceo y mejor pronostico para variables relacionadas no linealmente.