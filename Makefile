clean:
	@echo "Cleaning up build and *.pyc files..."
	@find . -name '*.pyc' -exec rm -rf {} \;
	@rm -rf build
	
unit: 
	@echo "Running simple-minify unit tests..."
	@cd minify && nosetests -s --verbose --with-coverage --cover-package=minify tests/unit/*
