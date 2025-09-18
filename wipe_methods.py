import json
import os
import subprocess
from cert_generator import generate_certificate
from wipe_methods import single_pass_overwrite, multi_pass_overwrite, crypto_pass_overwrite

def list_drives():
    cmd = [
        'powershell', '-noprofile', '-command',
        'Get-WmiObject -Class Win32_LogicalDisk | Select-Object DeviceID,VolumeName,DriveType | ConvertTo-Json'
    ]
    result = subprocess.run(cmd, text=True, stdout=subprocess.PIPE)
    try:
        drives = json.loads(result.stdout)
        return drives if isinstance(drives, list) else [drives]
    except json.JSONDecodeError:
        print("❌ Failed to parse drive list.")
        return []

def prompt_drive_selection(drives):
    print("\n📦 Available Drives:")
    for i, d in enumerate(drives):
        dtype = {
            0: "Unknown", 1: "No Root", 2: "Removable",
            3: "Local Disk", 4: "Network", 5: "CD-ROM", 6: "RAM"
        }.get(d["DriveType"], "Other")
        print(f"{i+1}. {d['DeviceID']} ({dtype}) - {d.get('VolumeName', '')}")

    choice = int(input("\nSelect a drive to wipe (number): ")) - 1
    selected = drives[choice]["DeviceID"]
    confirm = input(f"⚠️ Are you sure you want to wipe {selected}? Type YES to confirm: ")
    return selected if confirm == "YES" else None

def prompt_wipe_method():
    print("\n🧹 Choose Wipe Method:")
    print("1. Single Pass Overwrite (Fast, random data)")
    print("2. Multi Pass Overwrite (0s, 1s, random)")
    print("3. Crypto Pass Overwrite (Secure random data)")

    choice = int(input("Enter your choice (1-3): "))
    methods = {
        1: "Single Pass Overwrite",
        2: "Multi Pass Overwrite",
        3: "Crypto Pass Overwrite"
    }
    return methods.get(choice, "Single Pass Overwrite")

def simulate_wipe(drive_letter, method):
    dummy_file = f"{drive_letter}\\dummy_wipe.bin"
    try:
        with open(dummy_file, "wb") as f:
            f.write(b"A" * 1024 * 1024)  # 1MB dummy file
    except Exception as e:
        print(f"❌ Failed to create dummy file: {e}")
        return None

    print(f"\n🧹 Starting {method} on {dummy_file}...")

    if method == "Single Pass Overwrite":
        single_pass_overwrite(dummy_file)
    elif method == "Multi Pass Overwrite":
        multi_pass_overwrite(dummy_file)
    elif method == "Crypto Pass Overwrite":
        crypto_pass_overwrite(dummy_file)

    return f"Wipe log: {dummy_file} wiped using {method}."

def main():
    drives = list_drives()
    if not drives:
        print("❌ No drives detected.")
        return

    selected_drive = prompt_drive_selection(drives)
    if not selected_drive:
        print("❌ Wipe cancelled.")
        return

    wipe_method = prompt_wipe_method()
    wipe_log = simulate_wipe(selected_drive, wipe_method)
    if not wipe_log:
        print("❌ Wipe failed.")
        return

    device_info = {
        "serial_number": "SN123456789",
        "make": "Generic",
        "model": "DriveModelX",
        "storage_type": "HDD"
    }

    technician = {
        "technician_id": "tech-007",
        "signature": "TrustWipeSystem"
    }

    certificate = generate_certificate(wipe_log, device_info, technician)

    os.makedirs("certificates", exist_ok=True)
    filename = f"certificates/{certificate['certificate_id']}.json"
    with open(filename, 'w') as f:
        json.dump(certificate, f, indent=4)

    print(f"\n📄 Certificate saved to {filename}")

if __name__ == "__main__":
    main()
