#!/usr/bin/env python3
"""
Write a function called filter_datum that returns the log message obfuscated:
Arguments:
fields : a list of strings representing all fields to obfuscate
redaction : a string representing by what the field will be obfuscated
message : a string representing the log line
separator : a string representing by which character is separating all fields in the log line
( message )
The function should use a regex to replace occurrences of certain field values.
"""
import re
import logging

def filter_datum(fields, redaction, message, separator):
    for field in fields:
        message = re.sub(rf"(?<={field}=)(.*?)(?={separator})", redaction, message)
    return message

class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class"""
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"
    def __init__(self, fields):
        super().__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        record.msg = filter_datum(self.fields, self.REDACTION,
                     record.msg, self.SEPARATOR)
        return super().format(record)
