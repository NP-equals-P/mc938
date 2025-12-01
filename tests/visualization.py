from .nist_tests import NIST_results
from . import BATTERY, results_folder

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

from math import ceil

class TestVisualizer:

    def __init__(self, results=None):
        super().__init__()
        self.results = dict()
        self.add_results(results)

    def add_results(self, results):
        if isinstance(results, dict):
            self.results = results
        elif isinstance(results, NIST_results):
            self.results[results.get_name()] = results
        elif isinstance(results, list):
            for res in results:
                self.results[res.get_name()] = res
    
    def remove_results(self, name):
        del self.results[name]

    def _get_grouped_stats(self):
        names = []
        passed = []
        scores = []
        eligible = []
        for name, result in self.results.items():
            names.append(name)
            passed.append(result.get_pass_count())
            scores.append(result.get_mean_score())
            eligible.append(result.get_eligible_count())
        return names, passed, scores, eligible
    
    def _get_stat_per_test(self, stat_list, test_name):
        test_stats = [
            stats[test_name] for stats in stat_list
        ]
        return test_stats
    
    def _get_all_test_stats(self, stat_list):
        stats_per_tests = {
            test_name: [] for test_name in BATTERY.keys()
        }
        for stats in stat_list:
            for test_name, stat in stats.items():
                stats_per_tests[test_name].append(stat)
        return stats_per_tests
    
    def _get_ordered_test_stats(self, stats:NIST_results, test_seq):
        ordered_stats = []
        for test in test_seq:
            ordered_stats.append(stats[test])
        return ordered_stats
    
    def _format_xtick_label(self, label, line_ch_lim=10):
        label_words = " ".join(label.split("_")).title().split(" ")
        cum_len = 0
        form_lbl_words = []
        for word in label_words:
            form_lbl_words.append(word)
            cum_len += len(word)
            if cum_len > line_ch_lim:
                form_lbl_words.append("\n")
                cum_len = 0
            else:
                form_lbl_words.append(" ")
        if form_lbl_words[-1] == "\n":
            form_lbl_words.pop()
        return "".join(form_lbl_words)

    
    def show_compared_stats(
            self, 
            stat="passed"
    ):
        names, passed, scores, eligible = self._get_grouped_stats()

        match stat:
            case "passed":
                stats = passed
                title = "Times passed on each test"
            case "scores":
                stats = scores
                title = "Average P1 Score"
            case "eligibility":
                stats = eligible
                title = "Eligibility for the tests"
        

        tests = list(BATTERY.keys())
        fig, ax = plt.subplots(layout="constrained")
        width = 0.4
        fig_width = width*(len(names)*len(tests))
        fig.set_figwidth(fig_width)
        xtick_dist = width * (len(names) + 1)
        x = np.arange(len(tests)) * xtick_dist
        multiplier = 0
        y_max = 0.0

        for i in range(len(names)):
            offset = multiplier * width
            y = self._get_ordered_test_stats(stats[i], tests)
            if stat == "scores":
                y = np.round(y, decimals=2)
            rects = ax.bar(x + offset, y, width, label=names[i])
            ax.bar_label(rects, padding=3)
            multiplier += 1
            y_max = max(y_max, float(np.array(y).max()))

        leg_lines = ceil(len(names)/3)
        extra_yticks = 0.3 * y_max * leg_lines
        leg_box_h = 0.102 * leg_lines


        ax.set_title(label=title)
        legend = ax.legend(
            ncols=3, fancybox=True, shadow=True,
            bbox_to_anchor=(0., 0.995 - leg_box_h, 1., leg_box_h), loc='lower left',
            mode="expand", borderaxespad=0.
        ) #FIXME Puxar caixa de legendas para baixo do gráfico

        form_tests = [self._format_xtick_label(t) for t in tests]
        ax.set_ylim(top=y_max + extra_yticks)
        ax.set_xlim(left=-width, right=float((x+offset)[-1])+width)
        ax.set_xticks(x + (len(names) - 1)*width*0.5, form_tests, rotation=90)

        fig.savefig(os.path.join(results_folder, f"{stat}_comparison.png"))




    

    