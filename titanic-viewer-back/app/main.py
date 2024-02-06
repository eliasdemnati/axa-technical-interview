#!/usr/bin/env python3

import uvicorn
import os
from fastapi import FastAPI, HTTPException
from databases import Database
from model import OutputPassenger, InputPassenger
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

database = Database(
    "postgresql://{}:{}@{}:{}/{}".format(
        os.environ.get("POSTGRES_USER"),
        os.environ.get("POSTGRES_PASSWORD"),
        os.environ.get("POSTGRES_HOST"),
        os.environ.get("POSTGRES_PORT"),
        os.environ.get("POSTGRES_DB"),
    )
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get(
    "/passengers/",
    response_model=list[OutputPassenger]
)
async def get_all_passengers(search_value: str = ''):
    try:
        passengers = await database.fetch_all(
            query="""
                SELECT
                    passenger_id,
                    p_class,
                    name,
                    sex,
                    age,
                    nb_sibling_spouse,
                    nb_parent_children,
                    ticket,
                    fare,
                    cabin,
                    embark_location
                FROM
                    passengers
                WHERE
                    name ILIKE '%' || :search_value || '%';

            """,
            values={"search_value": search_value}
        )
        return [dict(passenger) for passenger in passengers]
    except Exception as error:
        print(error)
        raise HTTPException(status_code=500, detail='Error')  # Could be improved


@app.get(
    "/passengers/{passenger_id}",
    response_model=OutputPassenger
)
async def get_one_passenger(
    passenger_id: int = None
):
    if (passenger_id is None):
        raise HTTPException(status_code=404, detail='Passenger not found')
    try:
        passenger = await database.fetch_one(
            query="""
                SELECT
                    passenger_id,
                    p_class,
                    name,
                    sex,
                    age,
                    nb_sibling_spouse,
                    nb_parent_children,
                    ticket,
                    fare,
                    cabin,
                    embark_location
                FROM
                    passengers
                WHERE
                    passenger_id = :passenger_id
            """,
            values={"passenger_id": passenger_id}
        )

        if (passenger is None):
            raise HTTPException(status_code=404, detail='Passenger not found')

        return dict(passenger)
    except Exception as error:
        print(error)
        raise HTTPException(status_code=500, detail='Error')  # Could be improved


@app.post(
    "/passengers/",
    response_model=OutputPassenger
)
async def insert_passenger(passenger: InputPassenger):
    try:
        input_passenger = dict(passenger)
        new_passenger = await database.fetch_one(
            query="""
                INSERT INTO passengers
                    (
                        p_class,
                        name,
                        sex,
                        age,
                        nb_sibling_spouse,
                        nb_parent_children,
                        ticket,
                        fare,
                        cabin,
                        embark_location
                    )
                VALUES
                    (
                        :p_class,
                        :name,
                        :sex,
                        :age,
                        :nb_sibling_spouse,
                        :nb_parent_children,
                        :ticket,
                        :fare,
                        :cabin,
                        :embark_location
                    )
                RETURNING *
            """,
            values={
                "p_class": input_passenger['p_class'],
                "name": input_passenger['name'],
                "sex": input_passenger['sex'],
                "age": input_passenger['age'],
                "nb_sibling_spouse": input_passenger['nb_sibling_spouse'],
                "nb_parent_children": input_passenger['nb_parent_children'],
                "ticket": input_passenger['ticket'],
                "fare": input_passenger['fare'],
                "cabin": input_passenger['cabin'],
                "embark_location": input_passenger['embark_location'],
            }
        )
        return dict(new_passenger)
    except Exception as error:
        print(error)
        raise HTTPException(status_code=500, detail='Error')  # Could be improved

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)

