#!/usr/bin/env python
#-*- coding:utf-8 -*-
 
# Copyright Marcel Nicolay <marcel.nicolay@gmail.com>
 
# Licensed under the Open Software License ("OSL") v. 3.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
 
#     http://www.opensource.org/licenses/osl-3.0.php
 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from jsmin import jsmin
from cssmin import CssMin
from exception import FileDoesNotExist
import os, re, StringIO

class MinifyCompressor():
    
    def read_file(self, file):
        if not os.path.isfile(file):
            raise FileDoesNotExist("File does not exist %s" % file)
        
        f = open(file)
        try:
            lines = []
            for line in f:
                lines.append(line)
        finally:
            f.close()
        
        return "".join(lines)
    
    def write_file(self, content, file_output):
        f = open(file_output, "w")
        try:
            f.write(content)
        finally:
            f.close()
    
    def get_merged_files(self):
        files_in = []

        for file in self.files:
            files_in.append(self.read_file(self.media_dir + file))
            
        return "".join(files_in)
        
class JsCompressor(MinifyCompressor):

    def __init__(self, files=[], file_output=None, media_dir=None):
        self.files = files
        self.file_output = file_output
        self.media_dir = media_dir
        
    def run(self):
        merged_files = self.get_merged_files()
        
        content = jsmin(merged_files)
        #content = merged_files
        
        self.write_file(content, self.media_dir + self.file_output)
        
        return self.media_dir + self.file_output

class CssCompressor(MinifyCompressor):

    def __init__(self, files=[], file_output=None, media_dir=None):
        self.files = files
        self.file_output = file_output
        self.media_dir = media_dir

    def run(self):
        merged_files = self.get_merged_files()

        cssm = CssMin()
        content = cssm.compress(merged_files)

        self.write_file(content, self.media_dir + self.file_output)
        
        return self.media_dir + self.file_output
        
