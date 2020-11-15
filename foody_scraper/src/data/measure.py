from dataclasses import dataclass


@dataclass
class Measure:
    title: str
    normal_title_form: str
    amount: float
