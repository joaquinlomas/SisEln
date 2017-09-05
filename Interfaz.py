from __future__ import  division
import sys, scipy.stats
from PyQt4 import QtGui, uic, QtCore
import pyqtgraph as pg
import numpy as np
from scipy import signal

class Interfaz(QtGui.QMainWindow):
    def __init__(self,parent=None):
        super(Interfaz,self).__init__(parent)
        self.ui=uic.loadUi("Interfaz.ui",self) #Carga la mesa de Dj
        layout=self.ui.gridLayout
        
        
        self.frecuencia=40000      
        self.duty_cycle=50
        self.setduty_cycle=50
        self._conectado = False
         
         
         #Borrar desde aqui  
    
              
        self.plotWidget=pg.PlotWidget(name="Plot")
        self.plotWidget.setMouseEnabled(x=False,y=False)
        self.plotWidget.setYRange(-1,6)
        self.plotWidget.setXRange(-1.2/self.frecuencia,1.2/self.frecuencia)
        self.plotWidget.showGrid(x=True,y=True,alpha=(0.8))
        layout.addWidget(self.plotWidget)
        self.width = 512*8
        #BORRAR DESDE ACA SAPO REQLO 
        self.t = np.linspace(-1.5/self.frecuencia,1.5/self.frecuencia,self.width,endpoint=False)
        self.ydata=(5/2)*(1+signal.square(2*np.pi*self.frecuencia*self.t,duty=((self.duty_cycle)/100.0)))#+self.noise
        self.pwm = pg.PlotCurveItem(self.t, self.ydata, pen=pg.mkPen('g', width=2.0),
                      name='Pulso PWM',stepMode=False,fillLevel=None)
        self.plotWidget.addItem(self.pwm)
        
        
        
        #Hasta aqui si no funciona
        self._timer = QtCore.QTimer(self)
        self._timer.setInterval(100)
        self._timer.timeout.connect(self.updateGraph)
        self.ui.Slider.valueChanged.connect(self.updateGraph)
        self.ui.Slider_2.valueChanged.connect(self.updateGraph)
        self.a = 0
        
         
             
        #Asignar Rangos y los valores iniciales
        #Conectar las widget a el cambio de valores de frecuencia y duty
        self._timer = QtCore.QTimer(self)
        self._timer.setInterval(100)
        self.ui.prueba.clicked.connect(self.conectar)
        self.ui.dial.setRange(10000,50000)
        self.ui.Slider.setRange(10000,50000)
        self.ui.Slider.setValue(self.frecuencia)
        self.ui.dial.setValue(self.frecuencia)
        self.ui.Slider_2.setRange(0,100)
        self.ui.dial_2.setRange(0,100)
        self.ui.Slider_2.setValue(self.duty_cycle)
        self.ui.dial_2.setValue(self.duty_cycle)
        #Conectar las widget a el cambio de valores de frecuencia y duty
        self.ui.prueba.setText(u"Exit")
        self.ui.pushButton_2.setText(u"Update Plot")
    def setFreq(self,val1):
       self.frecuencia=val1
       self.setDc(self.duty_cycle)
    def setDc(self,val2): 
        self.duty_cycle=val2

        
    def setTimer(self):
        if self.a==0:
            self.ui.pushButton_2.setText(u"Stop Updating")
            self.ui.label.setText(u"PWM Monitor - Updating")      
            self.a = 1
        else:
            self.ui.pushButton_2.setText(u"Update Plot")
            self.ui.label.setText(u"PWM Monitor")
            self.a=0
        
    def updateGraph(self):
        if self.a == 1:
           self.ydata = (5/2)*(1+signal.square(2*np.pi*self.frecuencia*self.t,duty=((self.duty_cycle)/100.0)))
           self.pwm.setData(self.t,self.ydata)
        

            
    def conectar(self):
        if self._conectado:
           self.comms.close()
           self._conectado = False
           self.ui.prueba.setText('Connect')
        else:
            self.comms.setPort(str(self.ui.list.currentText()))
            self.comms.open()
            self.ui.prueba.setText('Disconnect')
            self._conectado = True
            
 
   
       
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    main_window = Interfaz()
    main_window.show()
    sys.exit(app.exec_())
