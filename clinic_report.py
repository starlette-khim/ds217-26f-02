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
    """Write the vitals report and the follow-up list to output/."""

    encounters, skipped = read_encounters(DATA_PATH)

    readings  = systolic_readings(encounters)

    lines = [
        f"Usable encounters: {len(encounters)}",
        f"Skipped rows: {skipped}",
        f"Patients seen: {count_patients(encounters)}",
        f"Mean systolic: {mean_systolic(readings)} mmHg",
        f"Highest systolic: {max(readings)} mmHg",
        f"Lowest systolic: {min(readings)} mmHg"
    ]
    report_text = "\n".join(lines) + "\n"

    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    report_path = output_dir / "vitals_report.txt"
    with open(report_path, "w", encoding="utf-8") as report_file:
        report_file.write(report_text)

    with open(report_path, "r", encoding="utf-8") as report_file:
        saved_text = report_file.read()
    
    print(f"Read back from {report_path:}")
    print(saved_text, end="")
    print(f"Saved report matches: {saved_text == report_text}")
    assert saved_text == report_text, "The saved report does not match the text we built."

    print(f"Checkpoint passed: {len(lines)} lines saved to {report_path}")

    cutoff = 140
    reason = "140 mmHg is the stage 3 hypertension threshold, so these patients most need follow-up care."

    followup_patients = sorted(patients_at_or_above(encounters, cutoff))
    
    followup_lines = [
        f"Cutoff: {cutoff} mmHg",
        f"Reason: {reason}",
    ] + followup_patients
    followup_text = "\n".join(followup_lines) + "\n"

    followup_path = output_dir / "followup_list.txt"
    with open(followup_path, "w", encoding="utf-8") as followup_file:
        followup_file.write(followup_text)
    
    with open(followup_path, "r", encoding="utf-8") as followup_file:
        saved_followup_text = followup_file.read()

    print(f"Read back from {followup_path}:")
    print(saved_followup_text, end="")
    assert saved_followup_text == followup_text, "The saved follow-up list does not match the text we built."

    print(f"Checkpoint passed: {len(followup_lines)} lines saved to {followup_path}")


if __name__ == "__main__":
    main()
