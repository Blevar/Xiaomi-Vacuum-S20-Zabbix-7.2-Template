#!/usr/bin/env python3

from miio.miot_device import MiotDevice
import json
import sys

if len(sys.argv) != 3:
    print("Usage: python xiaomi_vacuum_s20plus.py <IP> <TOKEN>")
    sys.exit(1)

IP = sys.argv[1]
TOKEN = sys.argv[2]

# Lista wlasciwosci (SIID + PIID), które chcemy pobrc
properties = [
    {"siid": 1, "piid": 1},  # Manufacturer
    {"siid": 1, "piid": 2},  # Model
    {"siid": 1, "piid": 5},  # Serial number
    {"siid": 2, "piid": 1},  # Status
    {"siid": 2, "piid": 2},  # Mode
    {"siid": 2, "piid": 3},  # Error code
    {"siid": 2, "piid": 4},  # Unknown, always 8?
    {"siid": 2, "piid": 5},  # Area cleaned
    {"siid": 2, "piid": 6},  # Duration
    {"siid": 2, "piid": 7},  # Fan level
    #{"siid": 2, "piid": 8},  # Current clean mode
    #{"siid": 2, "piid": 9},  # Clean type (1=sweep, 2=mop, 3=both)
    #{"siid": 2, "piid": 10}, # Virtual walls JSON
    #{"siid": 2, "piid": 11}, # Forbidden zones JSON
    #{"siid": 2, "piid": 12}, # No-go lines JSON
    #{"siid": 2, "piid": 13}, # Room IDs
    #{"siid": 2, "piid": 14}, # Room names
    #{"siid": 2, "piid": 15}, # Room clean config
    #{"siid": 2, "piid": 16}, # Clean path mode
    #{"siid": 2, "piid": 17}, # Map saved (bool)
    #{"siid": 2, "piid": 18}, # Water level
    #{"siid": 2, "piid": 19}, # Map index JSON
    #{"siid": 2, "piid": 20}, # Multi-map mode
    #{"siid": 2, "piid": 21}, # Cleaning paused
    {"siid": 3, "piid": 1},  # Battery level
    {"siid": 3, "piid": 2},  # Charging
    #{"siid": 3, "piid": 3},  # Docked
    {"siid": 4, "piid": 1},  # Child lock
    #{"siid": 4, "piid": 2},  # Volume
    #{"siid": 4, "piid": 3},  # Do not disturb
    {"siid": 5, "piid": 1},  # Mop installed
    {"siid": 5, "piid": 2},  # Water tank installed
    {"siid": 8, "piid": 1},  # Main brush time left
    {"siid": 8, "piid": 2},  # Main brush percentage
    {"siid": 9, "piid": 1},  # Side brush time left
    {"siid": 9, "piid": 2},  # Side brush percentage
    {"siid": 10, "piid": 1}, # Filter time left
    {"siid": 10, "piid": 2}, # Filter percentage
    #{"siid": 11, "piid": 1}, # Mop time left
    #{"siid": 11, "piid": 2}, # Mop percentage
    #{"siid": 14, "piid": 1}, # Voice config
    #{"siid": 14, "piid": 2}, # Voice language
]

# Mapa nazw czytelnych
field_names = {
    (1, 1): "manufacturer",
    (1, 2): "model",
    (1, 5): "serial_number",
    (2, 1): "status",
    (2, 2): "mode",
    (2, 3): "error_code",
    (2, 4): "unknown_2_4",
    (2, 5): "area_cleaned_m2",
    (2, 6): "clean_time_min",
    (2, 7): "fan_power_level",
    (2, 8): "current_clean_mode",
    (2, 9): "clean_type",
    (2, 10): "virtual_walls",
    (2, 11): "forbidden_zones",
    (2, 12): "no_go_lines",
    (2, 13): "room_ids",
    (2, 14): "room_names",
    (2, 15): "room_clean_config",
    (2, 16): "clean_path_mode",
    (2, 17): "map_saved",
    (2, 18): "water_level",
    (2, 19): "map_index",
    (2, 20): "multi_map_mode",
    (2, 21): "cleaning_paused",
    (3, 1): "battery_level",
    (3, 2): "charging",
    (3, 3): "docked",
    (4, 1): "child_lock",
    (4, 2): "volume",
    (4, 3): "dnd_enabled",
    (5, 1): "mop_installed",
    (5, 2): "water_tank_installed",
    (8, 1): "main_brush_time_left",
    (8, 2): "main_brush_percent",
    (9, 1): "side_brush_time_left",
    (9, 2): "side_brush_percent",
    (10, 1): "filter_time_left",
    (10, 2): "filter_percent",
    (11, 1): "mop_time_left",
    (11, 2): "mop_percent",
    (14, 1): "voice_config",
    (14, 2): "voice_language",
}

# Funkcja tlumaczaca statusy
def translate(field, value):
    maps = {
        "status": {
            0: "Idle", 1: "Sweeping", 2: "Paused", 3: "Charging",
            4: "Error", 5: "Sweeping & Mopping", 6: "Mopping", 8: "Sleeping"
        },
        "mode": {
            0: "Idle", 1: "Auto", 2: "Zoned", 3: "Spot", 4: "Room"
        },
        "fan_power_level": {
            0: "Silent", 1: "Standard", 2: "Strong", 3: "Turbo"
        },
        "clean_type": {
            1: "Sweep", 2: "Mop", 3: "Sweep & Mop"
        },
        "clean_path_mode": {
            0: "S-shape", 1: "Y-shape", 2: "Deep clean", 3: "Quick"
        }
    }
    if field in maps:
        return maps[field].get(value, f"Unknown({value})")
    return value

try:
    #print("Retrieving full vacuum data...")
    device = MiotDevice(ip=IP, token=TOKEN)
    result = device.raw_command("get_properties", properties)

    output = {}
    for prop, response in zip(properties, result):
        key = field_names.get((prop["siid"], prop["piid"]), f"siid:{prop['siid']},piid:{prop['piid']}")
        value = response.get("value") if isinstance(response, dict) else response
        output[key] = translate(key, value)

    #print("\nResult:\n")
    print(json.dumps(output, indent=4, ensure_ascii=False))

except Exception as e:
    print(f"Error while communicating with the vacuum: {e}")
