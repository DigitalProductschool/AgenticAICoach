import logging

# File handler with overwrite mode
file_handler = logging.FileHandler("feature_clarity.log", mode='w')
file_handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))

# Stream (console) handler
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))

# Main application logger
logger = logging.getLogger("feature_clarity")
logger.setLevel(logging.INFO)

# Clear existing handlers to avoid duplication (especially in hot reload)
if logger.hasHandlers():
    logger.handlers.clear()

logger.addHandler(file_handler)
logger.addHandler(stream_handler)
