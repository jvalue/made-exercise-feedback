from rubrics.Exercise1Rubric import buildExercise1Rubric
from rubrics.Exercise2Rubric import buildExercise2Rubric
from rubrics.Exercise3Rubric import buildExercise3Rubric
from rubrics.Exercise4Rubric import buildExercise4Rubric
from rubrics.Exercise5Rubric import buildExercise5Rubric
import os
import sys
import sqlite3
import pandas as pd


def gradeExercise(
    exNumber, rubricFactory, expectedModels, expectedOutputFile, expectedOutputTable
):
    print(f"[INFO] Preparing feedback for EXERCISE {exNumber}:")
    print(
        "[INFO] If this exercise does not need to be submitted yet, you can ignore all output after this."
    )
    if os.path.isfile(expectedOutputFile):
        os.remove(expectedOutputFile)

    for expectedModel in expectedModels:
        print(f"\tLooking for {expectedModel} to execute.")
        if not os.path.isfile(expectedModel):
            print(f"\t[WARNING] Could not find file to grade: {expectedModel}")
            break
      
        print(f"\t[SUCCESS] Found {expectedModel}, executing.")
        if expectedModel.endswith(".py"):
            os.system(f"python {expectedModel}")
            break
        elif expectedModel.endswith(".jv"):
            os.system(f"jv {expectedModel}")
            break
        else:
            print(
                f"\t[INFO] Could not find interpreter for model: {expectedModel}."
            )
            print("\tSkipping.")
            return

    print(f"\tLooking for {expectedOutputFile} to grade.")
    if os.path.isfile(expectedOutputFile):
        print(f"\t[SUCCESS] Found output file {expectedOutputFile}, grading...")
    else:
        print(f"\t[ERROR] Can not find expected output file: {expectedOutputFile}.")
        print("\tMake sure your model generates it as described in the exercise!")
        print("\tSkipping.")
        return

    connection = sqlite3.connect(expectedOutputFile)

    try:
        query = f"SELECT * FROM {expectedOutputTable}"
        df = pd.read_sql_query(query, connection)
    except Exception as e:
        print(f"Exception for {expectedOutputFile}: {e}")
        connection.close()
        return

    gradedRubric = rubricFactory().gradeData(df)
    feedback = gradedRubric.getConsoleOutput()

    print("")
    print(feedback)


def gradeProjectWork(
    pwNumber, expectedFiles
):
    print(f"[INFO] Preparing feedback for PROJECT WORK {pwNumber}:")
    print(
        "[INFO] If this project work does not need to be submitted yet, you can ignore all output after this."
    )

    for expectedFile in expectedFiles:
        print(f"\tLooking for file {expectedFile}.")
        if not os.path.isfile(expectedFile):
            print(f"\t[ERROR] Could not find file: {expectedFile}")
            break
      
        print(f"\t[SUCCESS] Found file: {expectedFile}.")

    print("\t[INFO] That's all we can currently offer as quick feedback for this project work. The rest is manual grading at the end of the semester.")


if len(sys.argv) < 1:
    print("Missing argument.\nUsage: python grading.py <exerciseId/projectWorkId> <dir (optional)>")
    exit(1)

exerciseId = sys.argv[1]

if len(sys.argv) > 2:
    os.chdir(sys.argv[2])

match (exerciseId):
    case "ex1":
      gradeExercise(
          1,
          buildExercise1Rubric,
          ["exercises/exercise1.jv"],
          "airports.sqlite",
          "airports",
      )
    case "ex2":
      gradeExercise(
          2,
          buildExercise2Rubric,
          ["exercises/exercise2.jv"],
          "trees.sqlite",
          "trees",
      )
    case "ex3":
        gradeExercise(
            3,
            buildExercise3Rubric,
            ["exercises/exercise3.jv"],
            "goodsTransportedByTrain.sqlite",
            "goods",
        )
    case "ex4":
        gradeExercise(
            4,
            buildExercise4Rubric,
            ["exercises/exercise4.jv"],
            "temperatures.sqlite",
            "temperatures",
        )
    case "ex5":
        gradeExercise(
            5,
            buildExercise5Rubric,
            ["exercises/exercise5.jv"],
            "gtfs.sqlite",
            "stops",
        )
    case "pw2":
        gradeProjectWork(
            2,
            ["project/project-plan.md"],
        )
    case "pw3":
        gradeProjectWork(
            3,
            ["project/pipeline.sh"],
        )
    case "pw4":
        gradeProjectWork(
            4,
            ["project/data-report.pdf"],
        )
    case "pw5":
        gradeProjectWork(
            5,
            ["project/tests.sh"],
        )
    case "pw6":
        gradeProjectWork(
            6,
            [".github/workflows/data-pipeline.yml"],
        )
    case "pw7":
        gradeProjectWork(
            7,
            ["project/analysis-report.pdf"],
        )
    case "pw8":
        gradeProjectWork(
            8,
            ["project/slides.pdf"],
        )
    case _: 
        print(f"No grading found for submission with id {exerciseId}")




