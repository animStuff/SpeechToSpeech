from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QLabel
from PyQt5.QtCore import QSize, QPoint,  QPropertyAnimation, QProcess, QCoreApplication
from PyQt5.QtGui import QIcon, QMovie, QFontDatabase
from speech import audioManager
import sys, playsound, os

text, error = None, None
class app(QWidget):
    global text, error

    def __init__(self):
        self.squareSize = 750
        self.press = True

        app = QApplication([])
        main_ui = self.gui()
        sys.exit(app.exec_())

    def gui(self, parent=None):
        super(app, self).__init__(parent)
        QFontDatabase.addApplicationFont('assets/Poppins-Bold.ttf')
        self.setWindowTitle('Speech To Speech!')
        self.setFixedSize(self.squareSize, self.squareSize)
        self.setStyleSheet(
           """background-color: #50577A"""
        )

        size1, C1 = 350, 700
        self.label = QLabel(self)
        self.label.move(int((self.squareSize - size1)/2), self.squareSize - C1)
        self.label.resize(size1, size1)
        self.label.setStyleSheet(f"border: 8px solid white;border-radius: {size1/2}px;")

        movieSize, C2 = 220, -415
        self.movie = QMovie('assets/animation.gif')
        self.movie.setScaledSize(QSize(movieSize, movieSize))
        self.label1 = QLabel(self)
        self.label1.setMovie(self.movie)
        self.label1.move(int((self.squareSize - movieSize)/2), (self.squareSize - movieSize) + C2)
        self.movie.start()

        buttonSize, C3 = 200, 100
        self.button = QPushButton(self)
        self.button.move(int((self.squareSize - buttonSize)/2), 500)
        self.button.setIcon(QIcon('assets/button.png'))
        self.button.setIconSize(QSize(buttonSize, buttonSize))
        self.button.setStyleSheet("""
            QPushButton{
                border-radius: 100px;
            }
           
            QPushButton:hover{
                background-color: #6B728E;
               
            }
           
        """)
        self.button.clicked.connect(self.onClick)

        self.hideAnimation = QPropertyAnimation(self.button, b"pos")
        self.hideAnimation.setDuration(1500)
        self.hideAnimation.setStartValue(self.button.pos())
        self.hideAnimation.setEndValue(QPoint(275, 750))

        self.label1 = QLabel('', self)
        self.label1.setStyleSheet("""
            font-family: Poppins;
            font-size: 30px;
        """)

        # container for other lang
        self.dummY = QPushButton(self)
        self.dummY.hide()

        self.show()


    def onClick(self):
        try:
            text, error = audioManager().all_in_one()
            self.onExecution(text, error)
            self.dummY.clicked.connect(self.reboot)


        except Exception as e:
            pass

    def reboot(self):
        os.remove('translated.mp3')
        QCoreApplication.quit()
        status = QProcess.startDetached(sys.executable, sys.argv)

    def onExecution(self, text, error):
        self.button.setIcon(QIcon('assets/buttonOnClick.png'))
        self.hideAnimation.start()
        self.updateText(text, error)
        self.hideAnimation.finished.connect(self.speakText)


    def updateText(self, text, error):
        if error:
            self.label1.setStyleSheet("""
                color: #850000;
                font-family: Poppins;
                font-size: 30px;
            
            """)

        # updating the text
        self.label1.setText(text)
        self.label1.adjustSize()
        self.label1.move(int((self.squareSize - self.label1.width())/2), 500)
        self.label1.update()

    def speakText(self):
        filename = os.path.join(os.getcwd(), 'translated.mp3')
        playsound.playsound(filename)
        self.dummY.click()



if __name__ == '__main__':
    app()


#%%
