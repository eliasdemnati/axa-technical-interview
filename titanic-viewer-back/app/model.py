#!/usr/bin/env python3

from pydantic import BaseModel
from enum import Enum
from typing import Optional


class EmbarkLocation(str, Enum):
    C = "C"
    Q = "Q"
    S = "S"


class Sex(str, Enum):
    male = "male"
    female = "female"


class OutputPassenger(BaseModel):
    passenger_id: int
    p_class: int
    name: str
    sex: Sex
    age: Optional[float]
    nb_sibling_spouse: int
    nb_parent_children: int
    ticket: str
    fare: Optional[float]
    cabin: Optional[str]
    embark_location: EmbarkLocation


class InputPassenger(BaseModel):
    p_class: int
    name: str
    sex: Sex
    age: Optional[float]
    nb_sibling_spouse: int
    nb_parent_children: int
    ticket: str
    fare: Optional[float]
    cabin: Optional[str]
    embark_location: EmbarkLocation
