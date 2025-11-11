import os
import asyncio
from typing import Optional
from dotenv import load_dotenv
from codecarbon import EmissionsTracker
from asgiref.sync import sync_to_async
import logging

logger = logging.getLogger(__name__)


class EmissionTracker:

    def __init__(self, filename: str, experiment_id: Optional[str] = None):
        self.filename = filename
        self.experiment_id = experiment_id or os.environ.get("EXPERIMENT_ID")
        self.is_prod = os.environ.get("PRODUCTION", "false") == "true"
        self._tracker: Optional[EmissionsTracker] = None
        self._start_time = None

    async def start(self):
        try:
            self._tracker = await sync_to_async(self._create_tracker)()
            await sync_to_async(self._tracker.start)()
            logger.info(f"Emission tracker started: {self.filename}")
        except Exception as e:
            logger.error(f"Error starting emission tracker: {e}")

    def _create_tracker(self) -> EmissionsTracker:
        if self.is_prod:
            return EmissionsTracker(
                project_name="ArtShift",
                experiment_id=self.experiment_id,
                save_to_file=False,
                save_to_api=True,
                output_dir="/tmp",
                log_level="error",
            )
        else:
            os.makedirs("./carbon_reports", exist_ok=True)
            return EmissionsTracker(
                project_name="ArtShift",
                experiment_id=self.experiment_id,
                output_dir="./carbon_reports",
                output_file=self.filename,
                save_to_file=True,
                save_to_api=True,
                log_level="error",
            )

    async def stop_background(self):
        if self._tracker is None:
            return

        asyncio.create_task(self._stop_and_send())
        logger.info(f"Emission tracker stop scheduled in background: {self.filename}")

    async def _stop_and_send(self):
        try:
            await sync_to_async(self._tracker.stop)()
            logger.info(f"Emission data sent successfully: {self.filename}")
        except Exception as e:
            logger.error(f"Error stopping/sending emission data: {e}")


def create_async_tracker(filename: str) -> EmissionTracker:
    return EmissionTracker(filename=filename)
