#!/usr/bin/env python3
import os
import random
import subprocess
from datetime import datetime

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

def read_number():
    with open('number.txt', 'r') as f:
        return int(f.read().strip())

def write_number(num):
    with open('number.txt', 'w') as f:
        f.write(str(num))

def git_commit():
    # Stage the changes
    subprocess.run(['git', 'add', 'number.txt'])

    # Create commit with current date
    date = datetime.now().strftime('%Y-%m-%d')
    commit_message = f"Update number: {date}"
    subprocess.run(['git', 'commit', '-m', commit_message])

def git_push():
    # Push the committed changes to GitHub
    result = subprocess.run(['git', 'push'], capture_output=True, text=True)
    if result.returncode == 0:
        print("Changes pushed to GitHub successfully.")
    else:
        print("Error pushing to GitHub:")
        print(result.stderr)

def update_cron_with_random_time():
    # Generate random hour (0-23) and minute (0-59)
    random_hour = random.randint(0, 23)
    random_minute = random.randint(0, 59)

    # Define the time for the scheduled task
    task_time = f"{random_hour:02}:{random_minute:02}"

    # Define the command to run the script
    task_name = "UpdateNumberTask"
    script_path = os.path.join(script_dir, 'update_number.py')
    command = f'schtasks /create /tn "{task_name}" /tr "python {script_path}" /sc once /st {task_time} /f'

    # Create or update the scheduled task
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"Task scheduled to run at {task_time} tomorrow.")
    else:
        print(f"Error scheduling task: {result.stderr}")

def main():
    try:
        current_number = read_number()
        new_number = current_number + 1
        write_number(new_number)

        git_commit()
        git_push()

        update_cron_with_random_time()

    except Exception as e:
        print(f"Error: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()
