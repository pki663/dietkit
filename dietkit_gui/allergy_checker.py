from PyQt5.QtWidgets import QDialog, QGridLayout, QVBoxLayout, QHBoxLayout, QCheckBox, QDialogButtonBox, QScrollArea, QFrame
from PyQt5 import QtCore
from math import sqrt, ceil
import json

class AllergyWindow(QDialog):
    """
    이 파일은 알러지 검사 기능 수행시 어떤 알러지를 검사받을 지를 사용자로부터 입력받음.
    """
    checklist = []
    def __init__(self, header, allow_preset = False):
        super().__init__()
        # 사용자가 사전에 입력한 알러지 프리셋 정보를 불러옴 (setting.py 참조)
        with open('./data/settings.json', 'r') as f:
            self.setting_data = json.load(f)
        self.initUI(header, allow_preset)

    def initUI(self, header, allow_preset):
        self.setWindowTitle('알러지 검사')
        self.setWindowModality(QtCore.Qt.ApplicationModal)

        # 알러지 종류에 따라 알러지 입력창을 보기좋게 조정하는 부분
        col_count = ceil(sqrt(len(header)))
        row_count = ceil(len(header) / col_count)
        
        vbox = QVBoxLayout()
        grid = QGridLayout()
        
        self.cboxs = {}
        temp_idx = 0
        for label in header:
            self.cboxs[label] = QCheckBox(label)
            grid.addWidget(self.cboxs[label], divmod(temp_idx, col_count)[0], temp_idx % col_count)
            temp_idx += 1
        
        # 이전에 선택한 알러지 목록을 불러와서 반영함
        for prev_checked in self.setting_data['prev_allergy']:
            try:
                self.cboxs[prev_checked].toggle()
            except ValueError:
                continue
        
        # 알러지 프리셋들을 반영함
        if allow_preset and self.setting_data["allergy_preset"]:
            preset_grid = QGridLayout()
            self.preset_cboxs = {}
            temp_idx = 0
            for preset in self.setting_data["allergy_preset"].keys():
                self.preset_cboxs[preset] = QCheckBox(preset)
                preset_grid.addWidget(self.preset_cboxs[preset], divmod(temp_idx, col_count)[0], temp_idx % col_count)
                self.preset_cboxs[preset].toggled.connect(lambda: self.preset_checked())
                temp_idx += 1
            vbox.addLayout(preset_grid)
            hline = QFrame()
            hline.setFrameShape(QFrame.HLine)
            hline.setFrameShadow(QFrame.Sunken)
            vbox.addWidget(hline)

        vbox.addLayout(grid)
        self.buttonBox = QDialogButtonBox()
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)
        vbox.addWidget(self.buttonBox, 0, QtCore.Qt.AlignHCenter)
        self.buttonBox.accepted.connect(self.getChecklist)
        self.buttonBox.rejected.connect(self.close)
        self.setLayout(vbox)
        self.show()
        self.exec_()

    def preset_checked(self):
        #프리셋이 선택되면 해당 프리셋에 포함된 알러지들을 잠금
        for preset in self.preset_cboxs.keys():
            if self.preset_cboxs[preset].isChecked():
                for allergen in self.setting_data["allergy_preset"][preset]:
                    self.cboxs[allergen].setCheckState(2)
                    self.cboxs[allergen].setEnabled(False)
            else:
                for allergen in self.setting_data["allergy_preset"][preset]:
                    self.cboxs[allergen].setCheckState(0)
                    self.cboxs[allergen].setEnabled(True)
    
    def getChecklist(self):
        # 확인 버튼 눌렀을 시 최종적으로 선택된 알러지들을 집계
        checked = []
        self.setting_data['prev_allergy'] = []
        for checkbox in self.cboxs.values():
            if checkbox.isChecked():
                checked.append(checkbox.text())
                self.setting_data['prev_allergy'].append(checkbox.text())
        with open('./data/settings.json', 'w') as f:
            json.dump(self.setting_data, f, indent = 2)
        self.checklist = checked
        self.close()