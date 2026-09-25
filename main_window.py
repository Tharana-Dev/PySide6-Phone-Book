from model import ContactBook
from input_panel import InputPanel
from list_panel import ContactListPanel

from PySide6.QtWidgets import QMainWindow, QTabWidget, QWidget, QVBoxLayout


class MainWindow(QMainWindow):
    def __init__(self,book:ContactBook):
        super().__init__()
        self.setWindowTitle("My Phone Book")
        self.setFixedSize(500, 400)

        self.book = book
        self.data_panel = InputPanel()
        self.contact_list = ContactListPanel()

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)

        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

# -------Tab 1---------------------
        self.tabs.addTab(self.data_panel, "Add Data")

# ------Tab 2----------------------
        self.tabs.addTab(self.contact_list, "View Contacts")

        self.contact_list.refresh(self.book.contacts)
        
#-----wiring the signals----------
        self.data_panel.contact_added.connect(self._add_contact)
        self.contact_list.delete_requested.connect(self._delete_contact)

    def _add_contact(self, first, last, phone, email):
        self.book.add(first, last, phone, email)
        self.contact_list.refresh(self.book.contacts)
        self.tabs.setCurrentWidget(self.contact_list)

    def _delete_contact(self, rows):
        for row in sorted(rows, reverse=True):
            self.book.remove(row)
        self.contact_list.refresh(self.book.contacts)