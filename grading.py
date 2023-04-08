from rubrics.Exercise1Rubric import buildExercise1Rubric
import os
import sys

def gradeExercise(rubricFactory, expectedModels, expectedOutputFile, expectedOutputTable):
    if os.path.isfile(expectedOutputFile):
        os.remove(expectedOutputFile)

    for expectedModel in expectedModels:
        if os.path.isfile(expectedModel):
            print('Found {}, executing model...'.format(expectedModel))
            if (expectedModel.endswith('.py')):
                os.system('python {}'.format(expectedModel))
                break
            elif (expectedModel.endswith('.jv')):
                os.system('jv {}'.format(expectedModel))
                break
            else:
                print('Could not find interpreter for model: {}. Skipping.'.format(expectedModel))
                return
    
    if os.path.isfile(expectedOutputFile):
        print('Found output file {}, grading...'.format(expectedOutputFile))
    else:
        print('Can not find expected output file: {}. Make sure your model generates it correctly!'.format(expectedOutputFile))
        print('Skipping.')
        return

    feedback = rubricFactory()\
        .gradeData('sqlite:///{}'.format(expectedOutputFile), expectedOutputTable)\
        .getConsoleOutput()

    print(feedback)

if (len(sys.argv) > 1):
    os.chdir(sys.argv[1])

gradeExercise(buildExercise1Rubric, ['exercises/exercise1.py', 'exercises/exercise1.jv'], 'airports.sqlite', 'airports')