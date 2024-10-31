from rubrics.Grader import Grader
from rubrics.Exercise1Rubric import buildExercise1Rubric
from rubrics.Exercise2Rubric import buildExercise2Rubric
from rubrics.Exercise3RubricGdp import buildExercise3RubricGdp
from rubrics.Exercise3RubricBondIssuance import buildExercise3RubricBondIssuance
from rubrics.Exercise4Rubric import buildExercise4Rubric
from rubrics.Exercise5Rubric import buildExercise5Rubric
import os
import sys
import sqlite3
import pandas as pd
from dataclasses import dataclass

@dataclass
class GradingSubject:
  rubricFactory: callable
  expectedOutputFile: str
  expectedOutputTable: str

def gradeExercise(
  exNumber: int, 
  expectedModel: str,
  gradingSubjects: list[GradingSubject]
):
  print(f"[INFO] Preparing feedback for EXERCISE {exNumber}:")
  print(
    "[INFO] If this exercise does not need to be submitted yet, you can ignore all output after this."
  )
  
  for gradingSubject in gradingSubjects:
      if os.path.isfile(gradingSubject.expectedOutputFile):
          os.remove(gradingSubject.expectedOutputFile)

  print(f"\tLooking for {expectedModel} to execute.")
  if not os.path.isfile(expectedModel):
      print(f"\t[WARNING] Could not find file to grade: {expectedModel}")
      return

  print(f"\t[SUCCESS] Found {expectedModel}, executing.")
  if not expectedModel.endswith(".jv"):
      print(
          f"\t[INFO] Could not find interpreter for model: {expectedModel}."
      )
      print("\tSkipping.")
      return

  os.system(f"jv {expectedModel}")
  
  grader = Grader(exNumber)
  
  for gradingSubject in gradingSubjects:
    gradeSubject(gradingSubject, grader)
    
  feedback = grader.getConsoleOutput()
  print("")
  print(feedback)
    
def gradeSubject(gradingSubject: GradingSubject, grader: Grader):
    print(f"\tLooking for {gradingSubject.expectedOutputFile} to grade.")
    if not os.path.isfile(gradingSubject.expectedOutputFile):
        print(f"\t[ERROR] Can not find expected output file: {gradingSubject.expectedOutputFile}.")
        print("\tMake sure your model generates it as described in the exercise!")
        print("\tSkipping.")
        gradedRubric = gradingSubject.rubricFactory()
        grader.gradeMissingOutput(gradedRubric)
        return

    print(f"\t[SUCCESS] Found output file {gradingSubject.expectedOutputFile}, grading...")
    connection = sqlite3.connect(gradingSubject.expectedOutputFile)

    cursor = connection.cursor()
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{gradingSubject.expectedOutputTable}';")
    table_exists = cursor.fetchone()
    if not table_exists:
      print(f"\t[ERROR] Table {gradingSubject.expectedOutputTable} does not exist in {gradingSubject.expectedOutputFile}.")
      connection.close()
      gradedRubric = gradingSubject.rubricFactory()
      grader.gradeMissingOutput(gradedRubric)
      return

    try:
        query = f"SELECT * FROM {gradingSubject.expectedOutputTable}"
        df = pd.read_sql_query(query, connection)
    except Exception as e:
        print(f"Exception for {gradingSubject.expectedOutputFile}: {e}")
        connection.close()
        return

    gradedRubric = gradingSubject.rubricFactory()
    grader.gradeData(df, gradedRubric)

if len(sys.argv) < 1:
    print("Missing argument.\nUsage: python grading.py <exerciseId> <dir (optional)>")
    exit(1)

try:
    exerciseId = int(sys.argv[1])
except ValueError:
    print("The argument provided is not an integer.")
    exit(1)

if len(sys.argv) > 2:
    os.chdir(sys.argv[2])

match (exerciseId):
    case 1:
        gradeExercise(
            1,
            "exercises/exercise1.jv", 
            [GradingSubject(
                expectedOutputFile="airports.sqlite", 
                expectedOutputTable="airports", 
                rubricFactory=buildExercise1Rubric
            )],
        )
    case 2:
        gradeExercise(
            2,
            "exercises/exercise2.jv", 
            [GradingSubject(
                expectedOutputFile="trees.sqlite", 
                expectedOutputTable="trees", 
                rubricFactory=buildExercise2Rubric
            )],
        )
    case 3:
        gradeExercise(
            3,
            "exercises/exercise3.jv", 
            [GradingSubject(
                expectedOutputFile="country-stats.sqlite", 
                expectedOutputTable="bondIssuance", 
                rubricFactory=buildExercise3RubricBondIssuance
            ), GradingSubject(
                expectedOutputFile="country-stats.sqlite", 
                expectedOutputTable="gdpPerCapita", 
                rubricFactory=buildExercise3RubricGdp
            )],
        )
    case 4:
        gradeExercise(
            4,
            "exercises/exercise4.jv", 
            [GradingSubject(
                expectedOutputFile="temperatures.sqlite", 
                expectedOutputTable="temperatures", 
                rubricFactory=buildExercise4Rubric
            )],
        )
    case 5:
        gradeExercise(
            5,
            "exercises/exercise5.jv", 
            [GradingSubject(
                expectedOutputFile="gtfs.sqlite", 
                expectedOutputTable="stops", 
                rubricFactory=buildExercise5Rubric
            )],
        )
    case _: 
        print(f"No grading found for exercise with id {exerciseId}")




