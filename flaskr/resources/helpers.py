import re

from flask_restful import abort

def match_email(email):
    email_pattern = re.compile(
        '(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'
        )

    return email_pattern.match(email)

def strip_whitespace(string):
    return string.replace(" ", "")

def check_for_empty_fields(args):
    for k, v in args.items():
        if v == "":
            abort(500, message='Please fill in the field {}'.format(k))
