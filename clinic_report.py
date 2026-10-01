#!/usr/bin/env python3
"""Summarize one week of clinic encounters and save the two report files."""

from pathlib import Path

from vitals_tools import (
    count_patients,
    mean_systolic,
    patients_at_or_above,
    systolic_readings,
)


DATA_PATH = Path("data") / "clinic_encounters.csv"
OUTPUT_DIR = Path("output")


def read_encounters(data_path):
    """
    Read the encounter file and return (enouncters, skipped).
    
    Each usable encounter is a dictionary with keys "patient_id" and "systolic".
    """

    with data_path.open("r", encoding="utf-8") as data_file:
        rows = data_file.readlines()
    
    encounters = []
    skipped = 0
    for row in rows[1:]:  # Skip the header line
        if not row.strip():
            print("Skipping a blank row.")
            skipped += 1
            continue
        fields = row.strip().split(",")
        if len(fields) != 3:
            print(f"Skipping a row with {len(fields)} fields: {row.strip()}")
            skipped += 1
            continue
        patient_id, visit_date, raw_systolic = fields
        try:
            systolic = int(raw_systolic)
        except ValueError as error:
            print(f"Skipping {patient_id}: {error}")
            skipped += 1
        else:
            if not (60 <= systolic <= 250):
                print(f"Skipping {patient_id}: Systolic reading {systolic} is not plausible.")
                skipped += 1
                continue
            encounters.append({"patient_id": patient_id, "systolic": systolic})
    return encounters, skipped


def main():
    """TODO: describe the two artifacts this writes."""
    encounters, skipped = read_encounters(DATA_PATH)

    # TODO: build the six report lines and write them to output/vitals_report.txt.
    # TODO: read the file back and print it, so you can see what was saved.
    # TODO: choose your follow-up cutoff, then write output/followup_list.txt
    #       with the Cutoff line, the Reason line, and one patient ID per line.


if __name__ == "__main__":
    main()
