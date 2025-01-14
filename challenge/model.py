import pandas as pd
import xgboost as xgb
import numpy as np
from datetime import datetime

from typing import Tuple, Union, List

class DelayModel:

    variables_necesarias=['Fecha-O','Fecha-I','OPERA','TIPOVUELO','MES']

    top_features = [
    "OPERA_Latin American Wings", 
    "MES_7",
    "MES_10",
    "OPERA_Grupo LATAM",
    "MES_12",
    "TIPOVUELO_I",
    "MES_4",
    "MES_11",
    "OPERA_Sky Airline",
    "OPERA_Copa Air"
    ]

    threshold_in_minutes = 15

    def __init__(
        self
    ):
        self._model = None # Model should be saved in this attribute.

    def preprocess(
        self,
        data: pd.DataFrame,
        target_column: str = None
    ) -> Union[Tuple[pd.DataFrame, pd.DataFrame], pd.DataFrame]:
        """
        Prepare raw data for training or predict.

        Args:
            data (pd.DataFrame): raw data.
            target_column (str, optional): if set, the target is returned.

        Returns:
            Tuple[pd.DataFrame, pd.DataFrame]: features and target.
            or
            pd.DataFrame: features.
        """
        """Verifico columnas necesarias"""
        # Verificar si todas las columnas necesarias están en el DataFrame
        if not set(self.variables_necesarias).issubset(data.columns):
            # Lanza una excepción si falta alguna columna
            raise ValueError(f"Faltan las siguientes columnas: {set(self.variables_necesarias) - set(data.columns)}")
        
        """agrego campos necesario para pronostico"""
        data['min_diff'] = data.apply(self.get_min_diff, axis = 1)
        data['delay'] = np.where(data['min_diff'] > self.threshold_in_minutes, 1, 0)

        """Creo los features utilizados para el pronostico"""
        features = pd.concat([
        pd.get_dummies(data['OPERA'], prefix = 'OPERA'),
        pd.get_dummies(data['TIPOVUELO'], prefix = 'TIPOVUELO'), 
        pd.get_dummies(data['MES'], prefix = 'MES')], 
        axis = 1
        )
        top_features=features[self.top_features]

        if(target_column!=None):
            target = data[target_column]
            return (top_features,target)
        else:
            return top_features

    def fit(
        self,
        features: pd.DataFrame,
        target: pd.DataFrame
    ) -> None:
        """
        Fit model with preprocessed data.

        Args:
            features (pd.DataFrame): preprocessed data.
            target (pd.DataFrame): target.
        """
        """CEHQUEO QUE EXISTAN LAS FEATURES"""
        if not set(self.top_features).issubset(features.columns):
            # Lanza una excepción si falta alguna columna
            raise ValueError(f"Faltan las siguientes columnas: {set(self.top_features) - set(features.columns)}")
        
        """Calculo de balanceo para modelo"""
        n_y0 = len(target[target == 0])
        n_y1 = len(target[target == 1])
        scale = n_y0/n_y1
        
        """ instancio Modelo"""
        self._model = xgb.XGBClassifier(random_state=1, learning_rate=0.01, scale_pos_weight = scale)
        
        """Hago fit del modelo"""
        self._model.fit(features, target)
        return None

    def predict(
        self,
        features: pd.DataFrame
    ) -> List[int]:
        """
        Predict delays for new flights.

        Args:
            features (pd.DataFrame): preprocessed data.
        
        Returns:
            (List[int]): predicted targets.
        """

        """CEHQUEO QUE EXISTAN LAS FEATURES"""
        if not set(self.top_features).issubset(features.columns):
            # Lanza una excepción si falta alguna columna
            raise ValueError(f"Faltan las siguientes columnas: {set(self.variables_necesarias) - set(features.columns)}")
        
        """CHEQUEO DE QUE EXISTA EL MODELO"""
        if self._model==None:
            raise Exception("No se ha realizado fit de modelo.")
        


        return self._model.predict(features)
    
    def get_min_diff(self,data):
        fecha_o = datetime.strptime(data['Fecha-O'], '%Y-%m-%d %H:%M:%S')
        fecha_i = datetime.strptime(data['Fecha-I'], '%Y-%m-%d %H:%M:%S')
        min_diff = ((fecha_o - fecha_i).total_seconds())/60
        return min_diff