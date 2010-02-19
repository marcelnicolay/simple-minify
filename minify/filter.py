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
from compressor import CssCompressor, JsCompressor
from exception import FilterTemplateDoesNotExist,FileDoesNotExist

class FilterTemplate():


    '''
    FilterTemplate
    @template_path
    @media_dir
    @css_path
    @js_path
    @media_url

    FilterTemplate("/home/marcel/workspace/simple-minify", "/home/marcel/workspace/labicyclette/web/public", "/css", "/js", "").run()
    '''
    def __init__(self, template_path, media_dir, css_path, js_path, media_url):
        self.template_path = template_path
        self.media_dir = media_dir
        self.css_path = css_path
        self.js_path = js_path

        self.media_url = media_url

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

        css_matchs = []
        js_matchs = []

        links = re.findall('\<link[^>]*/>',content)
        scripts = re.findall('\<script[^>]*></script>',content)

        for link in links:
            search = re.search('href="(?P<value>[^"]*)"', link)	
            if search and self.css_path in search.groupdict()['value']:
                css_files.append(search.groupdict()['value'])
                css_matchs.append(link)

        for script in scripts:
            search = re.search('src="(?P<value>[^"]*)"', script)
            if search and self.js_path in search.groupdict()['value']:
                js_files.append(search.groupdict()['value'])
                js_matchs.append(script)

        return css_files, js_files, css_matchs, js_matchs

    def parse(self, template_file, css_url=None, js_url=None, css_matchs=[], js_matchs=[]):
        content = self.read(template_file)

        # substitui a ultima ocorrencia
        content = re.sub(css_matchs.pop(), '<link type="text/css" href="%s" rel="stylesheet" />' % css_url, content)
        content = re.sub(js_matchs.pop(), '<script type="text/javscript" src="%s" ></script>' % js_url, content)
        
        # remove as outras
        for match in css_matchs + js_matchs:
                content = re.sub(match, "", content)

        self.write(template_file+".tmp", content)

    def run(self):
        dirlist = os.listdir(self.template_path)

        for fname in dirlist:
            search = re.search("(?P<name>[^\.]*)\.(?P<extension>.*)$",fname)
            if search and search.groupdict()['extension'] == 'html':
                template_file = "%s/%s" % (self.template_path, fname)

                css_files, js_files, css_matchs, js_matchs = self.filter(template_file)

                if css_files:
                    output_css = "%s/%s.min.css" % (self.css_path, search.groupdict()['name'])
                    compress = CssCompressor(files=css_files, file_output=output_css, media_dir=self.media_dir )
                    compress.run()
                    css_url = "%s/%s" % (self.media_url, output_css)

                if js_files:
                    output_js = "%s/%s.min.js" % (self.js_path, search.groupdict()['name'])
                    compress = JsCompressor(files=js_files, file_output=output_js, media_dir=self.media_dir )
                    compress.run()
                    js_url = "%s/%s" % (self.media_url, output_js)

                self.parse(template_file,css_url,js_url, css_matchs, js_matchs)
