cd grading
pip install -r requirements.txt

python grading.py ex1 "../main" 2>&1 | stdbuf -oL tee feedback-ex1.txt
python grading.py ex2 "../main" 2>&1 | stdbuf -oL tee feedback-ex2.txt
python grading.py ex3 "../main" 2>&1 | stdbuf -oL tee feedback-ex3.txt
python grading.py ex4 "../main" 2>&1 | stdbuf -oL tee feedback-ex4.txt
python grading.py ex5 "../main" 2>&1 | stdbuf -oL tee feedback-ex5.txt

python grading.py pw2 "../main" 2>&1 | stdbuf -oL tee feedback-pw2.txt
python grading.py pw3 "../main" 2>&1 | stdbuf -oL tee feedback-pw3.txt
python grading.py pw4 "../main" 2>&1 | stdbuf -oL tee feedback-pw4.txt
python grading.py pw5 "../main" 2>&1 | stdbuf -oL tee feedback-pw5.txt
python grading.py pw6 "../main" 2>&1 | stdbuf -oL tee feedback-pw6.txt
python grading.py pw7 "../main" 2>&1 | stdbuf -oL tee feedback-pw7.txt
python grading.py pw8 "../main" 2>&1 | stdbuf -oL tee feedback-pw8.txt