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
        v =strip_whitespace(v)
        if v == "":
            abort(500, message='Please fill in the field {}'.format(k))

def check_if_integer(args):
    try:
        args = int(args)
    except ValueError:
        # it was a string, not an int.
        abort(500, message='{} should be a number'.format(args))