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

class FilterTemplate():
    
    
    
    def __init__(self, path):
        self.path = path
    
    def read(self, file):
        if not os.path.isfile(file):
            raise Exception()
        
        f = open(file)
        try:
            lines = []
            for line in f:
                lines.append(line)
        finally:
            f.close()
        
        return "\n".join(lines)
        
    def parse(self, content):
    
    	css_files = []
    
    	links = re.findall('\<link[^>]*/>',content)
    	for link in links:
	    	result = re.search('href="(?P<value>[^"]*)"', link).groupdict()
	    	if result
	    		css_files.append(result['value'])
	    		
	    		
	    return css_files

	
            
    
    
