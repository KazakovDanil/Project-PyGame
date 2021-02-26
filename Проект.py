import sys
from PyQt5.QtWidgets import QApplication, QPushButton, \
    QListWidget, QMainWindow, QLabel, QDialog, QTextEdit
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui
from games import Змейка, Крестики_нолики, Арканоид


SPISOC = ['Арканоид', 'Змейка']
SPISOC2 = ['Крестики-нолики']
GAMES = {'Арканоид': Арканоид,
         'Змейка': Змейка,
         'Крестики-нолики': Крестики_нолики}


class Interface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Яндекс.Игры')
        self.setGeometry(500, 200, 800, 680)
        self.setWindowIcon(QtGui.QIcon('mario.png'))

        self.pixmap = QPixmap('phone3.png')
        self.pict = QLabel(self)
        self.pict.resize(800, 680)
        self.pict.setPixmap(self.pixmap)

        self.btn_game = QPushButton('Игры', self)
        self.btn_game.move(20, 230)
        self.btn_game.resize(321, 51)
        self.btn_game.setStyleSheet('background: #FFA500')
        self.btn_game.clicked.connect(self.list_games)

        self.about_program = QPushButton('О программе', self)
        self.about_program.move(20, 290)
        self.about_program.resize(321, 51)
        self.about_program.setStyleSheet('background: #00BFFF')
        self.about_program.clicked.connect(self.description)

        self.exit = QPushButton('Выход', self)
        self.exit.move(20, 350)
        self.exit.resize(321, 51)
        self.exit.setStyleSheet('background: #32CD32')
        self.exit.clicked.connect(self.exit_program)

    def description(self):
        dsc = """Авторы: Учащиеся - Казаков Данил, Кузин Даниил.
        
Описание идеи: Многим пользователям иногда 
хочется отдохнуть от работы и запустить 
простую компьютерную игрушку. При этом 
игра необязательно должна быть сложной и 
требующей больших умственных затрат, 
скорее наоборот. Поэтому мы решили создать 
сборник несложных игр для компьютера."""
        self.upDialog_2 = QDialog(self)
        self.upDialog_2.setFixedSize(300, 300)
        self.upDialog_2.setWindowTitle('Описание')
        self.upDialog_2.setStyleSheet("background: #FFFACD")

        self.text = QTextEdit(self.upDialog_2)
        self.text.resize(250, 250)
        self.text.move(25, 25)
        self.text.setStyleSheet('background: #fffacd')
        self.text.setText(dsc)
        self.upDialog_2.show()

    def list_games(self):
        self.upDialog = QDialog(self)
        self.upDialog.setFixedSize(500, 400)
        self.upDialog.setWindowTitle('Список игр')
        self.upDialog.setStyleSheet("background: #FFFACD")

        self.two = QPushButton('для двоих', self.upDialog)
        self.two.move(250, 50)
        self.two.resize(100, 40)
        self.two.clicked.connect(self.showList2)

        self.alone = QPushButton('для одного', self.upDialog)
        self.alone.move(120, 50)
        self.alone.resize(100, 40)
        self.alone.clicked.connect(self.showList)

        self.gameLabel = QLabel('ИГРЫ', self.upDialog)
        self.gameLabel.setStyleSheet('font-size: 33px; color: #FFA500')
        self.gameLabel.move(200, 10)

        self.upDialog.show()

    def exit_program(self):
        self.close()

    def showList2(self):
        self.two.setStyleSheet('background: #ffffff')
        self.alone.setStyleSheet('background: #fffacd')
        self.listWidget2 = QListWidget(self.upDialog)
        self.listWidget2.move(100, 100)
        self.listWidget2.setFixedSize(300, 250)
        self.listWidget2.setStyleSheet('background: white; color: black')
        for elem in SPISOC2:
            self.listWidget2.addItem(elem)
        self.listWidget2.itemClicked.connect(self.come_in)
        self.listWidget2.show()

    def showList(self):
        self.alone.setStyleSheet('background: #ffffff')
        self.two.setStyleSheet('background: #fffacd')
        self.listWidget = QListWidget(self.upDialog)
        self.listWidget.move(100, 100)
        self.listWidget.setFixedSize(300, 250)
        self.listWidget.setStyleSheet('background: white; color: black')
        for elem in SPISOC:
            self.listWidget.addItem(elem)
        self.listWidget.itemClicked.connect(self.come_in)
        self.listWidget.show()

    def come_in(self, name_game):
        try:
            GAMES[name_game.text()].start()
        except Exception as e:
            print(e)
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Interface()
    ex.show()
    sys.exit(app.exec())
