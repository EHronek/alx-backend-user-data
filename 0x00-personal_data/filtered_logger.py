#!/usr/bin/env python3
"""Defines a function returns the log message obfuscated"""
import re
from typing import List
import logging
import os
import mysql.connector

PII_FIELDS = ("name", "email", "phone", "ssn", "password")
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


def get_logger() -> logging.Logger:
    """creates and returns a logger object"""
    user_logger = logging.getLogger("user_data")
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    user_logger.setLevel(logging.INFO)
    user_logger.propagate = False
    user_logger.addHandler(stream_handler)
    return user_logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Returns a connector to Mysql db using env variables"""
    username = os.getenv('PERSONAL_DATA_DB_USERNAME', default='root')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST ', 'localhost')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')

    if not db_name:
        raise ValueError("Database name missing")
    try:
        conn = mysql.connector.connect(
            user=username,
            password=password,
            host=host,
            port=3306
            database=db_name
        )
        return conn
    except mysql.connector.Error as e:
        raise ConnectionError(f"Failed to connect database: {e}")


def main():
    """retrieves and displays filtered user data"""
    logger = get_logger()

    db_conn = get_db()
    cursor = db_conn.cursor(dictionary=True)
    fields = "name,email, phone,ssn,password,ip,last_login,user_agent"
    columns=fields.split(',')
    query="SELECT {} FROM users;".format(fields)
    with db_conn.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            record = map(
                lambda x: '{}={}'.format(x[0], x[1]),
                zip(columns, row),
            )
            msg = '{};'.format('; '.join(list(record)))
            args = ("user_data", logging.INFO, None, None, msg, None, None)
            log_record = logging.LogRecord(*args)
            logger.handle(log_record)
