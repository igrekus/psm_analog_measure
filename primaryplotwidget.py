import errno
import itertools
import os

from PyQt5.QtWidgets import QGridLayout, QWidget
from mytools.plotwidget import PlotWidget


class PrimaryPlotWidget(QWidget):

    params = {
        0: {
            '00': {
                'xlabel': 'F, ГГц',
                'xlim': [],
                'ylabel': 'S21, дБм',
                'ylim': []
            },
            '01': {
                'xlabel': 'F, ГГц',
                'xlim': [],
                'ylabel': 'КСВ вх, дБм',
                'ylim': []
            },
            '10': {
                'xlabel': 'F, ГГц',
                'xlim': [],
                'ylabel': 'КСВ вых, дБм',
                'ylim': []
            },
            '11': {
                'xlabel': 'F, ГГц',
                'xlim': [],
                'ylabel': 'φ ош, град',
                'ylim': []
            },
            '02': {
                'xlabel': 'V, В',
                'xlim': [0, 20],
                'ylabel': 'φ(v)',
                'ylim': [-100, 300]
            },
            '12': {
                'xlabel': 'F, ГГц',
                'xlim': [],
                'ylabel': 'S21 ош, дБ',
                'ylim': []
            },
            '03': {
                'xlabel': 'F, ГГц',
                'xlim': [],
                'ylabel': 'S21 ско',
                'ylim': []
            },
            '13': {
                'xlabel': 'F, ГГц',
                'xlim': [],
                'ylabel': 'helper',
                'ylim': []
            },
        },
    }

    def __init__(self, parent=None, result=None):
        super().__init__(parent)

        self._result = result
        self.only_main_states = False

        self._grid = QGridLayout()

        self._plotS21 = PlotWidget(parent=None, toolbar=True)
        self._plotVswrIn = PlotWidget(parent=None, toolbar=True)
        self._plotVswrOut = PlotWidget(parent=None, toolbar=True)
        self._plotS21PhaseErr = PlotWidget(parent=None, toolbar=True)
        self._plotS21PhaseRmse = PlotWidget(parent=None, toolbar=True)
        self._plotS21Err = PlotWidget(parent=None, toolbar=True)
        self._plotS21Rmse = PlotWidget(parent=None, toolbar=True)
        self._plotMisc = PlotWidget(parent=None, toolbar=True)

        self._grid.addWidget(self._plotS21, 0, 0)
        self._grid.addWidget(self._plotVswrIn, 0, 1)
        self._grid.addWidget(self._plotVswrOut, 1, 0)
        self._grid.addWidget(self._plotS21PhaseErr, 1, 1)
        self._grid.addWidget(self._plotS21PhaseRmse, 0, 2)
        # self._grid.addWidget(self._plotS21Err, 1, 2)
        # self._grid.addWidget(self._plotS21Rmse, 0, 3)
        # self._grid.addWidget(self._plotMisc, 1, 3)

        self.setLayout(self._grid)

        self._init()

    def _init(self, dev_id=0):

        def setup_plot(plot, pars: dict):
            plot.set_tight_layout(True)
            plot.subplots_adjust(bottom=0.150)
            # plot.set_title(pars['title'])
            plot.set_xlabel(pars['xlabel'], labelpad=-2)
            plot.set_ylabel(pars['ylabel'], labelpad=-2)
            # plot.set_xlim(pars['xlim'][0], pars['xlim'][1])
            # plot.set_ylim(pars['ylim'][0], pars['ylim'][1])
            plot.grid(b=True, which='major', color='0.5', linestyle='-')
            plot.tight_layout()

        setup_plot(self._plotS21, self.params[dev_id]['00'])
        setup_plot(self._plotVswrIn, self.params[dev_id]['01'])
        setup_plot(self._plotVswrOut, self.params[dev_id]['10'])
        setup_plot(self._plotS21PhaseErr, self.params[dev_id]['11'])
        setup_plot(self._plotS21PhaseRmse, self.params[dev_id]['02'])
        # setup_plot(self._plotS21Err, self.params[dev_id]['12'])
        # setup_plot(self._plotS21Rmse, self.params[dev_id]['03'])
        # setup_plot(self._plotMisc, self.params[dev_id]['13'])

    def clear(self):
        self._plotS21.clear()
        self._plotVswrIn.clear()
        self._plotVswrOut.clear()
        self._plotS21PhaseErr.clear()
        self._plotS21PhaseRmse.clear()
        self._plotS21Err.clear()
        self._plotS21Rmse.clear()
        # self._plotMisc.clear()

    def plot(self, dev_id=0):
        print('plotting primary stats')
        self.clear()
        self._init(dev_id)

        freqs = self._result.freqs
        s21s = self._result.s21
        vswr_in = self._result.vswr_in
        vswr_out = self._result.vswr_out
        phase_errs = self._result.phase_err
        phase_v = self._result.phase_v
        volts = self._result._volts
        # s21_err = self._result.s21_err
        # s21_rmse = self._result.s21_rmse
        # misc = self._result.misc

        n = len(s21s)

        for xs, ys in zip(itertools.repeat(freqs, n), s21s):
            self._plotS21.plot(xs, ys)

        for xs, ys in zip(itertools.repeat(freqs, n), vswr_in):
            self._plotVswrIn.plot(xs, ys)

        for xs, ys in zip(itertools.repeat(freqs, n), vswr_out):
            self._plotVswrOut.plot(xs, ys)

        for xs, ys in zip(itertools.repeat(freqs, n - 1), phase_errs):
            self._plotS21PhaseErr.plot(xs, ys)

        for xs, ys in zip(itertools.repeat(volts, len(phase_v)), phase_v):
            self._plotS21PhaseRmse.plot(xs, ys)

        # for xs, ys in zip(itertools.repeat(freqs, n), s21_err):
        #     self._plotS21Err.plot(xs, ys)
        #
        # for xs, ys in zip([freqs], [s21_rmse]):
        #     self._plotS21Rmse.plot(xs, ys)

        # for xs, ys in zip([freqs] * len(misc), misc):
        #     self._plotMisc.plot(xs, ys)

    def save(self, img_path='./image'):
        try:
            os.makedirs(img_path)
        except OSError as ex:
            if ex.errno != errno.EEXIST:
                raise IOError('Error creating image dir.')

        for plot, name in zip([self._plotS21, self._plotVswrIn, self._plotVswrOut, self._plotS21PhaseErr], ['stats.png', 'cutoff.png', 'delta.png', 'double-triple.png']):
            plot.savefig(img_path + name, dpi=400)


