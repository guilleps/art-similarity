import os
from dotenv import load_dotenv
from codecarbon import EmissionsTracker

def create_tracker_to_emission(filename: str):
    is_prod = os.environ.get("PRODUCTION", "false") == "true"
    experiment_id = os.environ.get("EXPERIMENT_ID")

    if is_prod:
        return EmissionsTracker(
            project_name="ArtShift",
            experiment_id=experiment_id,
            save_to_file=False,
            save_to_api=True,
            output_dir="/tmp",
        )
    else:
        os.makedirs("./carbon_reports", exist_ok=True)
        return EmissionsTracker(
            project_name="ArtShift",
            experiment_id=experiment_id,
            output_dir="./carbon_reports",
            output_file=filename,
            save_to_file=True,
            save_to_api=True,
        )
