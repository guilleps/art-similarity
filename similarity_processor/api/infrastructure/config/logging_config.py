import logging

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,  # DEBUG para más detalle
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[logging.StreamHandler()]
    )
