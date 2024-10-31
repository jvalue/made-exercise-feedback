import pandas as pd

from rubrics.GradingRubric import GradingRubric

class Grader:
    def __init__(self, exerciseName):
        self.exerciseName = exerciseName
        self.resultPerCategory: dict = {}
          
    def gradeData(self, df: pd.DataFrame, rubric: GradingRubric):
        for category in rubric.categories:
            if category not in self.resultPerCategory:
              self.resultPerCategory[category] = {'maxPoints': 0, 'pointsAchieved': 0, 'hints': []}

            for checkData in rubric.categories[category]:
                pointsAchieved = checkData['check'](df)

                self.resultPerCategory[category]['maxPoints'] += checkData['maxPoints']
                self.resultPerCategory[category]['pointsAchieved'] += pointsAchieved

                if (pointsAchieved < checkData['maxPoints']):
                    self.resultPerCategory[category]['hints'].append(checkData['errorHint'])        
        return self
      
    def totalAchievedPoints(self) -> int:
        totalPoints = 0
        for category in self.resultPerCategory:
            totalPoints += self.resultPerCategory[category]['pointsAchieved']
        return totalPoints
      
    def totalMaxPoints(self) -> int:
        totalMaxPoints = 0
        for category in self.resultPerCategory:
            totalMaxPoints += self.resultPerCategory[category]['maxPoints']
        return totalMaxPoints
      
    def getConsoleOutput(self) -> str:
              
        output = 'Feedback for {}\n'.format(self.exerciseName)
        output += '\tOverall points {} of {}\n'.format(self.totalAchievedPoints(), self.totalMaxPoints())
        output += '\t---\n'
        output += '\tBy category:\n'
        for category in self.resultPerCategory:
            output += '\t\t{}: {} of {}\n'.format(category, self.resultPerCategory[category]['pointsAchieved'], self.resultPerCategory[category]['maxPoints'])
            for hint in self.resultPerCategory[category]['hints']:
                output += '\t\t\tHint: {}\n'.format(hint)

        return output

    def getScore(self) -> str:
        return '{}%'.format((self.totalAchievedPoints() / self.totalMaxPoints()) * 100)