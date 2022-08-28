# импотируем библиотеки
from PyQt5 import QtWidgets, uic
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QIODevice
from PyQt5.QtGui import QTextCursor
import os

# иницилизируем qt и запускаем приложение
# Define function to import external files when using PyInstaller.


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


app = QtWidgets.QApplication([])
ui = uic.loadUi(resource_path("designer.ui"))
ui.setWindowTitle("PortListener")

serial = QSerialPort()
ports = QSerialPortInfo().availablePorts()

ui.portLabel.setStyleSheet("QLabel {background:rgba(191, 64, 64, 203) \
                                    rgba(255, 0, 0, 140); color:black}")

with open("res.txt", "r") as file:
    speed = int(file.readline())
    ui.speedPort.setText(str(speed))


for port in ports:
    ui.comList.addItem((port.portName()))


def printLogs(data):
    ui.logs.moveCursor(QTextCursor.End)
    ui.logs.insertPlainText(data + "\n")
    ui.logs.moveCursor(QTextCursor.End)


def onPortRead():
    lisenPort = ui.portLisen.checkState()
    logsSave = ui.logsSave.checkState()
    rx = serial.readLine()
    rxs = str(rx, "ISO-8859-1").strip()
    if lisenPort:
        printLogs(rxs)
        if logsSave:
            with open(r"log.txt", "a") as file:
                file.write(rxs + "\n")
    else:
        ui.logs.clear()


def onOpenPort():
    serial.setPortName(ui.comList.currentText())
    greenPortLabel = "QLabel {background:rgb(143, 240, 164); color:black;}"
    ui.portLabel.setStyleSheet(greenPortLabel)
    speed = int((ui.speedPort.text()).strip())
    with open(r"res.txt", "w") as file:
        file.write(str(speed))
    serial.setBaudRate(speed)
    ui.logs.setPlainText("Скорость = " + str(speed) + "\n")
    serial.open(QIODevice.ReadWrite)


def onClosePort():
    serial.close()
    ui.portLabel.setStyleSheet("QLabel {background:rgba(191, 64, 64, 203) \
                                        rgba(255, 0, 0, 140); color:black}")


def cleaToLogs():
    ui.logs.clear()


def cleaToLogsTx():
    with open(r"log.txt", "w") as file:
        file.write('')


def toPortSendData():
    serial.write((ui.portSend.text()).encode())
    ui.logs.setPlainText(str(ui.portSend.text()))


serial.readyRead.connect(onPortRead)
ui.openPort.clicked.connect(onOpenPort)
ui.closePort.clicked.connect(onClosePort)
ui.cleaLogs.clicked.connect(cleaToLogs)
ui.cleaLogsTx.clicked.connect(cleaToLogsTx)
ui.sendPortBtn.clicked.connect(toPortSendData)

if __name__ == '__main__':
    # Показываем
    ui.show()
    app.exec()
