#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import argparse
import time
import re
import logging
import uuid
import shutil

from slugify import slugify
from models import Module
from parsers import FantasyGrounds

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    # parse arguments
    parser = argparse.ArgumentParser(description="Convert .mod files from Fantasy Grounds to Encounter+")
    parser.add_argument("path", metavar="PATH", help="a path to .mod file or .xml file")
    parser.add_argument("--debug", action="store_true", default=False, help="enable debug logs")
    parser.add_argument("--name", help="name")
    parser.add_argument("--author", help="author")
    parser.add_argument("--cover", help="author")
    parser.add_argument("--code", help="code")
    parser.add_argument("--id", help="id")
    args = parser.parse_args()

    if args.debug:
        logger.setLevel(logging.DEBUG)

    # create module
    module = Module()
    module.id = args.id or str(uuid.uuid4())
    module.name = args.name or "Unknown"
    module.slug = slugify(module.name)
    module.description = "Converted from FG"
    module.author = args.author or "Unknown"
    module.code = args.code
    module.image = args.cover or "Cover.jpg"

    # process with FG parser
    fg = FantasyGrounds()
    fg.process(args.path, module)