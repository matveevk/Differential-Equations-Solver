import sys
import random
from PySide2.QtWidgets import *
from PySide2.QtCore import Slot, Qt
from diffeq.dif_solver import DifSolver


class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        # Create widgets
        self.enter = QVBoxLayout()
        self.enter.flabel = QLabel("Enter differential equation\n(e. g. y' = x*y, or dy/dt = t^2)")
        self.enter.fedit = QLineEdit().setPlaceholderText("differential equation")
        self.enter.clabel = QLabel("Enter condition\n(e. g. y(0) = 2")
        self.enter.cedit = QLineEdit().setPlaceholderText("condition")

        self.button_solve = QPushButton("Solve")

        # Create layout and add widgets
        layout = QVBoxLayout()
        layout.addWidget(self.enter.flabel)
        layout.addWidget(self.enter.fedit)
        layout.addWidget(self.enter.clabel)
        layout.addWidget(self.enter.cedit)
        #layout.addWidget(self.enter.button_solve)
        self.enter.setLayout(layout)

        layout = QVBoxLayout()
        layout.addWidget(self.enter)
        layout.addWidget(self.button_solve)

        # Set dialog layout
        self.setLayout(layout)

        # Add button signal to greetings slot
        self.button_solve.clicked.connect(self.solver)

    # Activated on click
    def solver(self):
        print(DifSolver(self.enter.fedit.text(), self.enter.cedit.text()).solve())


if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = Form()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec_())
