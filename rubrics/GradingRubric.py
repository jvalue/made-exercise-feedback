from typing import Callable
import pandas as pd

class GradingRubric:
    def __init__(self):
        self.categories = {}

    def addCheck(self, category: str, check: Callable[[pd.DataFrame], int], maxPoints: int, errorHint: str):
        if (category not in self.categories):
            self.categories[category] = []

        self.categories[category].append({'check': check, 'maxPoints': maxPoints, 'errorHint': errorHint})

    