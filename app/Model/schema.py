from pydantic import BaseModel, Field

class PowerInput(BaseModel):
    base: int = Field(..., ge=0)
    exponent: int = Field(..., ge=0)


class FibonacciInput(BaseModel):
    n: int = Field(..., ge=0)


class FactorialInput(BaseModel):
    n: int = Field(..., ge=0)
 