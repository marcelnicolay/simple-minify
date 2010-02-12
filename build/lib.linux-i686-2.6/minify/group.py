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

import os, re, StringIO

class Group():

    isJsFile = False
    isCssFile = False
    
    def __init__(self, name, files, output, root):
        self.name = name
        self.files = files
        self.output = output
        self.root = root
        
        self.detect_type(files[0])
        
    def detect_type(self, file):
        if re.search('\.js$', file):
            self.isJsFile = True
        else:
            self.isCssFile = True
            
    def read_file(self, file):
        file_path = self.root + file
        if not os.path.isfile(file_path):
            raise Exception()
        
        f = open(file_path)
        try:
            lines = []
            for line in f:
                lines.append(line)
        finally:
            f.close()
        
        return "\n".join(lines)
    
    def write_file(self, content, output):
        file_path = self.root + output
        f = open(file_path, "w")
        try:
            f.write(content)
        finally:
            f.close()
    
    def process(self):
        comb = self.combined()
        
        if self.isJsFile:
            content = jsmin(comb)
        elif self.isCssFile:
            cssm = CssMin()
            content = cssm.compress(comb)

        self.write_file(content, self.output)
        
    def combined(self):
        files_in = []

        for file in self.files:
            files_in.append(self.read_file(file))
            
        return "\n".join(files_in)
