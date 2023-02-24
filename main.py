import time

from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.Qt import pyqtSignal, pyqtSlot
from PyQt5.QtCore import QThread, QObject
import demo
import sys
import threading


# 可以将监听的事件与每一次监听发出的信号进行连接，但是由于不知道被监听事件需要多长的时间运行，所以无法准确标记每次监听的间隔
# 监听线程可以用与监听多个线程，主要用于管理线程的运行和停止
# 如果监听间隔较短，会导致事件线程阻塞

# 将槽函数搞到一个线程
class Monitor(QObject):
    signal = pyqtSignal()  # 开启监听线程的信号
    monitor_signal = pyqtSignal()  # 在监听的线程的信号信息，需要监听就一直发信号

    def __init__(self):
        super(Monitor, self).__init__()
        self.start = False
        self.pause = False
        self.stop = True
        self.signal.connect(self.run)

    @pyqtSlot()
    def run(self):
        while not self.stop:
            if self.pause:
                print(self.pause)
            elif self.start:
                self.monitor_signal.emit()
            print(time.time())
            time.sleep(1)


class EventObj(QObject):
    signal = pyqtSignal()

    def __init__(self, function, *args, **kwargs):
        super(EventObj, self).__init__()
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.signal.connect(self.run)

    @pyqtSlot()
    def run(self):
        print("in event run")
        self.function(*self.args, **self.kwargs)


class Add():
    def __init__(self):
        self.n = 1

    def add(self):
        time.sleep(3)
        self.n += 1
        print(self.n)


class DemoWidget(QWidget):

    def __init__(self, parent=None):
        super(DemoWidget, self).__init__(parent)
        self.ui = demo.Ui_Form()
        self.ui.setupUi(self)
        self.monitorObj = Monitor()
        self.monitorThread = QThread()
        self.monitorThread.start()
        self.monitorObj.moveToThread(self.monitorThread)
        self.monitorObj.monitor_signal.connect(self.monitored)
        # self.monitorObj = self.eventObj.parent()

    def creat_event(self):
        self.addnum = Add()  # 要监听的事件，实现在一个对象中的累加，通常情况下有一个初始值，后续对初始值进行修改
        self.eventObj = EventObj(self.addnum.add)
        self.eventThread = QThread()
        self.eventThread.start()
        self.eventObj.moveToThread(self.eventThread)
        # self.eventObj.setParent(self.monitorObj)    #监听线程结束时，被监听的线程同样要停止，设置eventObj的parent为MonitorObj

    @pyqtSlot()
    def monitored(self):
        self.eventObj.signal.emit()

    @pyqtSlot()
    def monitor_start(self):
        self.monitorObj.start = True
        self.monitorObj.pause = False
        if self.monitorObj.stop:
            self.creat_event()
            self.monitorObj.stop = False
            self.monitorObj.signal.emit()
        print(self.monitorObj.start)

    @pyqtSlot()
    def monitor_pause(self):
        self.monitorObj.pause = True
        self.monitorObj.start = False

    @pyqtSlot()
    def monitor_stop(self):
        self.monitorObj.stop = True
        # 重新初始化要操作的对象
        self.eventThread.exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    print(threading.get_ident())

    demo = DemoWidget()
    demo.show()
    sys.exit(app.exec_())
