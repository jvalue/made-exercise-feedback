cd grading
pip install -r requirements.txt

python grading.py ex1 "../main" 2>&1 | stdbuf -oL tee feedback-ex1.txt
python grading.py ex2 "../main" 2>&1 | stdbuf -oL tee feedback-ex2.txt
python grading.py ex3 "../main" 2>&1 | stdbuf -oL tee feedback-ex3.txt
python grading.py ex4 "../main" 2>&1 | stdbuf -oL tee feedback-ex4.txt
python grading.py ex5 "../main" 2>&1 | stdbuf -oL tee feedback-ex5.txt