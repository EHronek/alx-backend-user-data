#!/usr/bin/env python3
"""Defines a function returns the log message obfuscated"""
import re

patterns = {
    'extract': lambda x, y: r'(?P<field>{})=[^{}]*'.format('|'.join(x), y),
    'replace': lambda x: r'\g<field>={}'.format(x),
}

def filter_datum(fields, redaction, message, separator):
    """obfuscate specified fields in a log message"""
    extract, replace = (patterns["extract"], patterns["replace"])
    return re.sub(extract(fields, separator), replace(redaction), message)
