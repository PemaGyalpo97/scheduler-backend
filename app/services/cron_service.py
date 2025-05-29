import subprocess
from datetime import datetime

async def schedule_script_execution(scheduler_id: int, file_path: str, date_str: str, time_str: str):
    # Parse date and time
    dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")

    # Convert to cron format
    cron_time = f"{dt.minute} {dt.hour} {dt.day} {dt.month} *"
    command = f"{file_path} >> {file_path}.log 2>&1"

    # Add cron job
    cron_job = f"{cron_time} {command}"

    try:
        # Read existing crontab
        current_cron = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
        cron_jobs = current_cron.stdout if current_cron.returncode == 0 else ""

        # Add new cron line
        cron_jobs += f"\n# scheduler_id: {scheduler_id}\n{cron_job}\n"

        # Write new crontab
        subprocess.run(["crontab", "-"], input=cron_jobs, text=True)

        print("Cron job scheduled successfully")
    except Exception as e:
        print(f"Failed to schedule cron job: {e}")
