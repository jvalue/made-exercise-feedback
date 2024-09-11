cd grading
pip install -r requirements.txt

python grading.py "../main" 2>&1 | stdbuf -oL tee feedback-log.txt