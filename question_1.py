import os
import sys
import subprocess

from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QSpinBox,
                               QTableWidget, QTableWidgetItem, QFileDialog,
                               QVBoxLayout, QHBoxLayout)

from About import AboutWindow


class GradesWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.student_ids = []
        self.original_grades = []
        self.corrected_grades = []
        self.selected_file = ''
        self.header = ''

        self.about_window = AboutWindow()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Grades Correction')
        self.setGeometry(100, 100, 520, 700)

        self.title_label = QLabel('Grades Correction')
        self.title_label.setObjectName('title')

        self.file_load_button = QPushButton('Load Grades File')
        self.file_load_button.clicked.connect(self.file_load_method)

        self.file_label = QLabel('No file selected')

        self.grades_table = QTableWidget(50, 3)
        self.grades_table.setHorizontalHeaderLabels(['ID', 'Original Grades', 'Corrected Grades'])
        self.grades_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.grades_table.horizontalHeader().setStretchLastSection(True)
        self.grades_table.setColumnWidth(0, 140)
        self.grades_table.setColumnWidth(1, 140)

        self.points_label = QLabel('Correction points (press Enter):')
        self.points_input = QSpinBox()
        self.points_input.setRange(0, 100)
        self.points_input.editingFinished.connect(self.correct_grades)

        points_layout = QHBoxLayout()
        points_layout.addWidget(self.points_label)
        points_layout.addWidget(self.points_input)
        points_layout.addStretch()

        self.update_file_button = QPushButton('Update File')
        self.update_file_button.clicked.connect(self.update_file)

        self.about_button = QPushButton('About')
        self.about_button.setObjectName('about_button')
        self.about_button.clicked.connect(self.show_about_window)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.update_file_button)
        buttons_layout.addWidget(self.about_button)

        self.message_label = QLabel('')
        self.message_label.setObjectName('message')

        layout = QVBoxLayout()
        layout.addWidget(self.title_label)
        layout.addWidget(self.file_load_button)
        layout.addWidget(self.file_label)
        layout.addWidget(self.grades_table)
        layout.addLayout(points_layout)
        layout.addLayout(buttons_layout)
        layout.addWidget(self.message_label)
        self.setLayout(layout)

    def file_load_method(self):
        self.selected_file, _ = QFileDialog.getOpenFileName(self, 'Choose a grades file', '', 'CSV files (*.csv)')
        if self.selected_file == '':
            return

        self.student_ids = []
        self.original_grades = []
        self.corrected_grades = []

        with open(self.selected_file, 'r') as f:
            self.header = next(f).strip()
            for line in f:
                student_id, grade = line.strip().split(',')
                self.student_ids.append(student_id)
                self.original_grades.append(int(grade))
                self.corrected_grades.append(int(grade))

        self.file_label.setText(f'File: {self.selected_file}')
        self.message_label.setText(f'{len(self.student_ids)} students loaded')
        self.update_table()

    def update_table(self):
        self.grades_table.clearContents()
        for i in range(len(self.student_ids)):
            self.grades_table.setItem(i, 0, QTableWidgetItem(self.student_ids[i]))
            self.grades_table.setItem(i, 1, QTableWidgetItem(str(self.original_grades[i])))
            self.grades_table.setItem(i, 2, QTableWidgetItem(str(self.corrected_grades[i])))

    def correct_grades(self):
        points = self.points_input.value()

        for i in range(len(self.original_grades)):
            new_grade = self.original_grades[i] + points
            if new_grade > 100:
                new_grade = 100
            self.corrected_grades[i] = new_grade

        self.update_table()

    def update_file(self):
        if self.selected_file == '':
            self.message_label.setText('Load a file first')
            return

        with open(self.selected_file, 'w') as f:
            f.write(f'{self.header}\n')
            for i in range(len(self.student_ids)):
                f.write(f'{self.student_ids[i]},{self.corrected_grades[i]}\n')

        self.message_label.setText('File updated')
        self.open_file(self.selected_file)

    def open_file(self, file_name):
        if sys.platform == 'win32':
            os.startfile(file_name)
        elif sys.platform == 'darwin':
            subprocess.run(['open', file_name])
        else:
            subprocess.run(['xdg-open', file_name])

    def show_about_window(self):
        self.about_window.show()

    def closeEvent(self, event):
        self.about_window.close()


if __name__ == '__main__':
    app = QApplication()

    with open('style.qss') as f:
        app.setStyleSheet(f.read())

    window = GradesWindow()
    window.show()
    app.exec()
