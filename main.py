#!/usr/bin/env python
import json
import os
import sys

import jwt

ICON_ROOT = '/System/Library/CoreServices/CoreTypes.bundle/Contents/Resources'

ICON_ERROR = os.path.join(ICON_ROOT, 'AlertStopIcon.icns')
ICON_INFO = "jwt.png"


class WorkFlow:

    def __init__(self):
        self.items = []

    def add_item(
            self, title: str, subtitle: str, 
            arg: str, autocomplete: str, icon: str=ICON_INFO
    ):
        self.items.append(
            {
                "uid": "desktop",
                "type": "string",
                "title": title,
                "subtitle": subtitle,
                "arg": arg,
                "autocomplete": autocomplete,
                "icon": icon,
            }
        )

    def run(self, args: str):
        if len(args.split('.')) == 2:
            args = "{}.xxxx".format(args)
        elif len(args.split('.')) == 1:
            args = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.{}.xxxx".format(args)

        try:
            res = jwt.decode(
                args,
                "secret",
                algorithms=["HS256"],
                options={"verify_signature": False},
                issuer="auth",
                verify=False
            )
        except Exception as e:
            self.add_item("Error", str(e), "", "", ICON_ERROR)
        else:
            for key, value in res.items():
                value = str(value)
                self.add_item(value, key, value, value)

        json.dump({"items": self.items}, sys.stdout)

        sys.stdout.flush()


if __name__ == '__main__':
    s = sys.argv
    wf = WorkFlow()
    wf.run(s[1])
