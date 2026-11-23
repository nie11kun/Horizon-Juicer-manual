"""Host-side IPC client and SinuTrain screenshot capture pipeline for Horizon-Juicer-manual.

Communicates with tools/vm_bridge/vm_agent.ps1 running inside the VMware guest via
shared files (heartbeat.json, cmd.json, resp_<id>.json).
"""

import argparse
import json
import os
import sys
import time
import uuid
from PIL import Image

BRIDGE_DIR = os.path.dirname(os.path.abspath(__file__))
MANUAL_DIR = os.path.abspath(os.path.join(BRIDGE_DIR, "..", ".."))
HEARTBEAT_FILE = os.path.join(BRIDGE_DIR, "heartbeat.json")
CMD_FILE = os.path.join(BRIDGE_DIR, "cmd.json")
OUT_DIR = os.path.join(BRIDGE_DIR, "out")
HMI_SHOT_DIR = os.path.join(MANUAL_DIR, "images", "sinutrain")

# Default normalized HMI screen crop box within SinuTrain window (left, top, right, bottom).
# Tuned after calibration on live SinuTrain window capture; overridden by crop_calib.json if present.
DEFAULT_HMI_CROP = (0.055, 0.055, 0.495, 0.565)
CALIB_FILE = os.path.join(BRIDGE_DIR, "crop_calib.json")


def load_heartbeat():
    if not os.path.exists(HEARTBEAT_FILE):
        return None
    try:
        with open(HEARTBEAT_FILE, "r", encoding="utf-8-sig") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return None


def is_vm_alive(max_age_sec=12):
    hb = load_heartbeat()
    if not hb:
        return False, None
    age = time.time() - hb.get("epoch", 0)
    return (age <= max_age_sec), {"age_sec": round(age, 1), **hb}


def send_cmd(action, timeout=30.0, **kwargs):
    cmd_id = uuid.uuid4().hex[:10]
    resp_path = os.path.join(BRIDGE_DIR, f"resp_{cmd_id}.json")
    payload = {"id": cmd_id, "action": action, **kwargs}
    tmp_cmd = CMD_FILE + ".tmp"
    with open(tmp_cmd, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False)
    os.replace(tmp_cmd, CMD_FILE)

    t0 = time.time()
    while time.time() - t0 < timeout:
        if os.path.exists(resp_path):
            time.sleep(0.05)
            try:                                  # the VM agent may still be writing the file -> retry
                with open(resp_path, "r", encoding="utf-8-sig") as f:
                    resp = json.load(f)
            except (ValueError, OSError):
                time.sleep(0.2)
                continue
            try:
                os.remove(resp_path)
            except OSError:
                pass
            if not resp.get("ok"):
                raise RuntimeError(f"VM action '{action}' failed: {resp.get('message')}")
            return resp
        time.sleep(0.15)
    raise TimeoutError(f"Timed out waiting for VM response to action '{action}' (id={cmd_id})")


def get_crop_ratios():
    if os.path.exists(CALIB_FILE):
        with open(CALIB_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return tuple(data["hmi_crop_ratios"])
    return DEFAULT_HMI_CROP


def crop_hmi_image(full_path, crop_path, ratios=None):
    ratios = ratios or get_crop_ratios()
    img = Image.open(full_path)
    w, h = img.size
    box = (
        int(round(w * ratios[0])),
        int(round(h * ratios[1])),
        int(round(w * ratios[2])),
        int(round(h * ratios[3])),
    )
    os.makedirs(os.path.dirname(crop_path), exist_ok=True)
    img.crop(box).save(crop_path)
    return crop_path


def main():
    parser = argparse.ArgumentParser(description="Horizon-Juicer SinuTrain VM Bridge Client")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("status", help="Check VM agent heartbeat and live SinuTrain window")
    sub.add_parser("backup", help="Backup VM SinuTrain hmi folder")
    sub.add_parser("restore", help="Restore VM SinuTrain hmi folder from latest backup")

    p_imp = sub.add_parser("import", help="Import package System-CF-Card into VM SinuTrain")
    p_imp.add_argument("package_subdir", help="Subfolder name under tools/vm_bridge/packages")

    p_shot = sub.add_parser("shot", help="Take SinuTrain screenshot and optionally crop HMI region")
    p_shot.add_argument("filename", help="Output filename inside tools/vm_bridge/out/")
    p_shot.add_argument("--crop-out", help="Optional cropped HMI output path")

    p_click = sub.add_parser("click", help="Relative click inside SinuTrain window")
    p_click.add_argument("rx", type=float)
    p_click.add_argument("ry", type=float)
    p_click.add_argument("--wait-ms", type=int, default=450)

    p_keys = sub.add_parser("keys", help="SendKeys string to SinuTrain window")
    p_keys.add_argument("keys")
    p_keys.add_argument("--wait-ms", type=int, default=400)

    args = parser.parse_args()

    alive, hb = is_vm_alive()
    if args.cmd == "status":
        print(json.dumps({"alive": alive, "heartbeat": hb}, indent=2, ensure_ascii=False))
        if alive:
            resp = send_cmd("status")
            print(json.dumps(resp, indent=2, ensure_ascii=False))
        sys.exit(0 if alive else 2)

    if not alive:
        print("VM bridge agent is NOT alive. Start tools/vm_bridge/vm_agent.bat inside the VM first.", file=sys.stderr)
        sys.exit(2)

    if args.cmd == "backup":
        print(json.dumps(send_cmd("backup_hmi", timeout=300.0), indent=2, ensure_ascii=False))
    elif args.cmd == "restore":
        print(json.dumps(send_cmd("restore_hmi", timeout=300.0), indent=2, ensure_ascii=False))
    elif args.cmd == "import":
        print(json.dumps(send_cmd("import_cf", timeout=60.0, packageSubDir=args.package_subdir), indent=2, ensure_ascii=False))
    elif args.cmd == "shot":
        resp = send_cmd("screenshot", filename=args.filename)
        full_path = os.path.join(OUT_DIR, args.filename)
        if args.crop_out:
            crop_hmi_image(full_path, args.crop_out)
            resp["croppedPath"] = args.crop_out
        print(json.dumps(resp, indent=2, ensure_ascii=False))
    elif args.cmd == "click":
        print(json.dumps(send_cmd("click_rel", rx=args.rx, ry=args.ry, waitMs=args.wait_ms), indent=2, ensure_ascii=False))
    elif args.cmd == "keys":
        print(json.dumps(send_cmd("send_keys", keys=args.keys, waitMs=args.wait_ms), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
