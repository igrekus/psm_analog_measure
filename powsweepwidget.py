from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget

from mytools.plotwidget import PlotWidget


class PowSweepWidget(QWidget):
    def __init__(self, parent=None, controller=None):
        super().__init__(parent=parent)
        self._controller = controller

        self._ui = uic.loadUi('powsweepwidget.ui', self)

        self._plot = PlotWidget(parent=None, toolbar=True)
        # self._ui.verticalLayout.addWidget(self._plot)
        self._ui.btnPowSweep.hide()

        self._init()

    def _init(self):
        self._plot.set_title('Прогон по мощности')
        self._plot.set_xlabel('F, GHz', labelpad=-2)
        self._plot.set_ylabel('Pow, dB', labelpad=-2)
        self._plot.set_xlim(4, 8)
        # self._plot.set_ylim(pars['ylim'][0], pars['ylim'][1])
        self._plot.grid(b=True, which='major', color='0.5', linestyle='-')
        self._plot.tight_layout()

    @pyqtSlot()
    def on_btnPowSweep_clicked(self):
        freqs, amps = self._controller.pow_sweep()
        self._plot.clear()
        self._init()

        self._plot.plot(freqs, amps)

