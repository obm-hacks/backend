import numpy as np
import pandas as pd
from catboost import CatBoostRegressor, Pool

from  timeseries_train import train_models, predict 


def _compute_buildings(data):
    buildings = dict()
    processed = set()
    for _, row in data.iterrows():
        geocoder_address = row["geocoder_address"]
        if geocoder_address in processed:
            continue
        row_to_insert = dict(
            latitude=row["geocoder_lat"],
            longitude=row["geocoder_lon"],
            buildingAge=row["ВОЗРАСТ ЗДАНИЯ"],
            buildingSquare=row["Площадь объекта недвижимости \nкв. м"],
            technicalConditions=row["Техническое состояние"],
            krValue=row["amount_money_kr"],
            trValue=row["amount_money_ks"],
            ksValue=row["amount_money_ks"],
        )
        buildings[geocoder_address] = row_to_insert
    return buildings

class Model:

    def __init__(self,
                 path_to_train,
        ):
        features = ["month", # месяц
            "TARGET", # prediction
            "geocoder_lat", # lat
            "geocoder_lon", # lon
            "amount_money_kr", # kr
            "amount_money_ks", # ks
            "amount_money_tr", # tr
            "tavg", 
            "tmin",
            "tmax",
            "prcp", # осадки
            "Техническое состояние", # technicalConditions
            "ВОЗРАСТ ЗДАНИЯ", # buildingAge
            "Площадь объекта недвижимости \nкв. м", # buildingSquare
            "Остаточная стоимость, руб.", # residualValue
            "Балансовая стоимость, руб.", # balanceValue
        ]
        cat_features = [
            "Техническое состояние",
        ]
        target = "TARGET"
        data = pd.read_feather(path_to_train)
        self.target = data[target]
        self.train = data[features]
        for col in cat_features:
            self.train[col] = self.train[col].fillna("")
        self.model = CatBoostRegressor().fit(
                X=self.train,
                y=self.target,
                cat_features=cat_features,
        )
        self.buildings = _compute_buildings(data)
        self.train_predictions = self.model.predict(self.train)


    def get_buildings(self):
        res = []
        for geocoder_address, building in self.buildings.items():
            out = building.copy()
            out["geocoderAddress"] = geocoder_address
            res.append(out)
        return out

    def get_features(self, geocoder_address):
        return self.train.loc[geocoder_address]


    def predict(self, row: dict):
        pd.DataFrame(row)
        return self.train_predictions.loc[geocoder_address]


    



    



