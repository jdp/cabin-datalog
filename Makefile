DIAGRAM=archdiagram.png

all: $(DIAGRAM)

lint:
	flake8 .

test:
	bash test.sh

%.png: %.gv
	dot -Tpng $< -o $@

.INTERMEDIATE: archdiagram.gv
archdiagram.gv:
	bash vizarch.sh > $@

clean:
	-rm $(DIAGRAM)

.PHONY: all lint test clean
