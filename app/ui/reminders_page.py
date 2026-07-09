from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QPushButton, QComboBox, QLineEdit,
    QTextEdit, QTableWidget, QTableWidgetItem,
    QMessageBox, QHeaderView
)

from app.database.db import (
    list_clients,
    add_reminder,
    list_reminders,
    delete_reminder
)


class RemindersPage(QWidget):
    def __init__(self):
        super().__init__()

        self.build_ui()
        self.load_clients()
        self.load_reminders()

    def build_ui(self):
        layout = QVBoxLayout(self)

        title = QLabel("Hatırlatıcılar")
        title.setStyleSheet("font-size:30px;font-weight:bold;")
        layout.addWidget(title)

        row = QHBoxLayout()

        self.client_combo = QComboBox()

        self.title_edit = QLineEdit()
        self.title_edit.setPlaceholderText("Hatırlatma")

        self.date_edit = QLineEdit()
        self.date_edit.setPlaceholderText("2026-07-31")

        row.addWidget(self.client_combo)
        row.addWidget(self.title_edit)
        row.addWidget(self.date_edit)

        layout.addLayout(row)

        self.notes = QTextEdit()
        self.notes.setPlaceholderText("Not")

        layout.addWidget(self.notes)

        buttons = QHBoxLayout()

        self.save_btn = QPushButton("Kaydet")
        self.delete_btn = QPushButton("Sil")

        self.save_btn.clicked.connect(self.save_reminder)
        self.delete_btn.clicked.connect(self.delete_selected)

        buttons.addWidget(self.save_btn)
        buttons.addWidget(self.delete_btn)

        layout.addLayout(buttons)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "ID",
            "Mükellef",
            "Başlık",
            "Tarih",
            "Durum",
            "Not"
        ])

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        layout.addWidget(self.table)

    def load_clients(self):
        self.client_combo.clear()

        for client in list_clients():
            self.client_combo.addItem(client[1], client[0])

    def load_reminders(self):
        rows = list_reminders()

        self.table.setRowCount(len(rows))

        for r, row in enumerate(rows):
            for c, value in enumerate(row):
                self.table.setItem(r, c, QTableWidgetItem(str(value)))

    def save_reminder(self):
        client_id = self.client_combo.currentData()

        if client_id is None:
            QMessageBox.warning(self, "Hata", "Mükellef seçiniz.")
            return

        add_reminder(
            client_id,
            self.title_edit.text(),
            self.date_edit.text(),
            "Bekliyor",
            self.notes.toPlainText()
        )

        self.title_edit.clear()
        self.date_edit.clear()
        self.notes.clear()

        self.load_reminders()

    def delete_selected(self):
        row = self.table.currentRow()

        if row < 0:
            return

        reminder_id = int(self.table.item(row, 0).text())

        delete_reminder(reminder_id)

        self.load_reminders()