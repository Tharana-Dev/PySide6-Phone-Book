from PySide6.QtWidgets import QWidget, QMessageBox, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QLineEdit
from PySide6.QtCore import Signal, Qt

import sys
from PySide6.QtWidgets import QApplication

class InputPanel(QWidget):
    contact_added = Signal(str, str, str, str) # (first_name, last_name, phone, email)

    def __init__(self, parent=None):
        super().__init__(parent)

# -----Main Layout - vertical box(for inputs and buttons) -----------
        outer_layout = QVBoxLayout()
        self.setLayout(outer_layout)

        topic = QLabel("Data Handling center")
        topic.setObjectName("topic")
        topic.setAlignment(Qt.AlignmentFlag.AlignCenter)
        outer_layout.addWidget(topic)

# ------Input field Layout: horizontal [fiel name]: [input field] layout stacked vertically
        input_layout = QVBoxLayout()
        outer_layout.addLayout(input_layout)

# ------Row1: Fisrt name-----------
        row1 = QHBoxLayout()
        row1.setSpacing(12)
        input_layout.addLayout(row1)

        row1_name = QLabel("First Name: ")
        row1_name.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        row1_name.setObjectName("fieldLabel")

        self.first_name = QLineEdit()
        self.first_name.setObjectName("input")
        self.first_name.setPlaceholderText("Enter Your First Name Here")

        row1.addWidget(row1_name,4)
        row1.addWidget(self.first_name,6)

# ------Row2: Last name-----------
        row2 = QHBoxLayout()
        row2.setSpacing(12)
        input_layout.addLayout(row2)

        row2_name = QLabel("Last Name: ")
        row2_name.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        row2_name.setObjectName("fieldLabel")

        self.last_name = QLineEdit()
        self.last_name.setObjectName("input")
        self.last_name.setPlaceholderText("Enter Your Last Name Here")

        row2.addWidget(row2_name, 4)
        row2.addWidget(self.last_name, 6)

# ------Row3: Email-----------
        row3 = QHBoxLayout()
        row3.setSpacing(12)
        input_layout.addLayout(row3)

        row3_name = QLabel("Email: ")
        row3_name.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        row3_name.setObjectName("fieldLabel")

        self.email = QLineEdit()
        self.email.setObjectName("input")
        self.email.setPlaceholderText("Enter Your Email Here")

        row3.addWidget(row3_name, 4)
        row3.addWidget(self.email,6)

# ------Row4: Contact Number-----------
        row4 = QHBoxLayout()
        input_layout.addLayout(row4)

        row4_name = QLabel("Phone: ")
        row4_name.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        row4_name.setObjectName("fieldLabel")

        self.phone = QLineEdit()
        self.phone.setObjectName("input")
        self.phone.setPlaceholderText("Enter Your Contact Number Here")

        row4.addWidget(row4_name, 4)
        row4.addWidget(self.phone, 6)

# ----- Buttons: Add / Reset ---------
        button_layout = QHBoxLayout()
        outer_layout.addLayout(button_layout)

        self.add_btn = QPushButton("Add")
        self.add_btn.setObjectName("smallBtn")
        self.reset_btn = QPushButton("Reset")
        self.reset_btn.setObjectName("smallBtn")

        button_layout.addWidget(self.add_btn)
        button_layout.addWidget(self.reset_btn)

        self.add_btn.clicked.connect(self._on_add_clicked)
        
        self.reset_btn.clicked.connect(self._clear_fields)

        self.setStyleSheet("""
        QLabel#topic {
            font-size: 24px;
            font-weight: bold;
        }
        QLineEdit#input {
            min-height: 48px;
            font-size: 14px;
        }
        QLabel#fieldLabel {
            min-height: 48px;     
            font-size: 14px;
        }
        QPushButton#smallBtn {
            min-height: 32px;
            max-height: 32px;
            font-size: 18px;
        }
    """)

    def _on_add_clicked(self):
        first = self.first_name.text().strip()
        last = self.last_name.text().strip()
        phone = self.phone.text().strip()
        email = self.email.text().strip()

        if not (first and last and phone and email):
            return

        self.contact_added.emit(first, last, phone, email)
        self._clear_fields()

    def _clear_fields(self):
        self.first_name.clear()
        self.last_name.clear()
        self.email.clear()
        self.phone.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InputPanel()
    window.setFixedSize(500,400)
    window.show()
    sys.exit(app.exec())