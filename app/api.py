#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""api.py: Setup FastAPI."""

__author__ = "Dewynter Antoine AKA Warwin"
__credits__ = ["Dewynter Antoine AKA Warwin"]
__version__ = "1.0"
__status__ = "Developement"

from fastapi import FastAPI
from app.routes.index import user

app= FastAPI()

app.include_router(user)
