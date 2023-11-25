import numpy as np
import pandas as pd
import math
import json
import requests
import datetime
from meteostat import Point, Monthly
from catboost import CatBoostRegressor, Pool
from dateutil.relativedelta import relativedelta



def _get_datetime_range(start, end):
    result = []
    while start < end:
        result.append(start)
        start += relativedelta(months=1)
    return result

def _replace_nan(num):
    if pd.isna(num):
        return None
    return num

class Model:

    def __init__(self,
                 path_to_train,
        ):
        self.model_to_front = {
            "month": "month",
            "geocoder_lat": "latitude",
            "geocoder_lon": "longitude",
            "geocoder_address": "geocoderAddress",
            "amount_money_kr": "krValue", # kr
            "amount_money_ks": "ksValue", # ks
            "amount_money_tr": "trValue", # tr
            "tavg": "weatherAvg", 
            "tmin": "weatherMin",
            "tmax": "weatherMax",
            "prcp": "precipitation", # осадки
            "Техническое состояние": "technicalConditions",
            "ВОЗРАСТ ЗДАНИЯ": "buildingAge",
            "Площадь объекта недвижимости \nкв. м": "buildingSquare",
            "Остаточная стоимость, руб.": "residualValue",
            "Балансовая стоимость, руб.": "balanceValue",
            "TARGET": "prediction",
        }
        self.front_to_model = {
            value: key for key, value in self.model_to_front.items()
        }
        print(self.front_to_model)
        self.features = [
            "month", # месяц
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
        self.train = data[self.features]
        for col in cat_features:
            self.train[col] = self.train[col].fillna("")
        self.model = CatBoostRegressor().fit(
            X=self.train,
            y=self.target,
            cat_features=cat_features,

        )

        self.buildings = self._compute_buildings(data)
        self.train_predictions = self.model.predict(self.train)
        pd.DataFrame(self.train_predictions, columns=["TARGET"]).to_feather("predictions.frt")
    

    def _compute_buildings(self, data):
        buildings = dict()
        processed = set()
        columns = [
            "latitude",
            "longitude",
            "buildingAge",
            "buildingSquare",
            "technicalConditions",
            "krValue",
            "trValue",
            "ksValue",
            "residualValue",
            "balanceValue",
        ]
        for _, row in data.iterrows():
            geocoder_address = row["geocoder_address"]
            if geocoder_address in processed:
                continue
            row_to_insert = {
                column: row[self.front_to_model[column]]
                for column in columns
            }
            buildings[geocoder_address] = row_to_insert
        return buildings


    def get_buildings(self):
        res = []
        
        for geocoder_address, building in self.buildings.items():
            out = building.copy()
            out["geocoderAddress"] = geocoder_address
            out = {
                key: _replace_nan(value) for key, value in out.items()
            }
            res.append(out)

        return res

    def _request_to_weather_api(self, start, end, lat, lon):
        point = Point(lat=lat, lon=lon)
        data = Monthly(point, start, end)
        data = data.fetch()
        if not len(data):
            data = pd.DataFrame(index=_get_datetime_range(start, end), columns=data.columns)
        data["month"] = pd.to_datetime(data.index)
        return data.reset_index(drop=True)


    def _request_to_geocoder(string, api_key="8c1a744e-abae-4b1f-a292-076e70d90d92"):
        lat_1, lon_1 = 41.755060, 100.567964
        lat_2, lon_2 = 78.300151, 190.346714
        query = f"https://geocode-maps.yandex.ru/1.x?apikey={api_key}&geocode={string}&format=json&bbox={lon_1},{lat_1}~{lon_2},{lat_2}"
        res = requests.get(query)
        return json.loads(res.content)


    def predict_by_id(self, id: str):
        row = self.buildings[id]
        row = {
                key: _replace_nan(value) for key, value in row.items()
            }
        return self.predict(row)

    def predict(self, row: dict):
        columns = [
            "weatherMin",
            "weatherMax",
            "weatherAvg",   
            "precipitation",
        ]

        amount_money_columns = [
            "amount_money_kr", # kr
            "amount_money_ks", # ks
            "amount_money_tr", # tr
        ]

        now = datetime.datetime.now() - datetime.timedelta(days=365*3)
        start = datetime.datetime(year=now.year, month=now.month, day=1)
        end = start + datetime.timedelta(days=365 * 3)
        end = datetime.datetime(year=end.year, month=end.month, day=1)

        row = {self.front_to_model[key]: value for key, value in row.items()}

        lat = row["geocoder_lat"]
        lon = row["geocoder_lon"]
        df = self._request_to_weather_api(start, end, lat, lon)
        print(df.info())
        for key, value in row.items():
            df[key] = value
            if key in amount_money_columns:
                df[key] = value / len(df)
        print(df.info())
        prediction = self.model.predict(df[self.features])
        result = []

        for i, row in df.iterrows():
            answer = dict()
            answer["prediction"] = prediction[i]
            answer["date"] = row["month"]
            for column in columns:
                answer[column] = row[self.front_to_model[column]]
            answer = {
                key: _replace_nan(value) for key, value in answer.items()
            }
            result.append(answer)
        return result

    



    



