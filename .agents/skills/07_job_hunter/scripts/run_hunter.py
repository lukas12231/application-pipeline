import sys
import os
import subprocess

# Add project root to path so we can import 'job_hunter'
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
sys.path.append(project_root)

def check_onboarding():
    """Checks if the baseline profile exists and is valid."""
    profile_path = os.path.join(project_root, "baseline_profile.md")
    if not os.path.exists(profile_path):
        print("[!] Error: 'baseline_profile.md' not found.")
        print("[i] Please run the '00_init_workspace' skill or place source documents in 'import/'.")
        return False
    
    with open(profile_path, 'r') as f:
        content = f.read()
        if "[VORNAME]" in content or "[NACHNAME]" in content:
            print("[!] Warning: 'baseline_profile.md' contains placeholders.")
            print("[i] Ensure your profile is authentic before running the scout.")
            # We don't exit here, but we warn the user.
    return True

def main():
    if not check_onboarding():
        sys.exit(1)
    
    venv_python = os.path.join(project_root, ".venv/bin/python")
    
    # 1. Scout
    print("[*] Starting Scouting Phase...")
    subprocess.run([venv_python, "-m", "job_hunter.engine", "--config", "hunter_config.json"], check=True)
    
    # 2. Enrich
    print("\n[*] Starting Enrichment Phase...")
    subprocess.run([venv_python, "-m", "job_hunter.extractor", "--limit", "30"], check=True)
    
    # 3. Filter
    print("\n[*] Starting Semantic Filtering Phase...")
    subprocess.run([venv_python, "-m", "job_hunter.filter", "--config", "hunter_config.json", "--profile", "profile.json"], check=True)
    
    # 4. Report
    print("\n[*] Generating Final Report...")
    subprocess.run([venv_python, "generate_report.py"], check=True)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[!] Pipeline failed: {e}")
        sys.exit(1)
