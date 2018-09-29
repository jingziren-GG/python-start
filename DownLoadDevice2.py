# -*- coding:utf-8 -*-
import requests
import sys
from PyQt5.QtWidgets import (QWidget, QLabel,QInputDialog,QMessageBox,
    QLineEdit, QApplication)
from PyQt5.QtWidgets import (QMainWindow, QFileDialog, QApplication,QPushButton)
import os

class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        lbl1 = QLabel('Url:', self)
        lbl1.move(10, 10)

        self.lbl = QLabel(self)
        self.qle = QLineEdit(self)
        self.qle.move(40, 5)
        self.qle.resize(450,25)
        self.lbl.move(120, 80)

        lbl2 = QLabel('DataName:', self)
        lbl2.move(10, 45)

        self.lb2 = QLabel(self)
        self.qle2 = QLineEdit(self)
        self.qle2.move(70, 40)
        self.qle2.resize(420, 25)
        self.lb2.move(120, 80)

        lbl3 = QLabel('SaveUrl:', self)
        lbl3.move(10, 80)

        self.lb3 = QLabel(self)
        self.lb3.move(120, 80)
        self.qle3 = QLineEdit(self)
        self.qle3.move(70, 75)
        self.qle3.resize(420, 25)
        self.button = QPushButton('选取储存文件夹', self)
        self.button.move(5, 110)
        # self.button.resize(95, 25)
        self.button.clicked.connect(self.on_click)

        self.button2 = QPushButton('开始下载', self)
        self.button2.move(105, 110)
        self.button2.clicked.connect(self.DownData)

        self.button3 = QPushButton('文件重命名', self)
        self.button3.move(190, 110)
        self.button3.clicked.connect(self.ReName)

        self.button4 = QPushButton('打开文件夹', self)
        self.button4.move(275, 110)
        self.button4.clicked.connect(self.PaperFile)

        self.setGeometry(300, 300, 500, 300)
        self.setWindowTitle('下载器')
        self.show()


    # 选择文件夹
    def on_click(self):
        fname = QFileDialog.getExistingDirectory(self, '选取文件夹', './')
        self.qle3.setText(fname)

        # 选择文件
        # fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')
    def DownData(self):
        self.url = self.qle.text()
        if self.qle2.text():
            dataname = self.qle2.text()
            if '.' in dataname:
                self.qle2.setText(dataname)
                self.GetUrl(dataname)
                reply = QMessageBox.information(self, ">_<", "下载完成")
            else:
                # http://p0.so.qhimgs1.com/t013dee8baa471a5dc0.jpg
                dataname = dataname + '.' + self.url.split('/')[-1].split('.')[-1]
                self.qle2.setText(dataname)
                self.GetUrl(dataname)
                reply = QMessageBox.information(self, ">_<", "下载完成")
        else:
            # 通过地址检测下载的是什么
            self.dataname = self.url.split('/')[-1]
            self.qle2.setText(self.dataname)
            self.GetUrl(self.dataname)
            reply = QMessageBox.information(self, ">_<", "下载完成")



    # 下载
    def GetUrl(self,dataname):
        saveUrl = self.qle3.text()
        if not saveUrl:
            respon = requests.get(self.url)
            f = open(dataname,'wb')
            f.write(respon.content)
            f.close()
        else:
            DataN = str(saveUrl) + '/' + str(dataname)
            respon = requests.get(self.url)
            f = open(DataN, 'wb')
            f.write(respon.content)
            f.close()

    # 重命名
    def ReName(self,event):
        if self.qle2.text():
            # 判断文件是否存在
            if str(self.qle3.text()):
                DataPath = str(self.qle3.text()) + '/' + str(self.qle2.text())
                if os.path.exists(DataPath):
                    value, ok = QInputDialog.getText(self, "修改文件名", "请输入新的文件名:", QLineEdit.Normal,
                                                     "N%s" % self.qle2.text())
                    if ok:
                        name = self.qle2.text()
                        HZ = name.split('.')[-1]
                        VA = value.split('.')[0]
                        os.rename(DataPath, str(self.qle3.text()) + '/' + '%s.%s' % (VA, HZ))
                        reply = QMessageBox.information(self, "O_O", "修改成功")
                        self.qle2.setText('%s.%s' % (VA, HZ))
                    else:
                        pass
                else:
                    reply = QMessageBox.information(self, "O_O", "文件不存在请输入正确的文件名")
            else:
                if os.path.exists(self.qle2.text()):
                    value, ok = QInputDialog.getText(self, "修改文件名", "请输入新的文件名:", QLineEdit.Normal,
                                                     "N%s" % self.qle2.text())
                    if ok:
                        name = self.qle2.text()
                        HZ = name.split('.')[-1]
                        VA = value.split('.')[0]
                        os.rename(name, '%s.%s' % (VA, HZ))
                        reply = QMessageBox.information(self, "O_O", "修改成功")
                        self.qle2.setText('%s.%s' % (VA, HZ))
                    else:
                        pass

                else:
                    reply = QMessageBox.information(self, "O_O", "文件不存在请输入正确的文件名")
        else:
            reply = QMessageBox.information(self, "O_O", "请在文件名栏处输入文件名")


    # 打开文件夹
    def PaperFile(self):
        saveUrl = self.qle3.text()
        if saveUrl:
            os.system('explorer %s' % saveUrl)
        else:
            GG = os.getcwd()
            # 括号里是cmd命令
            os.system('explorer %s'%GG)



# https://www.66s.cc/e/DownSys/play/ckplayer/ckplayer.swf


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())