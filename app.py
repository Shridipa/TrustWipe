import json
import os
import subprocess
from datetime import datetime
import pytz
from cert_generator import generate_certificate
from render_pdf import render_certificate_to_pdf

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

    try:
        choice = int(input("\nSelect a drive to wipe (number): ")) - 1
        if choice < 0 or choice >= len(drives):
            print("❌ Invalid selection.")
            return None
        selected = drives[choice]["DeviceID"]
        confirm = input(f"⚠️ Are you sure you want to wipe {selected}? Type YES to confirm: ")
        return selected if confirm.strip().lower() == "yes" else None
    except ValueError:
        print("❌ Invalid input.")
        return None

def prompt_wipe_method():
    print("\n🧹 Choose Wipe Method:")
    print("1. Single Pass Overwrite (Fast, random data)")
    print("2. Multi Pass Overwrite (0s, 1s, random)")
    print("3. Crypto Pass Overwrite (Secure random data)")

    try:
        choice = int(input("Enter your choice (1-3): "))
        methods = {
            1: "Single Pass Overwrite",
            2: "Multi Pass Overwrite",
            3: "Crypto Pass Overwrite"
        }
        return methods.get(choice, "Single Pass Overwrite")
    except ValueError:
        print("❌ Invalid input.")
        return "Single Pass Overwrite"

def simulate_wipe(drive_letter, method):
    dummy_file = os.path.join(drive_letter, "dummy_wipe.bin")

    try:
        with open(dummy_file, "wb") as f:
            f.write(b"A" * 1024 * 1024)
        print(f"📁 Dummy file created at {dummy_file}")
    except Exception as e:
        print(f"❌ Failed to create dummy file: {e}")
        return None

    print(f"\n🧹 Starting {method} on {dummy_file}...")

    try:
        with open(dummy_file, "r+b") as f:
            if method == "Single Pass Overwrite":
                f.write(os.urandom(1024 * 1024))
            elif method == "Multi Pass Overwrite":
                f.write(b"\x00" * 1024 * 1024)
                f.seek(0)
                f.write(b"\xFF" * 1024 * 1024)
                f.seek(0)
                f.write(os.urandom(1024 * 1024))
            elif method == "Crypto Pass Overwrite":
                for _ in range(3):
                    f.seek(0)
                    f.write(os.urandom(1024 * 1024))
            f.flush()
        print(f"✅ {method} completed for {dummy_file}")
    except Exception as e:
        print(f"❌ Wipe failed: {e}")
        return None

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
        print("❌ Wipe simulation failed.")
        return

    device_info = {
        "serial_number": "SN123456789",
        "make": "Generic",
        "model": "DriveModelX",
        "storage_type": "HDD"
    }

    technician = {
        "technician_id": "tech-007",
        "signature": "TrustWipe Organization"
    }

    certificate = generate_certificate(wipe_log, device_info, technician)
    certificate["wipe_method"] = wipe_method

    # Add IST timestamp
    india_time = datetime.now(pytz.timezone("Asia/Kolkata"))
    certificate["timestamp"] = india_time.strftime("%Y-%m-%d %I:%M %p IST")

    os.makedirs("certificates", exist_ok=True)
    json_path = f"certificates/{certificate['certificate_id']}.json"
    with open(json_path, 'w') as f:
        json.dump(certificate, f, indent=4)

    print(f"\n📄 Certificate saved to {json_path}")

    wkhtmltopdf_path = r"C:\Users\KIIT\ZeroTrace_Cert\wkhtmltopdf\bin\wkhtmltopdf.exe"
    try:
        render_certificate_to_pdf(json_path, wkhtmltopdf_path)
    except Exception as e:
        print(f"❌ PDF generation failed: {e}")

if __name__ == "__main__":
    main()
