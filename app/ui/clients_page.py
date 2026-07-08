from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit,
    QTextEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QFrame, QMessageBox, QHeaderView
)

from app.database.db import (
    add_client, update_client, delete_client,
    list_clients, get_client
)


class ClientsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.selected_id = None
        self.build_ui()
        self.load_clients()

    def build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 35, 40, 35)
        layout.setSpacing(14)

        title = QLabel("Mükellefler")
        title.setStyleSheet("font-size:34px; font-weight:bold; color:#111827;")
        layout.addWidget(title)

        form = QFrame()
        form.setStyleSheet("background:white; border-radius:14px; padding:18px;")
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

        button_row = QHBoxLayout()
        button_row.addStretch()

        self.save_btn = QPushButton("Kaydet")
        self.update_btn = QPushButton("Güncelle")
        self.delete_btn = QPushButton("Sil")
        self.clear_btn = QPushButton("Temizle")

        self.save_btn.clicked.connect(self.save_client)
        self.update_btn.clicked.connect(self.update_selected_client)
        self.delete_btn.clicked.connect(self.delete_selected_client)
        self.clear_btn.clicked.connect(self.clear_form)

        button_row.addWidget(self.save_btn)
        button_row.addWidget(self.update_btn)
        button_row.addWidget(self.delete_btn)
        button_row.addWidget(self.clear_btn)

        form_layout.addLayout(row1)
        form_layout.addLayout(row2)
        form_layout.addWidget(self.notes)
        form_layout.addLayout(button_row)

        layout.addWidget(form)

        self.search = QLineEdit()
        self.search.setPlaceholderText("Mükellef ara...")
        self.search.textChanged.connect(self.load_clients)
        layout.addWidget(self.search)

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "ID", "Ad", "Vergi No", "Vergi Dairesi", "Telefon", "E-posta", "Yetkili"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.cellClicked.connect(self.table_clicked)
        layout.addWidget(self.table)

        self.apply_style()

    def save_client(self):
        if not self.name.text().strip():
            QMessageBox.warning(self, "Eksik bilgi", "Mükellef adı zorunludur.")
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

        self.clear_form()
        self.load_clients()

    def load_clients(self):
        rows = list_clients()
        keyword = self.search.text().lower() if hasattr(self, "search") else ""

        if keyword:
            rows = [row for row in rows if keyword in str(row).lower()]

        self.table.setRowCount(len(rows))

        for row_index, row_data in enumerate(rows):
            for col_index, value in enumerate(row_data):
                self.table.setItem(
                    row_index,
                    col_index,
                    QTableWidgetItem(str(value))
                )

    def table_clicked(self, row, column):
        item = self.table.item(row, 0)
        if not item:
            return

        self.selected_id = int(item.text())
        client = get_client(self.selected_id)
        if not client:
            return

        self.name.setText(client[1] or "")
        self.tax_no.setText(client[2] or "")
        self.tax_office.setText(client[3] or "")
        self.phone.setText(client[4] or "")
        self.email.setText(client[5] or "")
        self.contact.setText(client[6] or "")
        self.notes.setPlainText(client[7] or "")

    def update_selected_client(self):
        if not self.selected_id:
            QMessageBox.warning(self, "Seçim yok", "Güncellemek için tablodan bir mükellef seç.")
            return

        if not self.name.text().strip():
            QMessageBox.warning(self, "Eksik bilgi", "Mükellef adı zorunludur.")
            return

        update_client(
            self.selected_id,
            self.name.text(),
            self.tax_no.text(),
            self.tax_office.text(),
            self.phone.text(),
            self.email.text(),
            self.contact.text(),
            self.notes.toPlainText()
        )

        self.clear_form()
        self.load_clients()

    def delete_selected_client(self):
        if not self.selected_id:
            QMessageBox.warning(self, "Seçim yok", "Silmek için tablodan bir mükellef seç.")
            return

        answer = QMessageBox.question(
            self,
            "Silme Onayı",
            "Bu mükellefi silmek istediğine emin misin?"
        )

        if answer == QMessageBox.Yes:
            delete_client(self.selected_id)
            self.clear_form()
            self.load_clients()

    def clear_form(self):
        self.selected_id = None
        self.name.clear()
        self.tax_no.clear()
        self.tax_office.clear()
        self.phone.clear()
        self.email.clear()
        self.contact.clear()
        self.notes.clear()

    def apply_style(self):
        self.setStyleSheet("""
        QWidget { background:#f3f4f6; }

        QLineEdit, QTextEdit {
            background:white;
            border:1px solid #cbd5e1;
            border-radius:8px;
            padding:8px;
            font-size:14px;
        }

        QPushButton {
            background:#2563eb;
            color:white;
            border:none;
            border-radius:8px;
            padding:10px 18px;
            font-size:15px;
            font-weight:bold;
        }

        QPushButton:hover {
            background:#1d4ed8;
        }

        QTableWidget {
            background:white;
            border:1px solid #d1d5db;
            border-radius:10px;
            font-size:14px;
        }
        """)