from pydantic import BaseModel, validator
from typing import List


class SensorData(BaseModel):
    data: List[float]

    @validator("data")
    def ext(cls, v):
        data_len = 4
        if not len(v) == data_len:
            raise ValueError(f"Send exactly {data_len} values")
        return v
