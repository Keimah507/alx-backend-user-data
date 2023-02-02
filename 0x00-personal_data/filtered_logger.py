#!/usr/bin/env python3
"""Regexing"""
import re
import logging
from typing import List
import mysql.connector
from os import getenv

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List, redaction: str, message: str, separator: str) -> str:
    """Returns the log message obfuscated
    Arguments:
        fields: list of strings repping all fields to obfuscate
        redaction: str repping by what the field will be obfuscated
        message: a string representing the log line
        separator: a string representing by which character is separating all
         fields in the log line(message)
    Return: log message obfuscated"""
    for i in fields:
        message = re.sub(i + "=.*?" + separator,
                         i + "=" + redaction + separator, message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        return filter_datum(self.fields, self.REDACTION, super(RedactingFormatter, self).format(record),
                            self.SEPARATOR)


def get_logger() -> logging.Logger:
    """Takes no arguments and returns a logging.Logger object"""
    log = logging.getLogger('user_data')
    log.setLevel(logging.INFO)
    log.propagate = False

    sh = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    sh.setFormatter(formatter)
    log.addHandler(sh)

    return log


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
     connect to a secure holberton database to read a users table. The database
     is protected by a username and password that are set as environment
     variables on the server named PERSONAL_DATA_DB_USERNAME (set the default
     as “root”), PERSONAL_DATA_DB_PASSWORD (set the default as an empty string)
     and PERSONAL_DATA_DB_HOST (set the default as “localhost”).
    Returns: A connector to the database(mysql.connector.connection.MySQLConnection
    """
    db_connection = mysql.connector.connection.MySQLConnection(
        user=getenv('PERSONAL_DATA_DB_PASSWORD', 'root'),
        passwd=getenv('PERSONAL_DATA_DB_PASSWORD', ''),
        host=getenv('PERSONAL_DATA_DB_HOST', 'localhost'),
        database=getenv("PERSONAL_DATA_DB_NAME"),
    )

    return db_connection


def main():
    """
    obtain a database connection using get_db and retrieve all rows in the users table and display each row under a
    filtered format like this: [HOLBERTON] user_data INFO 2019-11-19 18:37:59,596: name=***; email=***; phone=***;
    ssn=***; password=***; ip=e848:e856:4e0b:a056:54ad:1e98:8110:ce1b; last_login=2019-11-14T06:16:24;
    user_agent=Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; KTXN);

    Filtered fields:

    name
    email
    phone
    ssn
    password
    Only your main function should run when the module is executed.

    Returns: Nothing
    """
    database = get_db()
    cursor = database.cursor
    cursor.execute("SELECT * FROM users;")
    fields = [i[0] for i in cursor.description]

    log = get_logger()

    for row in cursor:
        str_row = ''.join(f'{f}={str(r)}; ' for r, f in zip(row, fields))
        log.info(str_row.strip())

    cursor.close()
    database.close()


if __name__ == "__main__":
    main()
