from PySide6.QtWidgets import (
    QMainWindow, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QPushButton, QStackedWidget, QFrame
)

from app.ui.clients_page import ClientsPage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Oray Office Pro AI v0.4")
        self.resize(1400, 850)

        root = QWidget()
        root_layout = QHBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)

        self.pages = QStackedWidget()

        sidebar = self.build_sidebar()

        self.pages.addWidget(self.dashboard_page())
        self.pages.addWidget(self.simple_page("AI Asistan", "Doğal dil ile görev ve hatırlatma oluşturacağız."))
        self.pages.addWidget(ClientsPage())
        self.pages.addWidget(self.simple_page("Hatırlatıcılar", "Hatırlatıcı modülü burada olacak."))
        self.pages.addWidget(self.simple_page("Evrak", "Evrak takip modülü burada olacak."))
        self.pages.addWidget(self.simple_page("Vergi Takvimi", "Vergi takvimi burada olacak."))

        root_layout.addWidget(sidebar)
        root_layout.addWidget(self.pages)

        self.setCentralWidget(root)

    def build_sidebar(self):
        sidebar = QVBoxLayout()

        title = QLabel("🦉 Oray Office Pro")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: white; margin-bottom: 25px;")
        sidebar.addWidget(title)

        menu = ["Dashboard", "AI Asistan", "Mükellefler", "Hatırlatıcılar", "Evrak", "Vergi Takvimi"]

        for index, name in enumerate(menu):
            btn = QPushButton(name)
            btn.setMinimumHeight(46)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #1f2f55;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    font-size: 15px;
                    text-align: left;
                    padding-left: 18px;
                }
                QPushButton:hover {
                    background-color: #2f80ed;
                }
            """)
            btn.clicked.connect(lambda checked=False, i=index: self.pages.setCurrentIndex(i))
            sidebar.addWidget(btn)

        sidebar.addStretch()

        widget = QWidget()
        widget.setLayout(sidebar)
        widget.setFixedWidth(280)
        widget.setStyleSheet("background-color: #14213d; padding: 24px;")
        return widget

    def dashboard_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 35, 40, 35)

        title = QLabel("Dashboard")
        title.setStyleSheet("font-size: 34px; font-weight: bold; color: #111827;")

        subtitle = QLabel("Günaydın Oray. Bugünkü ofis durumun aşağıda.")
        subtitle.setStyleSheet("font-size: 17px; color: #4b5563; margin-bottom: 20px;")

        cards = QHBoxLayout()
        cards.addWidget(self.card("📌 Bugünkü İşler", "0", "Bekleyen görev"))
        cards.addWidget(self.card("⏰ Hatırlatıcılar", "0", "Aktif hatırlatma"))
        cards.addWidget(self.card("👥 Mükellefler", "0", "Kayıtlı mükellef"))
        cards.addWidget(self.card("📂 Evrak", "0", "Takipte evrak"))

        activity = QFrame()
        activity.setStyleSheet("background-color: white; border-radius: 14px; padding: 22px;")
        activity_layout = QVBoxLayout(activity)

        activity_title = QLabel("Yaklaşan İşler")
        activity_title.setStyleSheet("font-size: 22px; font-weight: bold; color: #111827;")

        empty = QLabel("Henüz yaklaşan iş yok.")
        empty.setStyleSheet("font-size: 16px; color: #6b7280; margin-top: 12px;")

        activity_layout.addWidget(activity_title)
        activity_layout.addWidget(empty)
        activity_layout.addStretch()

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addLayout(cards)
        layout.addWidget(activity)
        layout.addStretch()

        page.setStyleSheet("background-color: #f3f4f6;")
        return page

    def card(self, title, value, desc):
        frame = QFrame()
        frame.setStyleSheet("background-color: white; border-radius: 14px; padding: 20px;")
        layout = QVBoxLayout(frame)

        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 16px; color: #374151;")

        value_label = QLabel(value)
        value_label.setStyleSheet("font-size: 34px; font-weight: bold; color: #111827;")

        desc_label = QLabel(desc)
        desc_label.setStyleSheet("font-size: 14px; color: #6b7280;")

        layout.addWidget(title_label)
        layout.addWidget(value_label)
        layout.addWidget(desc_label)

        return frame

    def simple_page(self, title_text, desc_text):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 35, 40, 35)

        title = QLabel(title_text)
        title.setStyleSheet("font-size: 34px; font-weight: bold; color: #111827;")

        desc = QLabel(desc_text)
        desc.setStyleSheet("font-size: 18px; color: #4b5563;")

        layout.addWidget(title)
        layout.addWidget(desc)
        layout.addStretch()

        page.setStyleSheet("background-color: #f3f4f6;")
        return page