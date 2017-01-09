__author__ = 'paul'
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from graphlib import Graph, MeshLinePlot
from os.path import dirname, abspath
import files.datadump
import os
from kivy.uix.slider import Slider

class SimResultScreen(BoxLayout):
    def __init__(self, parentapp, simobj):
        super (SimResultScreen, self).__init__(orientation='vertical')
        self.parentapp = parentapp
        self.simobj = simobj
        graphmodule = self.getGraphModule(simobj)
        self.zoomslider = Slider(orientation='horizontal', min=-100, max=100, value=0, size_hint=(1, .1))
        self.zoomslider.bind(value=self.onZoomSliderChange)

        self.add_widget(graphmodule)
        self.add_widget(self.zoomslider)

        bottombar = BoxLayout(orientation='horizontal',size_hint=(1.0,0.1))
        datadumpbutton = Button(text='Save Result...')
        datadumpbutton.bind(on_press=self.dumpcallback)
        backbutton = Button(text='Back')
        backbutton.bind(on_press=self.backcallback)
        bottombar.add_widget(backbutton)
        bottombar.add_widget(datadumpbutton)
        self.add_widget(bottombar)

    def getGraphModule(self, simobj):
        respool = simobj.carmodel.respool
        bat = respool.batteryChargeAh
        g = SimUnitPlot('battery charge', bat)
        #self.add_widget(g)
        v = respool.velocityms
        gv = SimUnitPlot('velocity', v)
        return g

    def backcallback(self, instance):
        self.parentapp.showStartScreen()

    def dumpcallback(self, instance):
        #should refactor this into simobj.writeoutput or something. UI shouldn't really contain datadumping code, just call into it.
        parentDirectory = dirname(dirname(abspath('__path__')))
        targetDirectory = os.path.join(parentDirectory, "outputData")

        if not os.path.isdir(targetDirectory):
            os.mkdir(targetDirectory)

        data = files.datadump.getCSVData(self.simobj.carmodel.respool)
        files.datadump.dumpdata(os.path.join(targetDirectory, 'testdump.csv'), data)

    def onZoomSliderChange(self, instance, value):
        print('my value changed to %s' % value)
        return;


class SimUnitPlot(Graph):
    minwidth = 10#seconds
    numPlots=0
    isPlotted=False
    def __init__(self, title, solarres):
        bounds=solarres.getMinMax()
        Graph.__init__(self,
        x_ticks_major=60*60*60*24, y_ticks_major=500000,
        y_grid_label=True, x_grid_label=True, padding=5,
        x_grid=True, y_grid=True, xmin=bounds[0], xmax=bounds[1], ymin=bounds[2], ymax=bounds[3],
                       width=2000, height=500)
        self.unittype='test'
        tempplotdata = solarres.hist

        plot = MeshLinePlot(color=[1,0,0,1])
        plot.points = tempplotdata
        self.add_plot(plot)

        return
