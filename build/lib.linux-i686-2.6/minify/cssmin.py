#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
Simple CSS Minifier.
Code were created by Rafał Jońca.
The code is available on double license: GPL and MIT.
"""

import re

# Constants for use in compression level setting.
NONE = 0
SIMPLE = 1
NORMAL = 2
FULL = 3

_REPLACERS = {
  NONE: (None),                           # dummy
  SIMPLE: ((r'\/\*.{4,}?\*\/', ''),       # comment
           (r'\n\s*\n', r"\n"),           # empty new lines
           (r'(^\s*\n)|(\s*\n$)', "")),   # new lines at start or end
  NORMAL: ((r'/\*.{4,}?\*/', ''),         # comments
           (r"\n", ""),                   # delete new lines
           ('[\t ]+', " "),               # change spaces and tabs to one space
           (r'\s?([;:{},+>])\s?', r"\1"), # delete space where it is not needed, change ;} to }
           (r';}', "}"),                  # because semicolon is not needed there
           (r'}', r"}\n")),               # add new line after each rule
  FULL: ((r'\/\*.*?\*\/', ''),            # comments
         (r"\n", ""),                     # delete new lines
         (r'[\t ]+', " "),                # change spaces and tabs to one space
         (r'\s?([;:{},+>])\s?', r"\1"),   # delete space where it is not needed, change ;} to }
         (r';}', "}")),                   # because semicolon is not needed there
}

class CssMin:
  def __init__(self, level=NORMAL):
      self.level = level

  def compress(self, css):
      """Tries to minimize the length of CSS code passed as parameter. Returns string."""
      css = css.replace("\r\n", "\n") # get rid of Windows line endings, if they exist
      for rule in _REPLACERS[self.level]:
          css = re.compile(rule[0], re.MULTILINE|re.UNICODE|re.DOTALL).sub(rule[1], css)
      return css

def minimalize(css, level=NORMAL):
  """Compress css using level method and return new css as a string."""
  return CssMin(level).compress(css)
