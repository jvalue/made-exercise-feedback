import pandas as pd
from typing import Callable

class GradingRubric:
    def __init__(self, exerciseName):
        self.exerciseName = exerciseName
        self.exerciseResult = {}
        self.categories = {}

    def addCheck(self, category: str, check: Callable[[pd.DataFrame], int], maxPoints: int, errorHint: str):
        if (category not in self.categories):
            self.categories[category] = []

        self.categories[category].append({'check': check, 'maxPoints': maxPoints, 'errorHint': errorHint})

    def gradeData(self, df: pd.DataFrame):

        self.exerciseResult = {
            'maxPoints': 0, 'pointsAchieved': 0,
            'categories': {}
        }

        for category in self.categories:
            self.exerciseResult['categories'][category] = {'maxPoints': 0, 'pointsAchieved': 0, 'hints': []}

            for checkData in self.categories[category]:
                pointsAchieved = checkData['check'](df)

                self.exerciseResult['categories'][category]['maxPoints'] += checkData['maxPoints']
                self.exerciseResult['categories'][category]['pointsAchieved'] += pointsAchieved

                if (pointsAchieved < checkData['maxPoints']):
                    self.exerciseResult['categories'][category]['hints'].append(checkData['errorHint'])
            
            self.exerciseResult['maxPoints'] += self.exerciseResult['categories'][category]['maxPoints']
            self.exerciseResult['pointsAchieved'] += self.exerciseResult['categories'][category]['pointsAchieved']
        
        return self
    
    def getConsoleOutput(self) -> str:
        output = 'Feedback for {}\n'.format(self.exerciseName)
        output += '\tOverall points {} of {}\n'.format(self.exerciseResult['pointsAchieved'], self.exerciseResult['maxPoints'])
        output += '\t---\n'
        output += '\tBy category:\n'
        for category in self.exerciseResult['categories']:
            output += '\t\t{}: {} of {}\n'.format(category, self.exerciseResult['categories'][category]['pointsAchieved'], self.exerciseResult['categories'][category]['maxPoints'])
            for hint in self.exerciseResult['categories'][category]['hints']:
                output += '\t\t\tHint: {}\n'.format(hint)

        return output

    def getScore(self) -> str:
        return '{}%'.format((self.exerciseResult['pointsAchieved'] / self.exerciseResult['maxPoints']) * 100)