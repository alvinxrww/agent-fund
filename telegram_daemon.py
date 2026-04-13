import time
import os
import subprocess
import importlib.util
import sys

def load_module_from_path(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.path.insert(0, os.path.dirname(file_path))
    spec.loader.exec_module(module)
    sys.path.pop(0) 
    return module

# Load the Telegram server natively to poll for messages.
telegram_server = load_module_from_path('telegram_server', os.path.abspath('mcp-servers/telegram-bot/server.py'))

def flush_old_updates():
    """Fetch all pending updates on startup and return the next offset to use,
    effectively marking everything before this point as 'read'."""
    print("[*] Flushing old Telegram updates...")
    resp = telegram_server.get_latest_messages(limit=100)
    if resp.get("status") != "success":
        print(f"    Could not flush: {resp.get('message')}")
        return None
    
    messages = resp.get("messages", [])
    if messages:
        max_update_id = max(m.get("update_id", 0) for m in messages)
        print(f"    Flushed {len(messages)} old message(s). Starting fresh after update_id {max_update_id}.")
        return max_update_id + 1
    else:
        print("    No pending messages. Starting clean.")
        return None

def run_daemon():
    print("🚀 Telegram Daemon Started. Polling for inbound commands...")
    print("   Send '/run' to execute a dry run.")
    print("   Send '/run --live' to execute live trades.\n")
    
    # On startup, skip all old messages so we only react to new ones
    next_offset = flush_old_updates()
    
    while True:
        try:
            resp = telegram_server.get_latest_messages(limit=10, offset=next_offset)
            
            # If token is missing, the response is graceful but status is 'error'.
            if resp.get("status") == "error":
                print(f"⚠️ Telegram Polling Unavailable: {resp.get('message')}")
                print("   Daemon is sleeping for 30 seconds before retrying...")
                time.sleep(30)
                continue
                
            messages = resp.get("messages", [])
            messages.sort(key=lambda x: x.get("update_id", 0))
            
            for msg in messages:
                update_id = msg.get("update_id", 0)
                text = str(msg.get("text", "")).strip().lower()
                
                # Advance offset past this update so Telegram won't return it again
                next_offset = update_id + 1
                    
                if text == "/run":
                    print(f"\n[!] Detected '/run' command (Update ID: {update_id}). Spawning Orchestrator (DRY RUN)...")
                    telegram_server.send_message("⚙️ Detected `/run` command. Initiating pipeline (Dry Run)...")
                    
                    cmd = [r"venv\Scripts\python.exe", "orchestrator.py"]
                    subprocess.run(cmd)
                    
                    print("\n✅ Orchestrator execution complete. Returning to polling...")
                    
                elif text == "/run --live":
                    print(f"\n[!] Detected '/run --live' command (Update ID: {update_id}). Spawning Orchestrator (LIVE)...")
                    telegram_server.send_message("⚠️ Detected `/run --live` command. Initiating LIVE pipeline execution!")
                    
                    cmd = [r"venv\Scripts\python.exe", "orchestrator.py", "--live"]
                    subprocess.run(cmd)
                    
                    print("\n✅ Orchestrator LIVE execution complete. Returning to polling...")
                        
        except Exception as e:
            print(f"Daemon Polling Subsystem Error: {e}")
            
        time.sleep(1)

if __name__ == "__main__":
    run_daemon()

