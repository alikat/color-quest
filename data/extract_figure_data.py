#!/usr/bin/env python

# This file extracts interesting data points for use in graphs and/or tables
# from data_parsed.py

import sys

from data_parsed import Data, data_all, data_first_only, data_first_and_fin, get_rational_data_discrete
from result_accumulator import ResultAccumulator as ResAcc

# max number of round 1 rational choices
MAX_R1_CHOICES = 13

# which confidence intervals to generate (only valid choices are 90, 95, 99, and 9995)
INTERVALS = [95, 9995]

def simple_stats_table(out, precision, c):
    """
    Computes some basic statistics about the estimated impact of the
    zero-phenomenon for various round 1 rationality thresholds.
    @param c  minimum number of choices required for consideration
    """
    print >> out, ResAcc.get_latex_table_header('|c|c', '\\textbf{\\# Rational in Round 1} & \\textbf{\\# Samples} & ')
    for num_rational_in_r1 in range(0,MAX_R1_CHOICES+2):
        if num_rational_in_r1 == MAX_R1_CHOICES+1:
            l = 3
            u = 13
            title = 'ALL'
            print >> out, '\\hline'
        else:
            l = num_rational_in_r1
            u = num_rational_in_r1
            title = str(u)
        data = get_rational_data_discrete(data_first_and_fin, l, u, c)
        round2_rationalities = [(1.0-d.rationality(2))*100.0 for d in data]
        ra = ResAcc(round2_rationalities)
        ra.compute_stats(True)
        extra = '%s & %u & ' % (title, len(data))
        print >> out, extra + ra.get_latex_row(precision, INTERVALS)
    print >> out, ResAcc.get_latex_table_footer()

def rationality_scatter_plot(out_dat, plot_name, c):
    print >> out_dat, '# Round1Rationality Round2Rationality'
    for d in data_first_and_fin:
        print >> out_dat, '%f\t%f\n' % (d.rationality(1)*100.0, d.rationality(2)*100.0)

    out_plot = open('figures/' + plot_name + '.gnuplot', 'w')
    print >> out_plot, '''
unset title
unset label
set autoscale
set size 1.0, 1.0

set xlabel "%% of Round 1 Trades which were Rational"
set grid x
set xr [0:100]

set ylabel "%% of Round 2 Trades which were Rational"
set grid y
set yr [0:100]

set terminal postscript eps color enhanced linewidth 3 dashed
set output "%s.eps"

set style line 1 lt 1 lw 2 lc rgb "#000000" pt 2

plot "../dat/%s.dat" using 1:2 with points ls 1
''' % (plot_name, plot_name)
    out_plot.close()

def main():
    min_round2_choices_thresholds = [1, 3, 5, 10, 14]

    for i in min_round2_choices_thresholds:
        f = open('dat/simple_stats_%u.tex' % i, 'w')
        simple_stats_table(f, 1, i)
        f.close()

        f = open('dat/rationality_scatter_%u.dat' % i, 'w')
        rationality_scatter_plot(f, 'rationality_scatter_%u' % i, i)
        f.close()

    return 0

if __name__ == "__main__":
    sys.exit(main())
