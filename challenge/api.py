import fastapi
import challenge.modelAPI as modelAPI
import challenge.modeloPrediccion as modeloPrediccion
import pandas as pd


"""creo modelo con dato base y lo dejo entrenado para el acceso desde api"""
data = pd.read_csv(filepath_or_buffer="./data/data.csv")
modelo = modelAPI.DelayAPI(data)


app = fastapi.FastAPI()

@app.get("/health", status_code=200)
async def get_health() -> dict:
    return {
        "status": "OK"
    }

@app.post("/predict", status_code=200)
async def post_predict(solicitud: modeloPrediccion.SolicitudVuelos) -> dict:

    """Validar que los datos para prediccion esten dentro del ambito del modelo"""
    if len(solicitud.flights) == 0:
        raise fastapi.HTTPException(status_code=400, detail="La lista de vuelos no puede estar vacía.")
    resp=[]
    try:
        """Recorro listado"""
        for vuelo in solicitud.flights:
            """Valido data"""
            modelo.validateData(vuelo.OPERA,vuelo.TIPOVUELO,vuelo.MES)
            """formateo para predcir"""
            formated=modelo.formatPredict(vuelo.OPERA,vuelo.TIPOVUELO,vuelo.MES)
            result=modelo.predict(formated)
            """Concateno resultado"""
            resp.append(result)

    except ValueError as e:
        # Si ocurre un ValueError, capturamos y retornamos el error
        raise fastapi.HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        # Si ocurre otro tipo de error, capturamos y retornamos un error genérico
        raise fastapi.HTTPException(status_code=500, detail="Error interno del servidor")

    return {
        "predict": resp
        }