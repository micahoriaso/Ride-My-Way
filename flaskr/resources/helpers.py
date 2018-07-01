import re

def match_email(email):
    email_pattern = re.compile(
        '(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'
        )

    return email_pattern.match(email)

def strip_whitespace(string):
    return string.replace(" ", "")
