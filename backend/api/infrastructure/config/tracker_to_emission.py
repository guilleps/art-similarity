import os
from dotenv import load_dotenv
from codecarbon import EmissionsTracker


def create_tracker_to_emission(filename: str):
    is_prod = os.environ.get("PRODUCTION", "false") == "true"

    if is_prod:
        return EmissionsTracker(
            project_name="ArtShift",
            experiment_id="e0f3a9ae-b84d-4bc3-bda2-0ff6ab5842a9",
            save_to_file=False,
            save_to_api=True,
            output_dir="/tmp",
        )
    else:
        os.makedirs("./carbon_reports", exist_ok=True)
        return EmissionsTracker(
            project_name="ArtShift",
            experiment_id="e0f3a9ae-b84d-4bc3-bda2-0ff6ab5842a9",
            output_dir="./carbon_reports",
            output_file=filename,
            save_to_file=True,
            save_to_api=True,
        )
