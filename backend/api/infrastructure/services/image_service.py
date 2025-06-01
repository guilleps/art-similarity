import uuid
from datetime import datetime, timezone

def generate_id_for_image():
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    random_number = str(uuid.uuid4().int)[:6]
    return f"{timestamp}{random_number}"