# Makefile to build the plots

SRCS = $(wildcard *.gnuplot)
PNGS = $(SRCS:.gnuplot=.png)

.PHONY: default clean
.SUFFIXES: .gnuplot

default: $(PNGS)

# build the png file from gnuplot files
%.png : %.gnuplot
	gnuplot $<

# remove the graph outputs
clean:
	rm -f $(PNGS)
