import os, sys, atexit, getopt, re

def usage():
    print "\nPython Minify runner a command line Python script:"
    print "\nUsage: minify_runner.py [options] -- [args]\n"
    print "   --settings     settings"
    print "   --help         show this help\n"
    
def read_settings(file):

    if not os.path.isfile(file):
        raise Exception("setting's file invalid" + file)
        
    f = open(file)
    try:
        lines = []
        for line in f:
            if not line.startswith("#"):
                lines.append(line)
        content = "".join(lines)        
    finally:
        f.close()
    
    settings = {}
    rules = re.findall("(?P<attr>[^=]*)=(?P<value>[^\\n]*)", content)
    for rule in rules:
        settings[rule[0].strip()] = rule[1].strip()
    
    return settings

def main():

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hs", ["help", "settings=", ""])
    except getopt.GetoptError, err:
        print str(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)

    settings_file = "settings.conf"
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-s", "--settings"):
            settings_file = a
    
    print "python simple-minify runner start"
    print "\tminify runner reading setting's file..."
    settings = read_settings(settings_file)
    print "\tsetting's file good!"
    
    from filter import FilterTemplate
    filterTemplate = FilterTemplate(template_path = settings['TEMPLATE_PATH'], 
                                    media_dir = settings['MEDIA_DIR'], 
                                    css_path = settings['CSS_PATH'], 
                                    js_path = settings['JS_PATH'], 
                                    css_url_base = settings['CSS_URL_BASE'],
                                    js_url_base = settings['JS_URL_BASE'],
                                    img_url_base = settings['IMG_URL_BASE'],
                                    img_url_pattern = settings['IMG_URL_PATTERN'])

    print "\tfilter template runing..."
    filterTemplate.run()
    print "\tpython simple-minify runner SUCCESSFUL!"
    print "... see you ...\n"

if __name__ == "__main__":
    main()
