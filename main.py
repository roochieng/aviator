import multiprocessing
import subprocess
import sys
import os

def run_sportpesa():
    # Run sportpesa script
    subprocess.run([sys.executable, "E:/Development/Script/aviator/sportpesa.py"])

def run_aviator_app():
    # Run aviator_app script
    subprocess.run([sys.executable, "E:/Development/Script/aviator/aviator_app.py"])

if __name__ == "__main__":
    sportpesa_process = multiprocessing.Process(target=run_sportpesa)
    aviator_app_process = multiprocessing.Process(target=run_aviator_app)

    sportpesa_process.start()
    aviator_app_process.start()

    sportpesa_process.join()
    aviator_app_process.join()
