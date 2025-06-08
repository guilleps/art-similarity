import logging
import sys

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,  # DEBUG -> más detalle
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            # logging.FileHandler('app.log') # archivo de registro
        ]
    )
