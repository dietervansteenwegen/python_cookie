#! /usr/bin/python3
# -*- coding: utf-8 -*-
# vim: ts=4:sw=4:expandtab:cuc:autoindent:ignorecase:colorcolumn=99

REQUIRED_PACKAGES: list = [
    "uv",
    #     "ruff",
    #     "pre-commit",
]

print(
    "\n---> This template requires the following packages and tools to be installed: ",
    end="",
)
print(", ".join([f"[{package}]" for package in REQUIRED_PACKAGES]))
