from .nist_tests import NIST_results
from . import BATTERY, results_folder
from .statistics import get_conf_interval, scale_passed

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import matplotlib.colors as mc
import colorsys

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

    def _get_grouped_pass_stats(self):
        names = []
        passed = []
        scores = []
        eligible = []
        for name, result in self.results.items():
            names.append(name)
            passed.append(result.get_pass_count())
            eligible.append(result.get_eligible_count())
        return names, passed, eligible
    
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
    
    def adjust_lightness(self, color, amount=0.5):
        try:
            c = mc.cnames[color]
        except:
            c = color
        c = colorsys.rgb_to_hls(*mc.to_rgb(c))
        return colorsys.hls_to_rgb(c[0], max(0, min(1, amount * c[1])), c[2])
    
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

    def _get_show_filter(
            self, test_names, eligible = None, hide_non_eligible=False
    ):
        show_filter = [True for _ in test_names]
        if hide_non_eligible:
            show_filter = np.array(
                [
                    [gen[test] for gen in eligible]
                    for test in test_names
                ]
            ).max(axis=1) > 0
        return show_filter

    def _plot_pass_vs_eligible(
            self,
            gen_names,
            test_names,
            passed,
            eligible,
            ax,
            x,
            width=0.4
    ):
        multiplier = 0
        y_max = 0.0
        max_tests = 0

        for i in range(len(gen_names)):
            offset = multiplier * width

            y_pass = np.array(self._get_ordered_test_stats(passed[i], test_names))

            # Plotar a contagem de elegibilidade
            elig = np.array(self._get_ordered_test_stats(eligible[i], test_names))
            y_elig_compl = elig - y_pass
            rects = ax.bar(
                x + offset, y_elig_compl, width, label=f"{gen_names[i]} - Eligible", 
                bottom=y_pass
            )
            ax.bar_label(rects, padding=5)

            # Plotar a contagem de aprovações
            color = rects[0].get_facecolor()
            rects = ax.bar(
                x + offset, y_pass, width, label=f"{gen_names[i]} - Passed", 
                color=self.adjust_lightness(color, 0.7)
            )
            ax.bar_label(rects, label_type='center', color=self.adjust_lightness(color, 1.5))

            multiplier += 1
            y_max = max(y_max, float(np.array(y_elig_compl).max()))
            max_tests = max(max_tests, elig.max())
            return ax, y_max
        
    def _plot_pass_freq_report(
            self,
            gen_names,
            test_names,
            passed,
            eligible,
            ax,
            x,
            total_tests,
            width=0.4
    ):
        
        multiplier = 0
        y_max = 0.0

        for i in range(len(gen_names)):
            offset = multiplier * width

            y_pass = np.array(self._get_ordered_test_stats(passed[i], test_names))
            elig = np.array(self._get_ordered_test_stats(eligible[i], test_names))
            y_pass_sc = np.round(scale_passed(y_pass, elig), 2)
            hatch_filter = [
                None if el >= 55 else "//"
                for el in elig
            ]

            # Plotar a frequência de testes passados por testes feitos
           
            rects = ax.bar(
                x + offset, y_pass_sc, width, label=f"{gen_names[i]}",
                hatch=hatch_filter
            )
            ax.bar_label(rects, padding=3)

            multiplier += 1
            y_max = max(y_max, float(np.array(y_pass_sc).max()))

        c_int = get_conf_interval(total_tests)
        lower_lim = c_int[0]
        lim_ticks = ax.get_xticks()
        lim_ticks[0] -= 0.5*width
        lim_ticks[-1] += 0.5*width

        limit = ax.hlines(
            lower_lim, lim_ticks[0], lim_ticks[-1], linestyles='dashed', 
            colors='red', label="Acceptance limit"
        )

        return ax, y_max

    def show_pass_report(
            self,
            test_names,
            gen_names,
            passed,
            eligible,
            graph_type,
            hide_non_eligible=True,
            num_leg_cols=3
    ):

        fig, ax = plt.subplots(layout="constrained")
        width = 0.4
        xtick_dist = width * (len(gen_names) + 1)

        show_filter = self._get_show_filter(
            test_names, eligible, hide_non_eligible
        )
        filtered_tests = np.array(test_names)[show_filter]

        x = np.arange(len(filtered_tests)) * xtick_dist

        match graph_type:
            case "count":
                ax, y_max = self._plot_pass_vs_eligible(
                    gen_names, filtered_tests, passed, eligible,
                    ax, x, width
                )
                filename = "pass_vs_eligible"
                title = "Pass Count Report"
            case "frequency":
                total_tests_each = np.array(
                    [res.get_total_tests() for res in self.results.values()]
                )
                assert total_tests_each.min() == total_tests_each.max(), \
                    f"Warning: total tests of each generator differ"
                total_tests = int(total_tests_each.max())
                ax, y_max = self._plot_pass_freq_report(
                    gen_names, filtered_tests, passed, eligible,
                    ax, x, total_tests, width
                )
                filename = "pass_freq_report"
                title = "Pass Frequency Report"

        leg_lines = ceil(len(gen_names)/num_leg_cols)
        extra_yticks = 0.3 * y_max * leg_lines
        leg_box_h = 0.102 * leg_lines


        ax.set_title(label=title)
        legend = ax.legend(
            ncols=num_leg_cols, fancybox=True, shadow=True,
            bbox_to_anchor=(0., 0.995 - leg_box_h, 1., leg_box_h), loc='lower left',
            mode="expand", borderaxespad=0.
        )

        form_tests = [self._format_xtick_label(t) for t in filtered_tests]
        fig_width = width*(len(gen_names)*len(filtered_tests))
        fig.set_figwidth(fig_width)
        ax.set_ylim(top=y_max + extra_yticks)
        offset = len(gen_names) * width
        x_max = float(x[-1]) + offset + width
        ax.set_xlim(left=-width, right=x_max)
        ax.set_xticks(x + (len(gen_names) - 1)*width*0.5, form_tests, rotation=90)

        fig.savefig(os.path.join(results_folder, f"{filename}.png"))

    def show_compared_stats(
            self, 
            hide_non_eligible=False,
            num_leg_cols=4
    ):
        tests = list(BATTERY.keys())
        gens, passed, eligible = self._get_grouped_pass_stats()
        for graph_type in ["count", "frequency"]:
            self.show_pass_report(
                tests, gens, passed, eligible, graph_type, 
                hide_non_eligible, num_leg_cols
            )
        




    

    