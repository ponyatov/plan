log.log: init.4th VM.py
	python VM.py $< > $@ && tail $(TAIL) $@
