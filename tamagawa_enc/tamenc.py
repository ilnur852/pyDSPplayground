# -*- coding: utf-8 -*-
import sys
import os
import numpy as np
import serial 
import threading
import time
import binascii
from fixedpoint import FixedPoint
import serial.serialutil
import serial.tools
import serial.tools.list_ports
from ui_form import Ui_MainWindow
import PySide6.QtWidgets as QtWidgets
from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtGui import QColor as color

dval =0.0
fx = 0.1

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

class MainWindow(QtWidgets.QMainWindow):
    p = 0   
    ndata = QObject.__new__
    
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.m_ui = Ui_MainWindow()
        self.m_ui.setupUi(self)
        

if __name__ == "__main__":
    
    def serial_close():
        event.set()
        dn.join()
        sd.close()
        
    def serial_connect():
        comport = win.m_ui.comboBox.currentText()
        print(sd.port)
        if (comport != ''):
            sd.baudrate = 115200
            sd.port = comport
            sd.open()
            dn.start()
            print("port connected", comport)
            win.m_ui.pushButton.setText("Disconnect")
            win.m_ui.pushButton.clicked.connect(serial_close)
        win.m_ui.pushButton_2.clicked.connect(send_val)
        win.m_ui.horizontalScrollBar.valueChanged.connect(update_val)

    def display_num(event):
        while(True):
            if event.is_set():
                break
            time.sleep(0.05)
            win.m_ui.label.setText(str(win.m_ui.horizontalScrollBar.value()/1000)) 
            if (sd.in_waiting >= 10):
                r = sd.read_all()
                hexval = bytes.hex(r[2:5][::-1])
                intval = int(hexval, 16)
                degrees = (intval*360)/2**17
                degrees_f = "{:10.4f}".format(degrees)
                win.m_ui.lcdNumber.display(degrees_f)


    def send_val():
        try: 
            dval = float(win.m_ui.horizontalScrollBar.value()/1000)
        except: 
            dval = 0
        fx = FixedPoint(dval, m=8, n=24)
        print(bytes.fromhex(str(fx)))
        sd.write((bytes.fromhex(str(fx))))

    def update_val():
        if (win.m_ui.checkBox.isChecked() == True):
            send_val()       

    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sd = serial.Serial()
    event = threading.Event()
    dn = threading.Thread(target=display_num, args=(event,))
    win.m_ui.label.setText('i am here')  # win.m_ui.horizontalSlider.value()
    win.m_ui.pushButton.clicked.connect(serial_connect)
    ports = serial.tools.list_ports.comports()
    for port in ports:
        print(port)
        win.m_ui.comboBox.addItem(port.device)
    
    sys.exit(app.exec())

#ports =  list(serial.tools.list_ports.comports())
'''

'''