import subprocess
import logging
from datetime import datetime
import sys

# Configure logging to show INFO and ERROR messages in terminal
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

def run_script(file_path: str, *args):
    logging.info("🟡 Starting script execution")
    
    try:
        logging.info(f"📍 Step 1: Preparing to run script: {file_path}")
        if args:
            logging.info(f"📍 Step 2: With arguments: {args}")

        # Construct the command
        command = ["python", file_path] + list(args)
        logging.info(f"📍 Step 3: Executing command: {' '.join(command)}")

        # Run the subprocess
        result = subprocess.run(command, capture_output=True, text=True)

        logging.info(f"📍 Step 4: Script completed with return code: {result.returncode}")

        if result.stdout:
            logging.info(f"📤 STDOUT:\n{result.stdout.strip()}")
        if result.stderr:
            logging.error(f"📥 STDERR:\n{result.stderr.strip()}")

        print(result.returncode)
        if result.returncode != 0:
            logging.error("❌ Script execution failed.")
        else:
            logging.info("✅ Script executed successfully.")

    except Exception as e:
        logging.exception(f"❗ Unexpected error occurred while executing script: {e}")

    logging.info("🔚 Finished script execution.\n")
