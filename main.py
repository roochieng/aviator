import multiprocessing
import subprocess
import sys
import os

def run_sportpesa():
    # Run sportpesa script
    subprocess.run([sys.executable, "E:/Development/Script/aviator/sportpesa.py"])

def run_betika_app():
    # Run betika script
    subprocess.run([sys.executable, "E:/Development/Script/aviator/betika.py"])


def run_one_x_bet():
    # Run 1x bet script
    subprocess.run([sys.executable, "E:/Development/Script/aviator/one_x_bet.py"])

if __name__ == "__main__":
    sportpesa_process = multiprocessing.Process(target=run_sportpesa)
    aviator_app_process = multiprocessing.Process(target=run_betika_app)
    one_x_bet_process = multiprocessing.Process(target=run_one_x_bet)

    sportpesa_process.start()
    aviator_app_process.start()
    one_x_bet_process.start()

    sportpesa_process.join()
    aviator_app_process.join()
    one_x_bet_process.join()
