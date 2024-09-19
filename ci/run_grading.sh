cd grading
pip install -r requirements.txt

python grading.py 1 "../main" 2>&1 | stdbuf -oL tee feedback-ex1.txt
python grading.py 2 "../main" 2>&1 | stdbuf -oL tee feedback-ex2.txt
python grading.py 3 "../main" 2>&1 | stdbuf -oL tee feedback-ex3.txt
python grading.py 4 "../main" 2>&1 | stdbuf -oL tee feedback-ex4.txt
python grading.py 5 "../main" 2>&1 | stdbuf -oL tee feedback-ex5.txt