# -*- coding: utf-8 -*-
from app import app
from os import environ

app.run(port=environ.get("PORT", 5000), host='0.0.0.0')
