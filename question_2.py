import numpy as np

from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QFileDialog,
                               QVBoxLayout, QHBoxLayout)
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure

from About import AboutWindow


class IceCreamWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.temperatures = []
        self.revenues = []
        self.selected_file = ''

        self.about_window = AboutWindow()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Ice Cream Revenue')
        self.setGeometry(100, 100, 800, 650)

        self.title_label = QLabel('Ice Cream Revenue vs. Temperature')
        self.title_label.setObjectName('title')

        self.file_load_button = QPushButton('Load Data File')
        self.file_load_button.clicked.connect(self.file_load_method)

        self.about_button = QPushButton('About')
        self.about_button.setObjectName('about_button')
        self.about_button.clicked.connect(self.show_about_window)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.file_load_button)
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.about_button)

        self.figure = Figure()
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.canvas.setMinimumSize(600, 450)
        self.ax = self.figure.add_subplot()

        self.toolbar = NavigationToolbar2QT(self.canvas, self)

        self.message_label = QLabel('Load a file to see the graph')
        self.message_label.setObjectName('message')

        layout = QVBoxLayout()
        layout.addWidget(self.title_label)
        layout.addLayout(buttons_layout)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.message_label)
        self.setLayout(layout)

    def file_load_method(self):
        self.selected_file, _ = QFileDialog.getOpenFileName(self, 'Choose a data file', '', 'CSV files (*.csv)')
        if self.selected_file == '':
            return

        self.temperatures = []
        self.revenues = []

        with open(self.selected_file, 'r') as f:
            next(f)
            for line in f:
                if line.strip() == '':
                    continue
                temperature, revenue = line.strip().split(',')
                self.temperatures.append(float(temperature))
                self.revenues.append(float(revenue))

        self.message_label.setText(f'{len(self.temperatures)} days loaded')
        self.draw_graph()

    def draw_graph(self):
        self.ax.clear()

        self.ax.scatter(self.temperatures, self.revenues, s=1, color='blue', label='Data')

        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)

        self.ax.set_title('Ice Cream Revenue by Outside Temperature')
        self.ax.set_xlabel('Temperature (°C)')
        self.ax.set_ylabel('Revenue ($)')

        coefficients = np.polyfit(self.temperatures, self.revenues, 1)
        line_function = np.poly1d(coefficients)

        line_x = np.linspace(min(self.temperatures), max(self.temperatures), 100)
        line_y = line_function(line_x)

        self.ax.plot(line_x, line_y, color='red', label='Trend Line')
        self.ax.text(0.05, 0.9, f'y = {coefficients[0]:.2f}x + {coefficients[1]:.2f}',
                     transform=self.ax.transAxes, color='red', fontsize=12)
        self.ax.legend(loc='lower right')

        self.canvas.draw()

    def show_about_window(self):
        self.about_window.show()

    def closeEvent(self, event):
        self.about_window.close()


if __name__ == '__main__':
    app = QApplication()

    with open('style.qss') as f:
        app.setStyleSheet(f.read())

    window = IceCreamWindow()
    window.show()
    app.exec()
