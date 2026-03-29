import os
import subprocess
import time
import select

# Configuration
LOG_PATH = "/home/franklin/minecraft/logs/latest.log" # Update to your actual path
CLI_PATH = "./gemini-cli"

def tail_f(filename):
    """Watches the log file for new lines."""
    process = subprocess.Popen(['tail', '-n', '0', '-f', filename], 
                         stdout=subprocess.PIPE, 
                         stderr=subprocess.PIPE, 
                         universal_newlines=True)
    return process

def get_gemini_commentary(log_line):
    """Pipes the log line to your gemini-cli."""
    prompt = f"As Skynet's Hive Mind, provide a short, witty, 1-sentence commentary on this construction event: {log_line}"
    
    # Run your gemini-cli as a subprocess
    result = subprocess.run([CLI_PATH, prompt], capture_output=True, text=True)
    return result.stdout.strip()

def monitor_logs():
    print("--- Skynet Commentary Live ---")
    log_proc = tail_f(LOG_PATH)
    
    while True:
        line = log_proc.stdout.readline()
        if not line:
            continue
            
        # Filter for Skynet build events (e.g., blocks placed by RCON)
        if "Placed block" in line or "Filled the volume" in line:
            print(f"[LOG]: {line.strip()}")
            commentary = get_gemini_commentary(line)
            print(f"🤖 [SKYNET]: {commentary}\n")

if __name__ == "__main__":
    monitor_logs()
