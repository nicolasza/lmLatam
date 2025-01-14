from challenge.model import DelayModel
import pandas as pd

from typing import List

class DelayAPI:

    """extraido de los datos originales"""
    ambito_OPERA=['American Airlines', 'Air Canada', 'Air France', 'Aeromexico',
        'Aerolineas Argentinas', 'Austral', 'Avianca', 'Alitalia', 'British Airways',
        'Copa Air', 'Delta Air', 'Gol Trans', 'Iberia', 'K.L.M.', 'Qantas Airways',
        'United Airlines', 'Grupo LATAM', 'Sky Airline', 'Latin American Wings',
        'Plus Ultra Lineas Aereas', 'JetSmart SPA', 'Oceanair Linhas Aereas',
        'Lacsa']

    """extraido de los datos originales"""
    ambito_tipoVuelo=[
        "I",
        "N"
    ]


    def __init__(
        self,
        data:pd.DataFrame
    ):
        """Cargo modelo y data"""
        self.model = DelayModel()
        self.data = data
        
        """Preproceso datos"""
        features, target = self.model.preprocess(
            data=self.data,
            target_column="delay"
        )

        """Ajusto Modelo"""
        self.model.fit(features=features,target=target)

    def validateData(
        self,
        OPERA: str,
        TIPOVUELO: str,
        MES: int 
    ) -> bool:
        
        """Verificar si esta OPERA DENTRO DE AMBITO"""
        if not OPERA in self.ambito_OPERA:
            """Lanza una excepción si no se encuentra"""
            raise ValueError(f"El dato OPERA '{OPERA}' no esta dentro del ambito.")
        
        """Verificar si esta OPERA DENTRO DE AMBITO"""
        if not TIPOVUELO in self.ambito_tipoVuelo:
            """Lanza una excepción si no se encuentra"""
            raise ValueError(f"El dato TIPOVUELO '{TIPOVUELO}' no esta dentro del ambito.")
        
        """Verifica el mes"""
        if MES<1 or MES>12:
            raise ValueError(f"El dato MES '{MES}' no esta dentro del ambito")
        
        return True

    def formatPredict(
        self,
        OPERA: str,
        TIPOVUELO: str,
        MES: int 
    ) -> pd.DataFrame:

        """Verifica la data"""
        if(self.validateData(OPERA,TIPOVUELO,MES)):
            # Inicializa un diccionario vacío para la fila
            fila = {}

            """Verificar cada una de las columnas de top_features"""
            for feature in self.model.top_features:
                if feature.startswith("OPERA_"):
                    """Comprobar si la aerolínea coincide con la columna"""
                    aerolinea = feature.replace("OPERA_", "")  # Extrae la aerolínea
                    fila[feature] = (OPERA == aerolinea)  # Setea True o False

                elif feature.startswith("MES_"):
                    """Extraer el número de mes de la columna y comprobar si coincide"""
                    mes = int(feature.split("_")[1])  # Extrae el número del mes
                    fila[feature] = (MES == mes)  # Setea True o False

                elif feature.startswith("TIPOVUELO_"):
                    """Comprobar si el tipo de vuelo coincide"""
                    tipo_vuelo = feature.replace("TIPOVUELO_", "")  # Extrae el tipo de vuelo
                    fila[feature] = (TIPOVUELO == tipo_vuelo)  # Setea True o False

            # Crear el DataFrame con una sola fila
            df_boolean = pd.DataFrame([fila], columns=self.model.top_features)

            # Asegurarse de que todas las columnas sean de tipo booleano
            df_boolean = df_boolean.astype(bool)
            return df_boolean
        
        return None

    def predict(
        self,
        features: pd.DataFrame
    ) -> List[int]:
        
        """Comparo si existen las columnas necesarias"""
        if set(features.columns) == set(self.model.top_features):
           return self.model.predict(features).tolist()[0] # ajuste de formato para el retorno
        else:
            raise ValueError("No coinciden las columnas")
