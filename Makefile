FORCE:

dist: FORCE
	@pyinstaller --add-data 'styles:styles' --onefile braindump.py

install: FORCE
	@sudo rm -rf /usr/local/bin/braindump
	@sudo cp dist/braindump /usr/local/bin/braindump
