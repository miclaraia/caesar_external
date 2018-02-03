#!/usr/bin/env python
################################################################
# Main entrypoint

import caesar_external
from caesar_external import ui

import logging
logger = logging.getLogger(caesar_external.__name__)


def main():
    try:
        ui.run()
    except Exception as e:
        logger.critical(e)
        raise e


if __name__ == "__main__":
    main()
