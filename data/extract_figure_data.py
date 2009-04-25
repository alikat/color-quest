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

# whether to ignore results where round 2 is perfectly irrational: guess that
# people did not read the rules or were replaying for a high score with a new
# account
REMOVE_PERFECTLY_IRRATIONAL_ROUND_2 = False

def filter_common(data):
    if REMOVE_PERFECTLY_IRRATIONAL_ROUND_2:
        data = filter(lambda d : d.num_choices[2]!=d.num_rational[2], data)
    return data

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
        data = filter_common(get_rational_data_discrete(data_first_and_fin, l, u, c))
        round2_rationalities = [(1.0-d.rationality(2))*100.0 for d in data]
        ra = ResAcc(round2_rationalities)
        ra.compute_stats(True)
        extra = '%s & %u & ' % (title, len(data))
        print >> out, extra + ra.get_latex_row(precision, INTERVALS)
    print >> out, ResAcc.get_latex_table_footer()

def rationality_scatter_plot(out_dat, plot_name, c):
    print >> out_dat, '# Round1Rationality Round2Rationality'
    data = filter_common(data_first_and_fin)
    for d in data:
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

set terminal png
set output "%s.png"

set style line 1 lt 1 lw 2 lc rgb "#000000" pt 2

plot "../dat/%s.dat" using 1:2 with points ls 1
''' % (plot_name, plot_name)
    out_plot.close()

def score_versus_rationality_plot(out_dat, plot_name, min_rational_r1_choices, c, round_for):
    print >> out_dat, '# Score Round2Rationality'
    data = filter_common(get_rational_data_discrete(data_first_and_fin, min_rational_r1_choices, MAX_R1_CHOICES, c))
    points = []
    for d in data:
        t = (d.score, d.rationality(round_for)*100.0)
        points.append(t)

    points.sort()
    for p in points:
        print >> out_dat, '%f\t%f\n' % (p[0], p[1])

    out_plot = open('figures/' + plot_name + '.gnuplot', 'w')
    print >> out_plot, '''
unset title
unset label
set nokey
set autoscale
set size 1.0, 1.0

set xlabel "Score"
set grid x
set xr [70:240]

set ylabel "%% of Round %u Trades which were Rational"
set grid y
set yr [0:100]

set terminal png
set output "%s.png"

set style line 1 lt 1 lw 3 lc rgb "#000000" pt 2

plot "../dat/%s.dat" using 1:2 with linespoints ls 1
''' % (round_for, plot_name, plot_name)
    out_plot.close()

def rationality_cpdf_plot(out_dat, plot_name, min_rational_r1_choices, c, round_for, is_cdf):
    print >> out_dat, '# Rationality *DF'
    data = filter_common(get_rational_data_discrete(data_first_and_fin, min_rational_r1_choices, MAX_R1_CHOICES, c))
    rats = []
    for d in data:
        rats.append(int(d.rationality(round_for)*100.0))

    cdf = {}
    pdf = {}
    rats.sort()
    i = 0
    n = float(len(rats))
    for r in rats:
        i += 1
        cdf[r] = i / n
        if pdf.has_key(r):
            pdf[r] += (1 / n)
        else:
            pdf[r] = 1 / n

    for r in rats:
        df = cdf[r] if is_cdf else pdf[r]
        print >> out_dat, '%f\t%f\n' % (r, df*100.0)

    out_plot = open('figures/' + plot_name + '.gnuplot', 'w')
    print >> out_plot, '''
unset title
unset label
set nokey
set autoscale
set size 1.0, 1.0

set xlabel "%% of Round %u Trades which were Rational"
set grid x

set ylabel "%s"
set grid y
set yr [0:100]

set terminal png
set output "%s.png"

set style line 1 lt 1 lw 3 lc rgb "#000000" pt 2

plot "../dat/%s.dat" using 1:2 with linespoints ls 1
''' % (round_for, 'cdf' if is_cdf else 'pdf', plot_name, plot_name)
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

    MIN_R1_RATIONAL_TRADES = 10
    i = MIN_R2_TRADES = 5
    for round in [1,2]:
        name = 'score_versus_rationality%u_%u' % (round, i)
        f = open('dat/' + name + '.dat', 'w')
        score_versus_rationality_plot(f, name, MIN_R1_RATIONAL_TRADES, i, round)
        f.close()

    for round in [1,2]:
        for b in [True, False]:
            name = 'rationality%u_%s_%u' % (round, 'cdf' if b else 'pdf', i)
            f = open('dat/' + name + '.dat', 'w')
            rationality_cpdf_plot(f, name, MIN_R1_RATIONAL_TRADES, i, round, b)
            f.close()

    return 0

if __name__ == "__main__":
    sys.exit(main())
