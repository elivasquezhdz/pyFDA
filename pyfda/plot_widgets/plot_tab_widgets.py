# -*- coding: utf-8 -*-
"""
Tabbed container with all plot widgets

Author: Christian Münker
"""
from __future__ import print_function, division, unicode_literals, absolute_import

from ..compat import QTabWidget, QVBoxLayout, QEvent, QtCore, QSizePolicy


from pyfda.plot_widgets import (plot_hf, plot_phi, plot_pz, plot_tau_g, plot_impz,
                          plot_3d)

#------------------------------------------------------------------------------
class PlotTabWidgets(QTabWidget):
    def __init__(self, parent):
        super(PlotTabWidgets, self).__init__(parent)

        self.pltHf = plot_hf.PlotHf(self)
        self.pltPhi = plot_phi.PlotPhi(self)
        self.pltPZ = plot_pz.PlotPZ(self)
        self.pltTauG = plot_tau_g.PlotTauG(self)
        self.pltImpz = plot_impz.PlotImpz(self)
        self.plt3D = plot_3d.Plot3D(self)

        self._init_UI()

#------------------------------------------------------------------------------
    def _init_UI(self):
        """ Initialize UI with tabbed subplots """
        self.tabWidget = QTabWidget(self)
        self.tabWidget.setObjectName("plot_tabs")
        self.tabWidget.addTab(self.pltHf, '|H(f)|')
        self.tabWidget.addTab(self.pltPhi, 'phi(f)')
        self.tabWidget.addTab(self.pltPZ, 'P/Z')
        self.tabWidget.addTab(self.pltTauG, 'tau_g')
        self.tabWidget.addTab(self.pltImpz, 'h[n]')
        self.tabWidget.addTab(self.plt3D, '3D')

        layVMain = QVBoxLayout()
        layVMain.addWidget(self.tabWidget)
        layVMain.setContentsMargins(1,1,1,1)#(left, top, right, bottom)
#
        self.setLayout(layVMain)
        self.timer_id = QtCore.QTimer()
        self.timer_id.setSingleShot(True)
        # redraw current widget at timeout (timer was triggered by resize event):
        self.timer_id.timeout.connect(self.current_tab_redraw)

        # When user has selected a different tab, call self.tab_changed for a redraw
        self.tabWidget.currentChanged.connect(self.current_tab_redraw)
        # The following does not work: maybe current scope must be left?
        # self.tabWidget.currentChanged.connect(self.tabWidget.currentWidget().redraw) # 

        self.tabWidget.installEventFilter(self)

#------------------------------------------------------------------------------
        
#    @QtCore.pyqtSlot(int)
#    def tab_changed(self,argTabIndex):
    def current_tab_redraw(self):
        self.tabWidget.currentWidget().redraw()
            
#------------------------------------------------------------------------------
    def eventFilter(self, source, event):
        """
        Filter all events generated by the QTabWidget. Source and type of all
         events generated by monitored objects are passed to this eventFilter,
        evaluated and passed on to the next hierarchy level.
        
        This filter stops and restarts a one-shot timer for every resize event.
        When the timer generates a timeout after 500 ms, current_tab_redraw is 
        called by the timer.
        """
        if isinstance(source, QTabWidget):
            if event.type() == QEvent.Resize:
                self.timer_id.stop()
                self.timer_id.start(500)

        # Call base class method to continue normal event processing:
        return super(PlotTabWidgets, self).eventFilter(source, event)

#------------------------------------------------------------------------------
    def update_data(self):
        """ Calculate subplots with new filter DATA and redraw them """
        self.pltHf.draw()
        self.pltPhi.draw()
        self.pltPZ.draw()
        self.pltTauG.draw()
        self.pltImpz.draw()
        self.plt3D.draw()

#------------------------------------------------------------------------------
    def update_view(self):
        """ Update plot limits with new filter SPECS and redraw all subplots """
        self.pltHf.update_view()
        self.pltPhi.update_view()
        self.pltTauG.update_view()
        self.pltImpz.update_view()
#        self.pltPZ.draw()
#        self.plt3D.draw()
        
#------------------------------------------------------------------------

def main():
    import sys
    from pyfda import pyfda_rc as rc
    from ..compat import QApplication
    
    app = QApplication(sys.argv)
    app.setStyleSheet(rc.css_rc)

    mainw = PlotTabWidgets(None)
    mainw.resize(300,400)
    
    app.setActiveWindow(mainw) 
    mainw.show()
    
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    main()
