from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
    return [{
        "latitude": 55.733364,
        "longitude": 37.640751,
        "geocoderAddress": "Addr",
        "prediction": 1000,
        "buildingAge": 29,
        "buildingSquare": 230,
        "technicalConditions": "Хорошее",
    }, {
        "latitude": 55.741557,
        "longitude": 37.620027,
        "geocoderAddress": "Some addr",
        "prediction": 1000,
        "buildingAge": 29,
        "buildingSquare": 230,
        "technicalConditions": "Хорошее"
    }]


@app.get("/buildings/{id}")
def get_info(id: str):
    print(id);
    return [{
        "date": "2020-04-20",
        "prediction": 100000,
        "weather": {
            "min": 20,
            "max": 30,
            "avg": 25,
            "precipitation": 25,
        },
    },
    {
        "date": "2020-05-20",
        "prediction": 80000,
        "weather": {
            "min": 25,
            "max": 30,
            "avg": 27,
            "precipitation": 79,
        },
    },
    {
        "date": "2020-06-20",
        "prediction": 120000,
        "weather": {
            "min": 27,
            "max": 34,
            "avg": 30,
            "precipitation": 24,
        },
    }]
