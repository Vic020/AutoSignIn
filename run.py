#!/usr/bin/env python
# -*- coding: utf-8 -*-
import webbrowser
from web import app


def main():
    app.debug = False
    webbrowser.open_new_tab('http://127.0.0.1:8080')
    app.run(port=8080)

if __name__ == '__main__':
    main()
