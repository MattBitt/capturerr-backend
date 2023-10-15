#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

# BUILTIN modules
import os
from pprint import pprint

from capturerrbackend.config.configurator import config


def test_config() -> None:
    assert config.env == "test"


# ---------------------------------------------------------

if __name__ == "__main__":
    Form = argparse.ArgumentDefaultsHelpFormatter
    description = (
        "A utility script to test the configurator.py file with different environments."
    )
    parser = argparse.ArgumentParser(description=description, formatter_class=Form)
    parser.add_argument(
        "environment",
        type=str,
        choices=["dev", "test", "prod", "stage"],
        help="Specify ENVIRONMENT to use",
    )
    args = parser.parse_args()

    # To be able to test different environments we need
    # to set this BEFORE we import the config module.
    os.environ["ENVIRONMENT"] = args.environment
    pprint(config.model_dump())
