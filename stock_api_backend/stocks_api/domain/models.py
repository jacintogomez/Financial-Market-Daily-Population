# This file isn't currently used anywhere

from dataclasses import dataclass

@dataclass
class Stock:
    company_name: str
    ticker: str
    response_code: int

