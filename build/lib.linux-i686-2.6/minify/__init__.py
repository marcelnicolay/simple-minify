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
 
__version__ = '0.0.1'

import os
from group import Group

class Minify():
    
    groups = []
    
    '''
    '''
    def __init__(self):
        pass
            
    def add_group(self, name=None, files=[], output=None, root=None):
        self.groups.append(Group(name=name, files=files, output=output, root=root))

    def minimalize(self):
        
        for group in self.groups:
            group.process()