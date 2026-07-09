import os
import shutil
from pathlib import Path

from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton,
    QComboBox, QLineEdit, QTableWidget, QTableWidgetItem,
    QFileDialog, QMessageBox, QHeaderView
)

from app.database.db import (
    add_document,
    list_documents,
    delete_document,
    list_clients
)


DOCUMENTS_DIR = Path("data/documents")
DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)


class DocumentsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.build_ui()
        self.load_clients()
        self.load_documents()

    def build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 35, 40, 35)
        layout.setSpacing(14)

        title = QLabel("Evrak Takip")
        title.setStyleSheet("font-size:34px; font-weight:bold; color:#111827;")
        layout.addWidget(title)

        row = QHBoxLayout()

        self.client_combo = QComboBox()
        self.client_combo.setMinimumWidth(260)

        self.category = QLineEdit()
        self.category.setPlaceholderText("Kategori: Vergi Levhası, İmza Sirküsü, KDV...")

        self.add_btn = QPushButton("Evrak Ekle")
        self.open_btn = QPushButton("Dosyayı Aç")
        self.delete_btn = QPushButton("Seçili Evrakı Sil")

        self.add_btn.clicked.connect(self.add_file)
        self.open_btn.clicked.connect(self.open_selected)
        self.delete_btn.clicked.connect(self.delete_selected)

        row.addWidget(self.client_combo)
        row.addWidget(self.category)
        row.addWidget(self.add_btn)
        row.addWidget(self.open_btn)
        row.addWidget(self.delete_btn)

        layout.addLayout(row)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "ID", "Mükellef", "Dosya", "Kategori", "Yükleme Tarihi", "Yol"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        layout.addWidget(self.table)

        self.apply_style()

    def load_clients(self):
        self.client_combo.clear()

        clients = list_clients()

        if not clients:
            self.client_combo.addItem("Önce mükellef ekleyin", None)
            return

        for client in clients:
            client_id = client[0]
            client_name = client[1]
            self.client_combo.addItem(client_name, client_id)

    def add_file(self):
        client_id = self.client_combo.currentData()

        if not client_id:
            QMessageBox.warning(self, "Mükellef yok", "Önce bir mükellef seçmelisin.")
            return

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Evrak seç",
            "",
            "Belgeler (*.pdf *.doc *.docx *.xls *.xlsx *.jpg *.jpeg *.png);;Tüm Dosyalar (*)"
        )

        if not file_path:
            return

        source = Path(file_path)

        client_folder = DOCUMENTS_DIR / str(client_id)
        client_folder.mkdir(parents=True, exist_ok=True)

        target = client_folder / source.name
        shutil.copy2(source, target)

        category = self.category.text().strip()
        if not category:
            category = "Genel"

        add_document(
            client_id,
            source.name,
            str(target),
            category
        )

        self.category.clear()
        self.load_documents()

    def load_documents(self):
        rows = list_documents()
        self.table.setRowCount(len(rows))

        for row_index, row_data in enumerate(rows):
            for col_index, value in enumerate(row_data):
                self.table.setItem(
                    row_index,
                    col_index,
                    QTableWidgetItem(str(value))
                )

    def selected_document_id(self):
        row = self.table.currentRow()

        if row < 0:
            return None

        item = self.table.item(row, 0)

        if not item:
            return None

        return int(item.text())

    def selected_file_path(self):
        row = self.table.currentRow()

        if row < 0:
            return None

        item = self.table.item(row, 5)

        if not item:
            return None

        return item.text()

    def open_selected(self):
        file_path = self.selected_file_path()

        if not file_path:
            QMessageBox.warning(self, "Seçim yok", "Açmak için bir evrak seç.")
            return

        if not os.path.exists(file_path):
            QMessageBox.warning(self, "Dosya yok", "Dosya klasörde bulunamadı.")
            return

        os.startfile(file_path)

    def delete_selected(self):
        document_id = self.selected_document_id()

        if not document_id:
            QMessageBox.warning(self, "Seçim yok", "Silmek için bir evrak seç.")
            return

        answer = QMessageBox.question(
            self,
            "Silme Onayı",
            "Bu evrak kaydını silmek istediğine emin misin?"
        )

        if answer == QMessageBox.Yes:
            delete_document(document_id)
            self.load_documents()

    def apply_style(self):
        self.setStyleSheet("""
        QWidget {
            background:#f3f4f6;
        }

        QLineEdit, QComboBox {
            background:white;
            border:1px solid #cbd5e1;
            border-radius:8px;
            padding:9px;
            font-size:14px;
        }

        QPushButton {
            background:#2563eb;
            color:white;
            border:none;
            border-radius:8px;
            padding:10px 16px;
            font-size:14px;
            font-weight:bold;
            min-width:110px;
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