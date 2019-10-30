import os
import time

import matplotlib.pyplot as plt
import numpy as np


# def my_plot(y, t, label, color=None, mean_in_legend=False, linewidth=0.5):
#     if mean_in_legend:
#         mean_total_y = np.dot(t, y) / t.sum()
#         plt.plot(t.cumsum(), y, color=color,
#                  label='{} {:.2f}'.format(label, mean_total_y),
#                  linewidth=linewidth)
#     else:
#         plt.plot(t.cumsum(), y, color=color, label='{}'.format(label),
#                  linewidth=linewidth)


class NameGen(object):
    def __init__(self, filetag, output_folder='experiment_outputs'):
        os.makedirs(output_folder, exist_ok=True)

        self.filetag = filetag
        self.output_folder = output_folder

    def get_output_prefix(self, exptag, label):
        label = label.replace(" ", "")
        return os.path.join(self.output_folder,
                            '{}_{}{}'.format(self.filetag, label, exptag))

    def get_output_filename(self, exptag, label, ext):
        return '{}.{}'.format(self.get_output_prefix(exptag, label), ext)

    def save_plot(self, tag, label='', dpi=300, skip_eps=False):
        plt.draw()

        png_filename = self.get_output_filename(tag, label, 'png')
        plt.savefig(png_filename, dpi=dpi)
        if not skip_eps:
            eps_filename = self.get_output_filename(tag, label, 'eps')
            plt.savefig(eps_filename, dpi=dpi)
        pdf_filename = self.get_output_filename(tag, label, 'pdf')
        plt.savefig(pdf_filename, dpi=dpi)


class Timer(object):
    def __init__(self, name=None, logger=None):
        self.name = name
        if logger is None:
            self.log_f = print
        else:
            self.log_f = logger.info

    def __enter__(self):
        self.t_start = time.time()
        if self.name is None:
            self.log_f('Starting timer')
        else:
            self.log_f('Starting {}'.format(self.name))

    def __exit__(self, exc_type, exc_value, traceback):
        if self.name is None:
            self.log_f('Elapsed time: {0:.2f}s'
                       .format(time.time() - self.t_start))
        else:
            self.log_f('Elapsed time for {1}: {0:.2f}s'
                       .format(time.time() - self.t_start, self.name))