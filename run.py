#!/usr/bin/env python
# -*- coding:UTF-8 -*-

from app import app

if __name__ == '__main__':
    app.debug = app.config.get('DEBUG')
    port = app.config.get('PORT')
    app.secret_key = app.config.get('SECRET_KEY')
    app.run(host = "0.0.0.0", port = port)