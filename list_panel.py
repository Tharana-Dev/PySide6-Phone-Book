from PySide6.QtWidgets import QVBoxLayout, QLabel, QMessageBox, QListWidget, QWidget, QPushButton
from PySide6.QtCore import Signal, Qt


class ContactListPanel(QWidget):
    delete_requested = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)

        outer_layout = QVBoxLayout(self)

        topic = QLabel("Contacts")
        topic.setObjectName("topic")
        topic.setAlignment(Qt.AlignmentFlag.AlignCenter)
        outer_layout.addWidget(topic)

        self.list_widget = QListWidget()
        self.delete_btn = QPushButton("Delete")

        self.list_widget.setSpacing(5)
        self.list_widget.setItemAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        outer_layout.addWidget(self.list_widget)
        outer_layout.addWidget(self.delete_btn)

        self.delete_btn.clicked.connect(self._on_delete_clicked)

        self.setStyleSheet("""
            QListWidget {
                font-size: 24px;
                min-height: 200px;
            }
            QListWidget::item {
                min-height: 50px;
                padding: 6px 10px;
            }
            QListWidget::item:selected {
                background: palette(highlight);
                color: palette(highlighted-text);
            }
            QPushButton {
                min-height: 36px;
                font-size: 24px;
            }
            QLabel {
            font-size: 32px;
            font-weight: bold;
            padding: 6px 12px;
        }
        """)

    def refresh(self, contacts: list) -> None:  # contacts not imported for the MVP model
        self.list_widget.clear()

        if not contacts:
            self.list_widget.addItem("No Contacts Yet")
            self.list_widget.setItemAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            self.list_widget.setSelectionMode(self.list_widget.SelectionMode.NoSelection)
        else:
            self.list_widget.setSelectionMode(self.list_widget.SelectionMode.ExtendedSelection)
            for c in contacts:
                self.list_widget.addItem(f"{c.first_name} {c.last_name} \n  {c.phone} - {c.email}")

    def _on_delete_clicked(self):
        items = self.list_widget.selectedItems()
        if not items:
            QMessageBox.warning(self, "Nothing selected", "Pick a contact first.")
            return

        rows = [self.list_widget.row(item) for item in items]
        self.delete_requested.emit(rows)

if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication
    from model import Contact

    app = QApplication(sys.argv)
    panel = ContactListPanel()
    panel.setFixedSize(500, 400)
    panel.refresh([
        Contact("Ada", "Lovelace", "0123456789", "a@b.com"),
        Contact("Ada", "Lovelace", "0123456789", "a@b.com"),
        Contact("Ada", "Lovelace", "0123456789", "a@b.com"),
        Contact("Ada", "Lovelace", "0123456789", "a@b.com"),
        Contact("Ada", "Lovelace", "0123456789", "a@b.com"),
        Contact("Ada", "Lovelace", "0123456789", "a@b.com"),
        Contact("Alan", "Turing", "0123456789", "t@b.com"),
    ])
    panel.show()
    panel.delete_requested.connect(lambda row: print(f"delete row {row}"))
    sys.exit(app.exec())