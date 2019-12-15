from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from datetime import datetime

TEXT = "Жил да был Рикардо Милос. Он любил флексить. Однажды он встретил медведя в лесу и пригласил его на флекс."

RENDER_LEN = 30


class MainApp(QWidget):
    def __init__(self):
        super().__init__()
        self.genWidgets()
        self.text = TEXT
        self.pos = 0
        self.timer=QTimer()
        self.timer.timeout.connect(self.infoTableUpdate)
        self.timer.start(200)

        self.mistake = 0
        self.list_times = []
        self.time_last_key = datetime.now()
        self.all_time = 0

        self.renderText()
        self.infoTableUpdate()
        self.resize(self.widget.size())

    def genWidgets(self):
        self.widget = QWidget(self)
        self.layout = QVBoxLayout(self.widget)
        self.widget.setLayout(self.layout)
        self.rend = QTextEdit(self.widget)
        self.rend.setReadOnly(True)
        self.layout.addWidget(self.rend)
        self.input = QLineEdit(self)
        self.input.textChanged.connect(self.inputKeyPressEvent)
        self.layout.addWidget(self.input)
        self.info = QTextEdit(self.widget)
        self.info.setReadOnly(True)
        self.layout.addWidget(self.info)

        self.show()

    def renderText(self):
        pos1 = max(self.pos - RENDER_LEN // 2, 0)
        pos2 = min(len(self.text) + RENDER_LEN // 2, len(self.text))
        wtext = self.text[pos1:self.pos]
        try:
            cletter = self.text[self.pos]
        except:
            self.celebrate()
            return
        ntext = self.text[min(self.pos + 1, len(self.text)):pos2]

        html = "<i>{}</i><u><b>{}</b></u>{}".format(wtext, cletter, ntext)

        self.rend.setHtml(html)

    def inputKeyPressEvent(self):
        if self.input.text() == "":
            return
        letter = self.input.text()
        self.input.clear()

        if letter == self.text[self.pos]:
            self.pos += 1
            self.renderText()
            now = datetime.now()
            self.list_times.append((now - self.time_last_key).total_seconds())
            self.time_last_key = now
            self.all_time += self.list_times[-1]
            if len(self.list_times) > 10:
                self.list_times.pop(0)
        else:
            self.mistake += 1
        self.infoTableUpdate()

    def infoTableUpdate(self):
        position = self.pos + 1
        all_sym = len(self.text)
        left = all_sym - position
        if len(self.list_times):
            sr = position / self.all_time
            sr10 = 10 / sum(self.list_times)
            sr=round(sr,2)
            sr10 = round(sr10,2)
        else:
            sr = "-"
            sr10 = "-"
        if self.mistake:
            mi=self.mistake*100//(position+self.mistake)
        else:
            mi=0
        text = """Символ <b>{}</b> из <b>{}</b>
Осталось ввести: <b>{}</b>
Средняя скорость (в целом): <b>{}</b>
Средняя скорость (только сейчас): <b>{}</b>
Ошибки: {} ({}%)""".format(position, all_sym, left, sr, sr10,self.mistake,mi)
        self.info.setHtml(text)
    def celebrate(self):
        self.rend.setHtml("Вы закончили!")
        self.input.hide()


if __name__ == '__main__':
    a = QApplication([])
    app = MainApp()
    a.exec()
