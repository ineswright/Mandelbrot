import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QHBoxLayout, QVBoxLayout, QPushButton
from PyQt5.QtGui import QPalette, QColor, QPainter, QPen, QPixmap
from PyQt5.QtCore import Qt

#defines the top layer window
#this works fine with class ImageScreen but not ImagePixmap
class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("Mandelbrot Display")
        self.setFixedHeight(500)
        self.setFixedWidth(600)

        #define layouts to be used
        topLayout = QHBoxLayout()
        parameterLayout = QVBoxLayout()
        
        #create widgets for control panel
        controlLabel = QLabel("Controls")
        controlLabel.setAlignment(Qt.AlignCenter)
        controlLabel.setFixedHeight(30) #change later when structuring layout
        zoomInBtn = QPushButton()
        zoomInBtn.setText("Zoom in")
        zoomOutBtn = QPushButton()
        zoomOutBtn.setText("Zoom out")
        leftBtn = QPushButton()
        leftBtn.setText("Move left")
        rightBtn = QPushButton()
        rightBtn.setText("Move right")

        #add widgets to control panel layout
        parameterLayout.addWidget(controlLabel)
        parameterLayout.addWidget(zoomInBtn)
        parameterLayout.addWidget(zoomOutBtn)
        parameterLayout.addWidget(leftBtn)
        parameterLayout.addWidget(rightBtn)

        #add widgets and layout to top tier layout
        topLayout.addLayout(parameterLayout)
        topLayout.addWidget(ImagePixmap())

        #create window widget which goes inside mainWindow and has layout inside
        widget = QWidget()
        widget.setLayout(topLayout)
        ''' the working version has this but doesn't need it
        widget.show()'''
        
        #mainwindow can only have one subwindow- this one
        self.setCentralWidget(widget)

class ImagePixmap(QLabel):

    width = 450
    height = 500
    origin = [225,250]
    
    def __init__(self, *args, **kwargs):
        super(ImagePixmap, self).__init__(*args, **kwargs)
        self.setPixmap(QPixmap())
        self.setFixedWidth(1000)
        #change border to white once drawing works
        #can use "background: white;" to set background
        self.setStyleSheet("border: 2px inset black;")

#use either QPainter(self) or qp.begin(self) but not both
    def paintEvent(self, paintEvent):
        #mandelbrot function must be within paintEvent to be used for drawing
        #determine whether point lies within mandelbrot set
        #doesn't seem to work!
        offsetWidth = 300
        offsetHeight = 250
        size = 200
        def mandelbrot(cx,cy):
            zx = 0
            zy = 0
            for i in range(100):
                #calculates new value of z = z^2 + c
                xtemp = (zx**2) - (zy**2)
                ytemp = 2 * zx * zy
                zx = xtemp + cx
                zy = ytemp + cy

                #determine if its bound
                if ((zx-cx)**2) + ((zy-cy)**2) > 4:
                    return i
            return 150
        
        qp = QPainter(self)
        for i in range(2,998):
            for j in range(2,680):
                x = (i-offsetWidth)/size
                y = (j-offsetHeight)/size
                count = mandelbrot(x,y)
                if count == 150:
                    qp.setPen(QColor(0,0,0))
                else:
                    frac = 255*count/100
                    qp.setPen(QColor(frac,frac,frac))
                qp.drawPoint(i,j)
       

#use QApplication(sys.argv) if you want to use command line arguments for app
app = QApplication([])

#add basic window
#window = QWidget()

#add main window
window = MainWindow()
window.show() #windows are hidden by default


#event loop
app.exec_()

#any code here won't be reached until application loop has ended
