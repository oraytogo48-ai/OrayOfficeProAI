from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit,
    QTextEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QFrame
)

from app.database.db import add_client, list_clients


class ClientsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.build_ui()
        self.load_clients()

    def build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 35, 40, 35)

        title = QLabel("Mükellefler")
        title.setStyleSheet("font-size: 34px; font-weight: bold; color: #111827;")
        layout.addWidget(title)

        form = QFrame()
        form.setStyleSheet("background-color: white; border-radius: 14px; padding: 18px;")
        form_layout = QVBoxLayout(form)

        row1 = QHBoxLayout()
        self.name = QLineEdit()
        self.name.setPlaceholderText("Firma / Mükellef adı")
        self.tax_no = QLineEdit()
        self.tax_no.setPlaceholderText("Vergi No / TCKN")
        self.tax_office = QLineEdit()
        self.tax_office.setPlaceholderText("Vergi Dairesi")
        row1.addWidget(self.name)
        row1.addWidget(self.tax_no)
        row1.addWidget(self.tax_office)

        row2 = QHBoxLayout()
        self.phone = QLineEdit()
        self.phone.setPlaceholderText("Telefon")
        self.email = QLineEdit()
        self.email.setPlaceholderText("E-posta")
        self.contact = QLineEdit()
        self.contact.setPlaceholderText("Yetkili kişi")
        row2.addWidget(self.phone)
        row2.addWidget(self.email)
        row2.addWidget(self.contact)

        self.notes = QTextEdit()
        self.notes.setPlaceholderText("Notlar")
        self.notes.setFixedHeight(80)

        save_btn = QPushButton("Mükellef Kaydet")
        save_btn.setMinimumHeight(42)
        save_btn.clicked.connect(self.save_client)

        form_layout.addLayout(row1)
        form_layout.addLayout(row2)
        form_layout.addWidget(self.notes)
        form_layout.addWidget(save_btn)

        layout.addWidget(form)

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "ID", "Ad", "Vergi No", "Vergi Dairesi", "Telefon", "E-posta", "Yetkili"
        ])
        layout.addWidget(self.table)

        self.setStyleSheet("""
QWidget{
    background:#f3f4f6;
}

QLineEdit{
    background:white;
    border:1px solid #cbd5e1;
    border-radius:8px;
    padding:8px;
    font-size:14px;
}

QTextEdit{
    background:white;
    border:1px solid #cbd5e1;
    border-radius:8px;
    padding:8px;
    font-size:14px;
}

QPushButton{
    background:#2563eb;
    color:white;
    border:none;
    border-radius:8px;
    padding:10px;
    font-size:15px;
    font-weight:bold;
}

QPushButton:hover{
    background:#1d4ed8;
}

QTableWidget{
    background:white;
    border:1px solid #d1d5db;
    border-radius:10px;
}
""")

    def save_client(self):
        if not self.name.text().strip():
            return

        add_client(
            self.name.text(),
            self.tax_no.text(),
            self.tax_office.text(),
            self.phone.text(),
            self.email.text(),
            self.contact.text(),
            self.notes.toPlainText()
        )

        self.name.clear()
        self.tax_no.clear()
        self.tax_office.clear()
        self.phone.clear()
        self.email.clear()
        self.contact.clear()
        self.notes.clear()

        self.load_clients()

    def load_clients(self):
        rows = list_clients()
        self.table.setRowCount(len(rows))

        for row_index, row_data in enumerate(rows):
            for col_index, value in enumerate(row_data):
                self.table.setItem(row_index, col_index, QTableWidgetItem(str(value)))