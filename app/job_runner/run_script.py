import os
import subprocess
import logging
from datetime import datetime

# run_script.py
def run_script(file_path: str, *args):
    try:
        logging.info(f"[{datetime.now()}] Running script at: {file_path} with args: {args}")

        command = ["python", file_path] + list(args)  # Convert tuple to list and add args
        result = subprocess.run(command, capture_output=True, text=True)

        logging.info(f"Return Code: {result.returncode}")
        logging.info(f"STDOUT:\n{result.stdout}")
        
        if result.stderr:
            logging.error(f"STDERR:\n{result.stderr}")

        if result.returncode != 0:
            logging.error("Script execution failed.")
        else:
            logging.info("Script executed successfully.")
    except Exception as e:
        logging.error(f"Failed to execute script {file_path}: {e}")

    logging.info(f"[{datetime.now()}] Finished running script at: {file_path}")

