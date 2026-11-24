from PySide6.QtWidgets import QApplication, QWidget, QLabel


class AboutWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('About')
        self.setGeometry(200, 200, 420, 200)

        self.title_label = QLabel('About me', self)
        self.title_label.setObjectName('title')
        self.title_label.setGeometry(20, 20, 380, 40)

        self.name_label = QLabel('Name: Ofek Akri', self)
        self.name_label.setGeometry(20, 70, 380, 30)

        self.email_label = QLabel('Email: ofekakri29@gmail.com', self)
        self.email_label.setGeometry(20, 105, 380, 30)

        self.github_label = QLabel('GitHub: <a href="https://github.com/ofekakri29-dot/exe4">github.com/ofekakri29-dot/exe4</a>', self)
        self.github_label.setGeometry(20, 140, 380, 30)
        self.github_label.setOpenExternalLinks(True)


if __name__ == '__main__':
    app = QApplication()
    window = AboutWindow()
    window.show()
    app.exec()
