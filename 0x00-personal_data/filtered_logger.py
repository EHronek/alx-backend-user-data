#!/usr/bin/env python3
"""Defines a function returns the log message obfuscated"""
import re


def filter_datum(fields, redaction, message, separator):
    """obfuscate specified fields in a log message"""
    return re.sub(
            rf'({"|".join(fields)})=[^{separator}]*', rf'\1={redaction}',
            message)
