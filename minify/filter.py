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

import re
import os
from minify import Minify
from exception import FilterTemplateDoesNotExist

class FilterTemplate():
    
    
    '''
    	FilterTemplate
    	@template_path
    	@media_dir
    	@css_output css path output
    	@js_output js path output
    '''
    def __init__(self, template_path, media_dir, css_output, js_output):
        self.template_path = template_path
        self.media_dir = media_dir
        self.css_output = css_output
        self.js_output = js_output
    
    def read(self, file):
        if not os.path.isfile(file):
            raise FilterTemplateDoesNotExist("Template does not exist")
        
        f = open(file)
        try:
            lines = []
            for line in f:
                lines.append(line)
        finally:
            f.close()
        
        return "".join(lines)
    
    def apply(self):
    	dirlist = os.listdir(self.template_path)
    	
    	minify = Minify()
    	
        for fname in dirlist:
        	search = re.search("(?P<name>[^\.]*)\.(?P<extension>.*)$",fname)
        	if search and search.groupdict()['extension'] == 'tpl':
				template_file = "%s/%s" % (self.template_path, fname)

         		css_files, js_files = self.filter(template_file)
	        	
	        	output_css = "%s/minify/%s.css" % (self.css_output, search.groupdict()['name'])
	        	output_js = "%s/minify/%s.js" % (self.js_output, search.groupdict()['name'])
	        	
        		minify.add_group(files=css_files, output=output_css, root=self.media_dir )
        		minify.add_group(files=js_files, output=output_js, root=self.media_dir )

	        	self.parse(template_file, output_css, output_js)
		
		minify.minimalize()

    def write(self, file, content):
        f = open(file, "w")
        try:
            f.write(content)
        finally:
            f.close()
		
	def filter(self, template_file):
		content = self.read(template_file)
		
		css_files = []
		js_files = []

		links = re.findall('\<link[^>]*/>',content)
		scripts = re.findall('\<script[^>]*></script>',content)

		for link in links:
			search = re.search('href="(?P<value>[^"]*)"', link)			
			if search:
				css_files.append(search.groupdict()['value'])

		for script in scripts:
			search = re.search('src="(?P<value>[^"]*)"', script)
			if search:
				js_files.append(search.groupdict()['value'])
		
		return css_files, js_files	

	def parse(self, template_file, output_css, output_js):	
     	content = self.read(template_file)
     	
     	content = re.sub("\<link[^>]*/>", "", content)
     	content = re.sub("\<script[^>]*></script>", "", content)
     	
     	content = re.sub("</head>", '<link type="text/css" href="%s" rel="stylesheet" />\n</head>' % output_css, content)
     	content = re.sub("</body>", '<script type="text/javscript" src="%s" ></script>\n</body>' % output_js, content)
     	
     	self.write(template_file, content)
