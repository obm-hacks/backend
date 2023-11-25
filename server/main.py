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
    res = model.get_buildings()
    return res


@app.get("/buildings/{id}")
def get_info(id: str):
    print(id)
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
