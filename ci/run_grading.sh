cd grading
pip install -r requirements.txt

python grading.py "../main" 1 2>&1 | stdbuf -oL tee feedback-ex1.txt
python grading.py "../main" 2 2>&1 | stdbuf -oL tee feedback-ex2.txt
python grading.py "../main" 3 2>&1 | stdbuf -oL tee feedback-ex3.txt
python grading.py "../main" 4 2>&1 | stdbuf -oL tee feedback-ex4.txt
python grading.py "../main" 5 2>&1 | stdbuf -oL tee feedback-ex5.txt