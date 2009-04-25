.PHONY: default view clean

default:
	cd .. && ./extract_figure_data.py && cd dat
	pdflatex ex.tex

view: default
	acroread ex.pdf

clean:
	rm -f simple_stats*.tex ex.pdf ex.aux ex.out *.log
