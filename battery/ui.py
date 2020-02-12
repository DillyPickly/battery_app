#!/home/dylan/anaconda3/envs/battery/bin/python

from PyQt5 import QtWidgets, QtGui
from pyqtgraph import PlotWidget, plot
from PyQt5.QtCore import Qt
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import os

from battery_data import date_limits, get_data, update_data
from datetime import timedelta, datetime

def timestamp():
    return int(time.mktime(datetime.datetime.now().timetuple()))


class TimeAxisItem(pg.AxisItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setLabel(text='Time', units=None)
        self.enableAutoSIPrefix(False)

    def tickStrings(self, values, scale, spacing):
        return [datetime.fromtimestamp(value).strftime("%b %d %H:%M") for value in values]
        

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):        
        super(MainWindow, self).__init__(*args, **kwargs)
        # super(GraphicsWindow, self).__init__(*args, **kwargs)

        pg.setConfigOption('background', QtGui.QColor(41, 47, 49))
        pg.setConfigOption('foreground', 'w')
        

        self.graphWidget = pg.PlotWidget(labels = {'left': 'Laptop Battery %', 'bottom' : 'Time'},
                                        axisItems={'bottom': TimeAxisItem(orientation='bottom')})
        self.zoomGraph = pg.PlotWidget( labels = {'left': 'Laptop Battery %', 'bottom' : 'Time'},
                                        axisItems={'bottom': TimeAxisItem(orientation='bottom')})


        self.border = QtWidgets.QWidget()
        self.setCentralWidget(self.border)

        layout = QtGui.QVBoxLayout()
        layout.setContentsMargins(10,10,10,10)
        layout.addWidget(self.graphWidget)
        layout.addWidget(self.zoomGraph)
        self.border.setLayout(layout)

        lr = pg.LinearRegionItem([1.581E9,1.5811E9])
        self.graphWidget.addItem(lr)

        self.border.setAutoFillBackground(True)
        p = self.border.palette()
        p.setColor(self.border.backgroundRole(), QtGui.QColor(51, 57, 59))
        self.border.setPalette(p)

        pg.setConfigOptions(antialias=True)
        self.graphWidget.showGrid(x=True, y=True)
        self.zoomGraph.showGrid(x=True, y=True)


        def updatePlot():
            self.zoomGraph.setXRange(*lr.getRegion(), padding=0)
        def updateRegion():
            lr.setRegion(self.zoomGraph.getViewBox().viewRange()[0])
        lr.sigRegionChanged.connect(updatePlot)
        self.zoomGraph.sigXRangeChanged.connect(updateRegion)
        updatePlot()



        _light_green = (0  ,200,  20,150) #'#007000'
        _light_red   = (200, 20,  20,150)#'#D84315' #'#E65100' #'#D2222D'

        _green = (0  ,250, 20,150) #'#8BC34A' #'#CDDC39'
        _red   = (250, 20, 20,150)#'#FF9800' #'#FFB300' #'#FFCA28' #'#F39C12'

        delta = timedelta(weeks=1)

        date_time, percent, plugged, charging, unplugged = date_limits(*get_data(update_data()),delta)


        charge_dates = [d.timestamp() for d in charging[0]]
        unplugged_dates = [d.timestamp() for d in unplugged[0]]
        dates = [d.timestamp() for d in date_time]


        last = dates[-1]
        first = dates[0]
        self.graphWidget.setLimits(yMin=0,yMax=105, minYRange=105, xMax = last, xMin = first)
        self.zoomGraph.setLimits(yMin=0,yMax=105, minYRange=105, xMax = last, xMin = first)

        # Plotting the filled areas on the graph
        i_0 = 0
        toggle = plugged[0]
        date_0 = date_time[0]
        for i in range(1,len(plugged)):
            date = date_time[i]

            if date-date_0 > timedelta(minutes=3):
                pass
                if percent[i] > percent[i-1]:
                    self.graphWidget.plot(  dates[i-1:i+1], 
                                            percent[i-1:i+1], 
                                            pen=None, 
                                            fillLevel=0.0, 
                                            brush=_light_green)
                    self.zoomGraph.plot(  dates[i-1:i+1], 
                                            percent[i-1:i+1], 
                                            pen=None, 
                                            fillLevel=0.0, 
                                            brush=_light_green)

                else:
                    self.graphWidget.plot(  dates[i-1:i+1], 
                                            percent[i-1:i+1], 
                                            pen=None, 
                                            fillLevel=0.0, 
                                            brush=_light_red)
                    self.zoomGraph.plot(  dates[i-1:i+1], 
                                            percent[i-1:i+1], 
                                            pen=None, 
                                            fillLevel=0.0, 
                                            brush=_light_red)
                

                if toggle:
                    self.graphWidget.plot(  dates[i_0:i], 
                                            percent[i_0:i], 
                                            pen=None, 
                                            fillLevel=0.0, 
                                            brush=_green)
                    self.zoomGraph.plot(  dates[i_0:i], 
                                            percent[i_0:i], 
                                            pen=None, 
                                            fillLevel=0.0, 
                                            brush=_green)
                else:
                    self.graphWidget.plot(  dates[i_0:i], 
                                            percent[i_0:i], 
                                            pen=None, 
                                            fillLevel=0.0, 
                                            brush=_red)
                    self.zoomGraph.plot(  dates[i_0:i], 
                                            percent[i_0:i], 
                                            pen=None, 
                                            fillLevel=0.0, 
                                            brush=_red)
                

                i_0 = i

            elif toggle != plugged[i]:
                pass
                if toggle:
                    self.graphWidget.plot(  dates[i_0:i+1], 
                                            percent[i_0:i+1], 
                                            pen=None, 
                                            fillLevel=0.0, 
                                            brush=_green)
                    self.zoomGraph.plot(  dates[i_0:i+1], 
                                            percent[i_0:i+1], 
                                            pen=None, 
                                            fillLevel=0.0, 
                                            brush=_green)
                else:
                    self.graphWidget.plot(  dates[i_0:i+1], 
                                            percent[i_0:i+1], 
                                            pen=None, 
                                            fillLevel=0.0, 
                                            brush=_red)
                    self.zoomGraph.plot(  dates[i_0:i+1], 
                                            percent[i_0:i+1], 
                                            pen=None, 
                                            fillLevel=0.0, 
                                            brush=_red)

                i_0 = i

            elif i == len(plugged)-1:
                pass
                if plugged[i]:  
                    self.graphWidget.plot(  dates[i_0:i+1], 
                                            percent[i_0:i+1], 
                                            pen=None, 
                                            fillLevel=0.0, 
                                            brush=_green)
                    self.zoomGraph.plot(  dates[i_0:i+1], 
                                            percent[i_0:i+1], 
                                            pen=None, 
                                            fillLevel=0.0, 
                                            brush=_green)
                else:
                    self.graphWidget.plot(  dates[i_0:i+1], 
                                            percent[i_0:i+1], 
                                            pen=None, 
                                            fillLevel=0.0, 
                                            brush=_red)
                    self.zoomGraph.plot(  dates[i_0:i+1], 
                                            percent[i_0:i+1], 
                                            pen=None, 
                                            fillLevel=0.0, 
                                            brush=_red)

            toggle = plugged[i]
            date_0 = date 


def main():
    app = QtWidgets.QApplication(sys.argv)

    main = MainWindow()
    main.resize(800,400)
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()