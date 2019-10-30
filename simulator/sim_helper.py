#!/usr/bin/env python
import matplotlib.pyplot as plt
import numpy as np


def my_plot(q, t, label, color=None, mean_in_legend=False, linewidth=0.5):
    if mean_in_legend:
        mean_total_q = np.average(q[:-1], weights=np.diff(t))
        plt.plot(t, q, color=color,
                 label='{} {:.2f}'.format(label, mean_total_q),
                 linewidth=linewidth)
    else:
        plt.plot(t, q, color=color, label='{}'.format(label),
                 linewidth=linewidth)


def get_mean_std(means, axis=1):
    return means.mean(axis=axis), np.zeros_like(means.mean(axis=axis))


class SimulatorSimple:
    def __init__(self, namegen, runtag, save):
        self.namegen = namegen
        self.runtag = runtag
        self.save = save

    def run(self, sim, max_steps, label, verbose=False, plot_stride=100,
            log_steps=None, plot_1=True):

        if log_steps is None:
            log_steps = max_steps // 4

        metrics1 = np.zeros(max_steps // plot_stride)
        metrics2 = np.zeros(max_steps // plot_stride)
        event_times = np.zeros(max_steps // plot_stride)

        for i in range(max_steps):
            if i % log_steps == 0 and verbose:
                print("{}/{}".format(i, max_steps))
                sim.print_state(verbose)

            sim.step()
            metrics1[i // plot_stride] = sim.metric1
            metrics2[i // plot_stride] = sim.metric2
            event_times[i // plot_stride] = sim.cur_time

        if plot_1:
            my_plot(metrics1, event_times, label)
        else:
            my_plot(metrics2, event_times, label)

        if self.save:
            npz_filename = self.namegen.get_output_filename(
                self.runtag, label, 'npz')
            np.savez(npz_filename,
                     metrics1=metrics1,
                     metrics2=metrics2,
                     event_times=event_times)

    def load(self, label, new_label, plot_1=True, mean_in_legend=True,
             linewidth=1):
        npz_filename = self.namegen.get_output_filename(
            self.runtag, label, 'npz')
        metrics1 = np.load(npz_filename)['metrics1']
        metrics2 = np.load(npz_filename)['metrics2']
        event_times = np.load(npz_filename)['event_times']

        if plot_1:
            my_plot(metrics1, event_times, new_label,
                    mean_in_legend=mean_in_legend, linewidth=linewidth)
        else:
            my_plot(metrics2, event_times, new_label,
                    mean_in_legend=mean_in_legend, linewidth=linewidth)

    def finalize_plot(self, xlabel='Time', ylabel='Jobs in System', extra_tag="",
                      sci_axis=False, fontsize=12, legend_size=6):
        plt.legend(loc='best', prop={'size': legend_size})
        if sci_axis:
            plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0),
                                 fontsize=fontsize)

        plt.xlabel(xlabel, fontsize=fontsize)
        plt.ylabel(ylabel, fontsize=fontsize)

        plt.tight_layout(pad=1.4)

        self.namegen.save_plot(self.runtag, extra_tag, skip_eps=True)
        plt.show()


class SimulatorSeries:
    def __init__(self, namegen, runtag, save):
        self.namegen = namegen
        self.runtag = runtag
        self.save = save

        self.reps = None
        self.values = None
        self._n = None

        self.labels = []
        self.series_avg_metric1 = {}
        self.series_avg_metric2 = {}
        self.series_avg_metric1h = {}
        self.series_avg_metric2h = {}
        self.has_run = {}

    def init_series(self, reps, values, labels):
        self.values = values
        self.labels = []
        n = len(values)

        self._n = n
        self.reps = reps

        for label in labels:
            self.init_label(label)

    def init_label(self, label):
        n = self._n
        reps = self.reps
        self.series_avg_metric1[label] = np.zeros((n, reps))
        self.series_avg_metric2[label] = np.zeros((n, reps))
        self.series_avg_metric1h[label] = np.zeros((n, reps))
        self.series_avg_metric2h[label] = np.zeros((n, reps))
        self.has_run[label] = False
        self.labels.append(label)

    def run(self, ri, vi, sim, max_steps, label, plot_stride=100,
            log_steps=None, verbose=False):

        if log_steps is None:
            log_steps = max_steps // 4

        metrics1 = np.zeros(max_steps // plot_stride)
        metrics2 = np.zeros(max_steps // plot_stride)
        event_times = np.zeros(max_steps // plot_stride)

        for i in range(max_steps):
            if i % log_steps == 0 and verbose:
                print("{}/{}".format(i, max_steps))

            sim.step()
            metrics1[i // plot_stride] = sim.metric1
            metrics2[i // plot_stride] = sim.metric2
            event_times[i // plot_stride] = sim.cur_time

        if label not in self.series_avg_metric1:
            self.init_label(label)

        self.series_avg_metric1[label][vi, ri] = \
            np.average(metrics1[:-1], weights=np.diff(event_times))

        self.series_avg_metric2[label][vi, ri] = metrics2[-1]
        # np.average(metrics2[:-1], weights=np.diff(event_times))

        self.series_avg_metric1h[label][vi, ri] = \
            np.average(metrics1[:-1][max_steps // plot_stride // 2:],
                       weights=np.diff(event_times)[
                               max_steps // plot_stride // 2:])

        self.series_avg_metric2h[label][vi, ri] = \
            np.average(metrics2[:-1][max_steps // plot_stride // 2:],
                       weights=np.diff(event_times)[
                               max_steps // plot_stride // 2:])

        self.has_run[label] = True

    def plot_save_all_series(self, plot_1=False, markersize=10, plot_h=False):
        for label in self.labels:
            self.plot_save_series(label, plot_1, markersize, plot_h)

    def plot_save_series(self, label, plot_1=True, markersize=10, plot_h=False):
        if not self.has_run[label]:
            return

        if plot_1:
            if plot_h:
                data = self.series_avg_metric1h
            else:
                data = self.series_avg_metric1
        else:
            if plot_h:
                data = self.series_avg_metric2h
            else:
                data = self.series_avg_metric2

        means, stds = get_mean_std(data[label])
        plt.errorbar(self.values, means, yerr=stds, fmt='o-',
                     markersize=markersize, label=label)

        if self.save:
            npz_filename = self.namegen.get_output_filename(
                self.runtag, label, 'npz')
            np.savez(npz_filename,
                     series_avg_metric1=self.series_avg_metric1[label],
                     series_avg_metric1h=self.series_avg_metric1h[label],
                     series_avg_metric2=self.series_avg_metric2[label],
                     series_avg_metric2h=self.series_avg_metric2h[label])

    def load(self, label, new_label, plot_1=True, markersize=10,
             verbose=False, plot_h=False, index_from=0, index_to=None,
             linewidth=1, fmt="o-"):

        npz_filename = self.namegen.get_output_filename(
            self.runtag, label, 'npz')

        if plot_1:
            if plot_h:
                series_avg_metric1h = np.load(npz_filename)['series_avg_metric1h']
                data = series_avg_metric1h
            else:
                series_avg_metric1 = np.load(npz_filename)['series_avg_metric1']
                data = series_avg_metric1
        else:
            if plot_h:
                series_avg_metric2h = np.load(npz_filename)['series_avg_metric2h']
                data = series_avg_metric2h
            else:
                series_avg_metric2 = np.load(npz_filename)['series_avg_metric2']
                data = series_avg_metric2

        if verbose:
            print("Data for {}: {}".format(label, data))

        if index_to is None:
            index_to = len(data)

        means, stds = get_mean_std(data)
        plt.plot(self.values[index_from:index_to], means[index_from:index_to],
                 fmt, label=new_label, markersize=markersize,
                 linewidth=linewidth)

    def finalize_plot(self, xlabel, ylabel, sci_axis=False,
                      extra_tag="", legend_size=6, fontsize=12):
        plt.legend(loc='best', prop={'size': legend_size})
        if sci_axis:
            plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0),
                                 fontsize=fontsize)

        plt.xlabel(xlabel, fontsize=fontsize)
        plt.ylabel(ylabel, fontsize=fontsize)

        plt.tight_layout(pad=1.4)
        self.namegen.save_plot(self.runtag, extra_tag, skip_eps=True)
        plt.show()
