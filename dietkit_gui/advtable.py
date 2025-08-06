from PyQt5.QtWidgets import QItemDelegate, QComboBox, QCompleter, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDoubleValidator

"""
이 파일은 프로그램에서 사용자가 각 셀을 수정하는 기능을 구현하기 위한 파트임
"""
class ComboDelegate(QItemDelegate):
    #식단표에서 각 셀을 수정하는 파트
    def __init__(self, parent=None):
        super(ComboDelegate, self).__init__(parent)
    def setItems(self, items):
        self.items = items
    def createEditor(self, widget, option, index):
        editor = QComboBox(widget)
        editor.addItems(self.items)
        editor.setEditable(True)
        completer = QCompleter(self.items)
        completer.setCompletionMode(QCompleter.PopupCompletion)
        completer.setFilterMode(Qt.MatchContains)
        editor.setCompleter(completer)
        return editor

class NumericDelegate(QItemDelegate):
    # 영양기준 설정에서 각 상항 하한 입력시 사용되는 파트. 숫자만을 입력받고 하한을 0으로 지정함
    def __init__(self, parent=None):
        super(NumericDelegate, self).__init__(parent)
    def createEditor(self, widget, option, index):
        editor = QLineEdit(widget)
        editor.setValidator(QDoubleValidator(bottom = 0.0))
        return editor