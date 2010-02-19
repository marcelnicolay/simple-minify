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

import os

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
