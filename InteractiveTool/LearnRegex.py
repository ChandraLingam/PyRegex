"""
Python Regular Expressions - GUI Interactive Tool
  Chandra Lingam
  Cloud Wave LLC

  Compatible with 3.x version of python
Distributed under GNU Public License - https://www.gnu.org/licenses/gpl-3.0.en.html

Version History
Original Version - Chandra Lingam
PyQt5 migration - Sash Eranki
Changed txtResult to QPlainTextEdit as QTextEdit automatically renders html content.
  it was difficult to work with html input text - Chandra Lingam
"""


import sys
from PyQt5 import QtGui, QtWidgets  # modified from PyQt4 to PyQt5 for anaconda 3.5 distr
import re
import time


class LearnRegex(QtWidgets.QWidget):
    def __init__(self):
        super(LearnRegex, self).__init__()
        self.setFont(QtGui.QFont("Sans Serif", 12))
        self.txtPattern = QtWidgets.QLineEdit()
        self.txtRepPattern = QtWidgets.QLineEdit()
        # Changed to plain text
        self.txtText = QtWidgets.QPlainTextEdit()
        # TODO: changed QTextEdit to QPlainTextEdit
        self.txtResult = QtWidgets.QPlainTextEdit()

        self.regex = None
        self.regex_text = None
        self.regex_group_index = None
        self.match_iter = None

        self.init_ui()

    def init_ui(self):
        lbl_pattern = QtWidgets.QLabel('Pattern')
        lbl_rep_pattern = QtWidgets.QLabel('Replacement Pattern')
        lbl_text = QtWidgets.QLabel('Text')
        lbl_result = QtWidgets.QLabel('Result')
        btn_match = QtWidgets.QPushButton('Match')
        btn_next_match = QtWidgets.QPushButton('Next Match')
        btn_replace = QtWidgets.QPushButton('Replace')
        btn_split = QtWidgets.QPushButton('Split')

        btn_match.clicked.connect(self.match_click)
        btn_next_match.clicked.connect(self.next_match_click)
        btn_replace.clicked.connect(self.replace_click)
        btn_split.clicked.connect(self.split_click)

        grid = QtWidgets.QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(lbl_pattern, 1, 0)
        grid.addWidget(self.txtPattern, 1, 1, 1, 4)
        grid.addWidget(lbl_rep_pattern, 2, 0)
        grid.addWidget(self.txtRepPattern, 2, 1, 1, 4)

        grid.addWidget(lbl_text, 3, 0)
        grid.addWidget(self.txtText, 3, 1, 1, 4)
        grid.addWidget(btn_match, 4, 1)
        grid.addWidget(btn_next_match, 4, 2)
        grid.addWidget(btn_replace, 4, 3)
        grid.addWidget(btn_split, 4, 4)
        grid.addWidget(lbl_result, 5, 0)
        grid.addWidget(self.txtResult, 5, 1, 5, 4)

        self.setLayout(grid)

        self.setGeometry(300, 300, 860, 620)
        self.setWindowTitle('Learning Regex with Python')
        self.show()

    def match_click(self):
        # TODO Plain Text
        self.txtResult.setPlainText('Value,Index,Length,ElapsedTime(s)')
        try:
            self.regex = re.compile(self.txtPattern.text())
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, 'Error', 'Pattern error: {0}'.format(str(e)))
            return

        self.regex_text = self.txtText.toPlainText()
        self.regex_group_index = dict((v, k) for k, v in self.regex.groupindex.items())
        self.match_iter = self.regex.finditer(self.regex_text)
        self.highlight_match()

    def next_match_click(self):
        self.highlight_match()

    def replace_click(self):
        self.txtResult.setPlainText(
            re.sub(self.txtPattern.text(), self.txtRepPattern.text(), self.txtText.toPlainText())
        )

    def split_click(self):
        self.txtResult.setPlainText("")
        for s in re.split(self.txtPattern.text(), self.txtText.toPlainText()):
            self.txtResult.appendPlainText(s)

    def highlight_match(self):
        start_time = None
        try:
            self.txtText.setPlainText(self.regex_text)

            start_time = time.time()
            match = self.match_iter.__next__()
            end_time = time.time()

            self.txtResult.appendPlainText(
                '{0},{1},{2},{3:.2f}'.format(
                    match.group(0), match.start(), match.end() - match.start(), end_time - start_time
                )
            )

            for i in range(0, len(match.groups())):
                gn = i + 1
                group_name = None
                if gn in self.regex_group_index:
                    group_name = self.regex_group_index[gn]

                self.txtResult.appendPlainText(
                    '  Group:{0}, Name:{1}, Value: {2}'.format(gn, group_name, match.group(gn))
                )

            self.highlighter(match.start(), match.end())

        except StopIteration:
            end_time = time.time()
            self.txtResult.appendPlainText('End, Elapsed Time (s): {0:0.2f}'.format(end_time - start_time))

    def highlighter(self, start, end):
        format_ = QtGui.QTextCharFormat()
        format_.setBackground(QtGui.QBrush(QtGui.QColor("yellow")))
        cursor = self.txtText.textCursor()
        cursor.setPosition(start)
        cursor.movePosition(QtGui.QTextCursor.Right, QtGui.QTextCursor.KeepAnchor, end - start)
        cursor.mergeCharFormat(format_)


def main():
    app = QtWidgets.QApplication(sys.argv)
    ex = LearnRegex()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
