import json
import sys
import csv

from collections import defaultdict


# ============================================================
# ARINC429 Decoder / Analyzer
#
# Features:
#   - Proper ARINC label decode
#   - Odd parity validation
#   - CSV export
#   - Label summary
#   - Interactive terminal viewer
#   - Automatic JSON structure detection
#
# Usage:
#   python arinc_decode.py capture.json
#
# Outputs:
#   decoded.csv
#   label_summary.csv
# ============================================================


# ------------------------------------------------------------
# Reverse ARINC label bits
# ------------------------------------------------------------
def reverse8(b):

    b = ((b & 0xF0) >> 4) | ((b & 0x0F) << 4)
    b = ((b & 0xCC) >> 2) | ((b & 0x33) << 2)
    b = ((b & 0xAA) >> 1) | ((b & 0x55) << 1)

    return b


# ------------------------------------------------------------
# ARINC odd parity check
# ------------------------------------------------------------
def check_odd_parity(word):

    ones = 0

    for i in range(32):

        if word & (1 << i):
            ones += 1

    return (ones % 2) == 1


# ------------------------------------------------------------
# Decode ARINC word
# ------------------------------------------------------------
def decode_arinc(word):

    raw_label = word & 0xFF

    label = reverse8(raw_label)

    sdi = (word >> 8) & 0x3

    data = (word >> 10) & 0x7FFFF

    ssm = (word >> 29) & 0x3

    parity_bit = (word >> 31) & 0x1

    parity_ok = check_odd_parity(word)

    return {

        "raw_hex": f"0x{word:08X}",

        "label_oct": format(label, '03o'),

        "label_dec": label,

        "sdi": sdi,

        "data_hex": f"0x{data:05X}",

        "data_dec": data,

        "ssm": ssm,

        "parity_bit": parity_bit,

        "parity_ok": parity_ok,
    }


# ------------------------------------------------------------
# Automatically locate message list in JSON
# ------------------------------------------------------------
def find_records(obj):

    # direct list
    if isinstance(obj, list):
        return obj

    # recursive dict search
    if isinstance(obj, dict):

        for k, v in obj.items():

            if isinstance(v, list):

                if len(v) > 0 and isinstance(v[0], dict):
                    return v

            elif isinstance(v, dict):

                r = find_records(v)

                if r is not None:
                    return r

    return None


# ============================================================
# MAIN
# ============================================================

if len(sys.argv) < 2:

    print()
    print("usage:")
    print("    python arinc_decode.py capture.json")
    print()

    sys.exit(1)

filename = sys.argv[1]

print()
print("======================================================")
print(" ARINC429 DECODER")
print("======================================================")
print()

# ------------------------------------------------------------
# Load file
# ------------------------------------------------------------
with open(filename, 'r') as f:

    raw = f.read()

print(f"Loaded file : {filename}")
print(f"File size   : {len(raw)} bytes")
print()

# ------------------------------------------------------------
# Parse JSON
# ------------------------------------------------------------
try:

    parsed = json.loads(raw)

except Exception as e:

    print("JSON parse failed:")
    print(e)

    sys.exit(1)

# ------------------------------------------------------------
# Find records
# ------------------------------------------------------------
records = find_records(parsed)

if records is None:

    print("Could not locate message records.")
    sys.exit(1)

print(f"Records found: {len(records)}")
print()

# ------------------------------------------------------------
# Decode records
# ------------------------------------------------------------
decoded_rows = []

label_stats = defaultdict(int)

parity_good = 0
parity_bad = 0

for i, rec in enumerate(records):

    if "word" not in rec:
        continue

    word = rec["word"]

    d = decode_arinc(word)

    if d["parity_ok"]:
        parity_good += 1
    else:
        parity_bad += 1

    row = {

        "index": i,

        "timestamp_ms": rec.get("ts_ms"),

        "channel": rec.get("channel"),

        "direction": rec.get("direction"),

        "word_hex": d["raw_hex"],

        "label_oct": d["label_oct"],

        "label_dec": d["label_dec"],

        "sdi": d["sdi"],

        "data_hex": d["data_hex"],

        "data_dec": d["data_dec"],

        "ssm": d["ssm"],

        "parity_bit": d["parity_bit"],

        "parity_ok": d["parity_ok"],
    }

    decoded_rows.append(row)

    label_key = (
        d["label_dec"],
        d["label_oct"],
        d["sdi"]
    )

    label_stats[label_key] += 1


# ============================================================
# PARITY SUMMARY
# ============================================================

print("======================================================")
print(" PARITY SUMMARY")
print("======================================================")
print()

print(f"GOOD : {parity_good}")
print(f"BAD  : {parity_bad}")

if parity_bad == 0:

    print()
    print("Parity appears VALID.")

else:

    print()
    print("WARNING: parity failures detected")

print()

# ============================================================
# LABEL SUMMARY
# ============================================================

print("======================================================")
print(" LABEL SUMMARY")
print("======================================================")
print()

# SORT BY LABEL NUMBER
sorted_labels = sorted(
    label_stats.items(),
    key=lambda x: (x[0][0], x[0][2])
)

print(
    f"{'LABEL_OCT':>10} "
    f"{'LABEL_DEC':>10} "
    f"{'SDI':>5} "
    f"{'COUNT':>10}"
)

print("-" * 42)

for (label_dec, label_oct, sdi), count in sorted_labels:

    print(
        f"{label_oct:>10} "
        f"{label_dec:10d} "
        f"{sdi:5d} "
        f"{count:10d}"
    )

print()

# ============================================================
# EXPORT decoded.csv
# ============================================================

decoded_csv = "decoded.csv"

with open(decoded_csv, 'w', newline='') as f:

    writer = csv.DictWriter(
        f,
        fieldnames=list(decoded_rows[0].keys())
    )

    writer.writeheader()

    for row in decoded_rows:
        writer.writerow(row)

print(f"Wrote: {decoded_csv}")

# ============================================================
# EXPORT label_summary.csv
# ============================================================

summary_csv = "label_summary.csv"

with open(summary_csv, 'w', newline='') as f:

    writer = csv.writer(f)

    writer.writerow([
        "label_oct",
        "label_dec",
        "sdi",
        "count"
    ])

    for (label_dec, label_oct, sdi), count in sorted_labels:

        writer.writerow([
            label_oct,
            label_dec,
            sdi,
            count
        ])

print(f"Wrote: {summary_csv}")

print()

# ============================================================
# Ask before terminal dump
# ============================================================

view = input("Open interactive terminal viewer? (y/n): ")

if view.lower() != 'y':

    print()
    print("Done.")
    print()

    sys.exit(0)

# ============================================================
# INTERACTIVE MESSAGE VIEWER
# ============================================================

print()
print("======================================================")
print(" MESSAGE DUMP")
print("======================================================")
print()

print(
    f"{'IDX':>5} "
    f"{'TIME(ms)':>13} "
    f"{'CH':>3} "
    f"{'DIR':>4} "
    f"{'LABEL':>6} "
    f"{'SDI':>3} "
    f"{'DATA_HEX':>10} "
    f"{'DATA_DEC':>10} "
    f"{'SSM':>3} "
    f"{'PAR':>3} "
    f"{'VALID':>6}"
)

print("-" * 95)

PAGE_SIZE = 100

start = 0

while start < len(decoded_rows):

    end = min(start + PAGE_SIZE, len(decoded_rows))

    for row in decoded_rows[start:end]:

        print(
            f"{row['index']:5d} "
            f"{row['timestamp_ms']:13} "
            f"{row['channel']:3} "
            f"{str(row['direction']).upper():>4} "
            f"{row['label_oct']:>6} "
            f"{row['sdi']:3d} "
            f"{row['data_hex']:>10} "
            f"{row['data_dec']:10d} "
            f"{row['ssm']:3d} "
            f"{row['parity_bit']:3d} "
            f"{str(row['parity_ok']):>6}"
        )

    start += PAGE_SIZE

    if start < len(decoded_rows):

        print()

        user = input(
            f"-- Showing {start}/{len(decoded_rows)} rows -- "
            f"Press ENTER for more or Q to quit: "
        )

        if user.lower() == 'q':
            break

        print()

print()
print("Done.")
print()