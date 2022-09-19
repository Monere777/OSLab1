import ipaddress
import platform
import sys
from threading import Thread

from PyQt6.QtWidgets import *


class IpInfoWindow(QMainWindow):
    def __init__(self, number, address, mask):
        super().__init__()
        self.setFixedSize(200, 250)
        self.setWindowTitle("Info №" + number)

        self.layout = QGridLayout()
        self.layout.addWidget(QLabel("Address:"), 0, 1)
        self.layout.addWidget(QLabel("Mask:"), 1, 1)
        self.layout.addWidget(QLabel("Cidr:"), 2, 1)
        self.layout.addWidget(QLabel("Network:"), 3, 1)
        self.layout.addWidget(QLabel("Broadcast:"), 4, 1)
        self.layout.addWidget(QLabel("Full hosts:"), 5, 1)
        self.layout.addWidget(QLabel("Available hosts:"), 6, 1)

        # custom
        # ip_list = list(map(int, address.split(".")))
        # mask_list = list(map(int, mask.split(".")))
        #
        # close_bit = 0
        # open_octant = 4
        #
        # for o in mask_list:
        #     if o == 255:
        #         close_bit += 8
        #     else:
        #         close_bit += bin(o).count('1')
        #         break
        #     open_octant -= 1
        #
        # open_bit = 32 - close_bit
        # full_hosts = 2 ** open_bit
        #
        # if open_octant != 0:
        #
        #     tmp = int(full_hosts / (256 ** (open_octant - 1)))
        #     tmp_count = int(ip_list[4 - open_octant] / tmp)
        #
        #     host = ""
        #     broadcast = ""
        #     for o in range(4 - open_octant):
        #         host += str(ip_list[o]) + "."
        #         broadcast += str(ip_list[o]) + "."
        #
        #     host += str(tmp * tmp_count)
        #     broadcast += str(tmp * (tmp_count + 1) - 1)
        #
        #     for o in range(3 - host.count('.')):
        #         host += ".0"
        #         broadcast += ".255"
        #
        # else:
        #     host = address
        #     broadcast = address
        #
        # self.layout.addWidget(QLabel(str(address)), 0, 2)
        # self.layout.addWidget(QLabel(str(mask)), 1, 2)
        # self.layout.addWidget(QLabel(str(close_bit)), 2, 2)
        # self.layout.addWidget(QLabel(str(host)), 3, 2)
        # self.layout.addWidget(QLabel(str(broadcast)), 4, 2)
        # self.layout.addWidget(QLabel(str(full_hosts)), 5, 2)
        # self.layout.addWidget(QLabel(str(full_hosts - 2 if full_hosts - 2 > 0 else 0)), 6,
        #                      2)

        # lib
        ipi = ipaddress.ip_interface(address + "/" + mask)
        self.layout.addWidget(QLabel(str(ipi.ip)), 0, 2)
        self.layout.addWidget(QLabel(str(ipi.netmask)), 1, 2)
        self.layout.addWidget(QLabel(str(ipi.network).split('/')[1]), 2, 2)
        self.layout.addWidget(QLabel(str(ipi.network).split('/')[0]), 3, 2)
        self.layout.addWidget(QLabel(str(ipi.network.broadcast_address)), 4, 2)
        self.layout.addWidget(QLabel(str(ipi.network.num_addresses)), 5, 2)
        self.layout.addWidget(QLabel(str(ipi.network.num_addresses - 2 if ipi.network.num_addresses - 2 > 0 else 0)), 6,
                              2)
        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)
        container.setFocus()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lab 1")
        self.setFixedSize(550, 320)
        layout = QGridLayout()

        self.ipDefault = ["192.168.2.4", "164.240.89.149", "36.116.125.42", "97.137.177.194", "30.126.146.183"]
        self.ipSubnetDefault = [3, 8, 5, 1, 12]
        self.windows = []
        self.treads = []
        self.ipRecords = []
        self.priority = []
        self.ipSubnetMask = []
        for i in range(len(self.ipDefault)):
            self.ipRecords.append(QLineEdit(self.ipDefault[i]))
            tmp = QComboBox()
            tmp.addItems(["255.255.255.255", "255.255.255.254", "255.255.255.252", "255.255.255.248",
                          "255.255.255.240", "255.255.255.224", "255.255.255.192", "255.255.255.128",
                          "255.255.255.0", "255.255.254.0", "255.255.252.0", "255.255.248.0",
                          "255.255.240.0", "255.255.224.0", "255.255.192.0", "255.255.128.0",
                          "255.255.0.0", "255.254.0.0", "255.252.0.0", "255.248.0.0",
                          "255.240.0.0", "255.224.0.0", "255.192.0.0", "255.128.0.0",
                          "255.0.0.0", "254.0.0.0", "252.0.0.0", "248.0.0.0",
                          "240.0.0.0", "192.0.0.0", "128.0.0.0", "0.0.0.0",
                          ])
            tmp.setCurrentIndex(self.ipSubnetDefault[i])
            self.ipSubnetMask.append(tmp)
            tmp = QComboBox()
            tmp.addItems(["high", "normal", "low"])
            tmp.setCurrentIndex(1)
            self.priority.append(tmp)

        layout.addWidget(QLabel("Host IP address"), 0, 1)
        layout.addWidget(QLabel("Subnet mask"), 0, 2)
        for i in range(0, len(self.ipRecords)):
            self.ipRecords[i].setMaximumWidth(120)
            self.ipSubnetMask[i].setMaximumWidth(120)
            self.priority[i].setMaximumWidth(100)
            layout.addWidget(QLabel("IP №" + str(i + 1)), i * 2 + 1, 1)
            layout.addWidget(self.ipRecords[i], i * 2 + 2, 1)
            layout.addWidget(self.ipSubnetMask[i], i * 2 + 2, 2)
            layout.addWidget(self.priority[i], i * 2 + 2, 3)

        button = QPushButton("Calculate")
        button2 = QPushButton("Close All")
        button.setFixedWidth(100)
        button2.setFixedWidth(100)
        button.clicked.connect(self.clic_act)
        button2.clicked.connect(self.closeEvent)

        layout.addWidget(QWidget(), len(self.ipDefault) * 2 + 2, 3)
        layout.addWidget(button, 2, 4)
        layout.addWidget(button2, 3, 4)
        # layout.addWidget(QWidget(), len(self.ipDefault) * 2 + 3, 5)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        container.setFocus()

    def clic_act(self):
        for i in range(len(self.ipRecords)):
            pr = 0
            if self.priority[i].currentText() == "normal":
                pr = 0
            elif self.priority[i].currentText() == "high":
                pr = 2
            elif self.priority[i].currentText() == "low":
                pr = -2

            x1 = Thread(target=self.show_info(i, pr))
            x1.start()

    def show_info(self, num, pr):
        if platform.system() == 'Windows':
            win32process.SetThreadPriority(win32api.GetCurrentThread(), pr)
        tmp_window = IpInfoWindow(str(num + 1), self.ipRecords[num].text(), self.ipSubnetMask[num].currentText())
        tmp_window.move(250 * num, 0)
        self.windows.append(tmp_window)
        tmp_window.show()

    def closeEvent(self, event):
        for w in self.windows:
            w.close()


if __name__ == '__main__':

    if platform.system() == 'Windows':
        import win32api
        import win32process

    app = QApplication(sys.argv)

    window = MainWindow()

    window.show()

    app.exec()
