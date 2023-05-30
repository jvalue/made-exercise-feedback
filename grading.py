from rubrics.Exercise1Rubric import buildExercise1Rubric
from rubrics.Exercise2Rubric import buildExercise2Rubric
import os
import sys

def gradeExercise(rubricFactory, expectedModels, expectedOutputFile, expectedOutputTable):
    if os.path.isfile(expectedOutputFile):
        os.remove(expectedOutputFile)

    for expectedModel in expectedModels:
        print('Looking for {} to execute.'.format(expectedModel))
        if os.path.isfile(expectedModel):
            print('[SUCCESS] Found {}, executing.'.format(expectedModel))
            if (expectedModel.endswith('.py')):
                os.system('python {}'.format(expectedModel))
                break
            elif (expectedModel.endswith('.jv')):
                os.system('jv {}'.format(expectedModel))
                break
            else:
                print('[ERROR] Could not find interpreter for model: {}.'.format(expectedModel))
                print('Skipping.')
                return
    
    print('Looking for {} to grade.'.format(expectedOutputFile))
    if os.path.isfile(expectedOutputFile):
        print('[SUCCESS] Found output file {}, grading...'.format(expectedOutputFile))
    else:
        print('[ERROR] Can not find expected output file: {}. Make sure your model generates it correctly!'.format(expectedOutputFile))
        print('Skipping.')
        return

    feedback = rubricFactory()\
        .gradeData('sqlite:///{}'.format(expectedOutputFile), expectedOutputTable)\
        .getConsoleOutput()

    print(feedback)

if (len(sys.argv) > 1):
    os.chdir(sys.argv[1])

#gradeExercise(buildExercise1Rubric, ['exercises/exercise1.py', 'exercises/exercise1.jv'], 'airports.sqlite', 'airports')
gradeExercise(buildExercise2Rubric, ['exercises/exercise2.py', 'exercises/exercise2.jv'], 'trainstops.sqlite', 'trainstops')