#!/usr/bin/env python

# This file extracts interesting data points for use in graphs and/or tables
# from data_parsed.py

import sys

from data_parsed import Data, data_all, data_first_only, data_first_and_fin, get_rational_data_discrete
from result_accumulator import ResultAccumulator as ResAcc

# max number of round 1 rational choices
MAX_R1_CHOICES = 13

# minimum number of choices required in round 2 data in order to consider the reslt
MIN_R2_CHOICES = 5

# which confidence intervals to generate (only valid choices are 90, 95, 99, and 9995)
INTERVALS = [95, 9995]

def simple_stats_table(out, precision):
    """
    Computes some basic statistics about the estimated impact of the
    zero-phenomenon for various round 1 rationality thresholds.
    """
    print >> out, ResAcc.get_latex_table_header('|c|c', '\\textbf{\\# Rational in Round 1} & \\textbf{\\# Samples} & ')
    for num_rational_in_r1 in range(3,MAX_R1_CHOICES+1):
        data = get_rational_data_discrete(data_first_and_fin, num_rational_in_r1, num_rational_in_r1, MIN_R2_CHOICES)
        round2_rationalities = [(1.0-d.rationality(2))*100.0 for d in data]
        ra = ResAcc(round2_rationalities)
        ra.compute_stats(True)
        extra = '%u & %u & ' % (num_rational_in_r1, len(data))
        print >> out, extra + ra.get_latex_row(precision, INTERVALS)
    print >> out, ResAcc.get_latex_table_footer()

def main():
    f = open('dat/simple_stats.tex', 'w')
    simple_stats_table(f, 2)
    f.close()
    return 0

if __name__ == "__main__":
    sys.exit(main())
