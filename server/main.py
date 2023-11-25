from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from model import Model

model = Model(
    'data_with_target.frt')


origins = [
    "http://51.250.11.222",
    "http://localhost:5173",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/buildings")
def main():
    global model

    return [{
        "latitude": 55.733364,
        "longitude": 37.640751,
        "geocoderAddress": "Addr",
        "buildingAge": 29,
        "buildingSquare": 230,
        "technicalConditions": "Хорошее",
        "krValue": 21212124,
        "ksValue": 2112124,
        "trValue": 123123,
        "residualValue": 2011000,
        "balanceValue": 2012120,
    }, {
        "latitude": 55.741557,
        "longitude": 37.620027,
        "geocoderAddress": "Some addr",
        "buildingAge": 29,
        "buildingSquare": 230,
        "technicalConditions": "Хорошее",
        "krValue": 211212124, # кап ремонт
        "ksValue": 21122124, # еще какие-то
        "trValue": 1232123, # устройство территории
        "residualValue": 20110010,
        "balanceValue": 20122120,
    }]


@app.get("/buildings/{id}")
def get_info(id: str):
    print(id)
    return [{
        "prediction": 100000,
        "weatherMin": 20,
        "weatherMax": 30,
        "weatherAvg": 30,    
        "precipitation": 25,
    },
    {
        "prediction": 10000,
        "weatherMin": 19,
        "weatherMax": 32,
        "weatherAvg": 25,    
        "precipitation": 25,
    },
    {
        "prediction": 10000,
        "weatherMin": 19,
        "weatherMax": 32,
        "weatherAvg": 25,    
        "precipitation": 25,
    }]
