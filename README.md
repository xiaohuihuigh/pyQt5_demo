# pyQt5_demo
pyQt5 关于QThread的应用与线程控制

通过对线程的了解，我发现在次线程一个不断循环的事件并对该事件进行一定程度的控制是一件相对复杂的事。
这里通过两个线程，一个线程为控制线程，一个线程为事件线程，将以循环为元操作的的事件，变为以循环内的程序为元操作的
事件，和控制循环的监听线程，提高程序的颗粒程度。

如果对于每次执行循环内操作没有明确的时间间隔要求，也可以在事件线程内部进行线程控制。
