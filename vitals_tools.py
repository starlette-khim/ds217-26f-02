"""Reusable helpers for summarizing clinic systolic readings."""


def systolic_readings(encounters):
    """Return the systolic readings stored in encounter records."""
    readings = [encounter["systolic"] for encounter in encounters]
    return readings


def mean_systolic(readings):
    """Return the average of the systolic readings, or None if there are no readings."""
    if not readings:
        return None
    return sum(readings) / len(readings)


def count_patients(encounters):
    """Return the number of distinct patients in the encounter records."""
    patient_ids = {encounter["patient_id"] for encounter in encounters}
    return len(patient_ids)


def patients_at_or_above(encounters, cutoff):
    """Return the IDs of patients whose systolic reading is at or above the cutoff."""
    return {encounter["patient_id"] for encounter in encounters if encounter["systolic"] >= cutoff}