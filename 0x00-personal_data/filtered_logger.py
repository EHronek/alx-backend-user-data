#!/usr/bin/env python3
"""Defines a function returns the log message obfuscated"""
import re
from typing import List
import logging

patterns = {
    'extract': lambda x, y: r'(?P<field>{})=[^{}]*'.format('|'.join(x), y),
    'replace': lambda x: r'\g<field>={}'.format(x),
}


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """obfuscate specified fields in a log message"""
    extract, replace = (patterns["extract"], patterns["replace"])
    return re.sub(extract(fields, separator), replace(redaction), message)

class RedactingFormatter(logging.Formatter):
    """Redacting formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Filters values in incoming log records using filter_datum"""
        msg = super(RedactingFormatter, self).format(record)
        txt = filter_datum(self.fields,  self.REDACTION, msg, self.SEPARATOR)
        return txt

