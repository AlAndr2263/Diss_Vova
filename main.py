import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QApplication,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class StatCard(QFrame):
    def __init__(self, value: str, label: str):
        super().__init__()
        self.setObjectName("statCard")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 14, 18, 14)
        layout.setSpacing(6)

        value_label = QLabel(value)
        value_label.setObjectName("cardValue")

        label_label = QLabel(label)
        label_label.setObjectName("cardLabel")
        label_label.setWordWrap(True)

        layout.addWidget(value_label)
        layout.addWidget(label_label)


class SectionBox(QFrame):
    def __init__(self, title: str):
        super().__init__()
        self.setObjectName("sectionBox")
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(14, 14, 14, 14)
        self.layout.setSpacing(10)

        title_label = QLabel(title)
        title_label.setObjectName("sectionTitle")
        self.layout.addWidget(title_label)


class DashboardWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("АСУ испытаний авиационной техники")
        self.resize(1520, 860)
        self._build_ui()

    def _build_ui(self) -> None:
        root = QWidget()
        root_layout = QHBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        root_layout.addWidget(self._build_sidebar(), 2)
        root_layout.addWidget(self._build_center(), 8)
        root_layout.addWidget(self._build_right_panel(), 4)

        self.setCentralWidget(root)
        self.setStyleSheet(self._stylesheet())

    def _build_sidebar(self) -> QWidget:
        panel = QFrame()
        panel.setObjectName("sidebar")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(10)

        logo = QLabel("АСУ ИСПЫТАНИЙ\nАВИАЦИОННОЙ ТЕХНИКИ")
        logo.setObjectName("logo")
        layout.addWidget(logo)

        menu_items = [
            "Главная",
            "Испытания",
            "Оборудование",
            "Лётчики-испытатели",
            "Отчёты",
            "Аналитика",
            "Документы",
            "НТД",
        ]

        for i, item in enumerate(menu_items):
            btn = QPushButton(item)
            btn.setObjectName("menuBtn")
            if i == 0:
                btn.setProperty("active", True)
            btn.setCursor(Qt.PointingHandCursor)
            layout.addWidget(btn)

        layout.addStretch()

        today = SectionBox("ЗАДАЧИ НА СЕГОДНЯ")
        for task in [
            "09:00 — Тест наземного контура",
            "10:30 — Проверка ресурса крыла",
            "13:30 — Полёт №245",
            "16:00 — Синхронизация телеметрии",
        ]:
            today.layout.addWidget(QLabel(f"• {task}"))
        layout.addWidget(today)
        return panel

    def _build_center(self) -> QWidget:
        panel = QFrame()
        panel.setObjectName("center")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        top_bar = self._build_top_tabs()
        layout.addWidget(top_bar)

        cards_layout = QGridLayout()
        cards_layout.setSpacing(10)
        cards = [
            ("24", "ТЕКУЩИХ ИСПЫТАНИЙ"),
            ("198", "УСПЕШНО ЗАВЕРШЕНЫ"),
            ("12", "ТЕСТИРУЕМЫХ САМОЛЁТОВ"),
            ("3", "ИСПЫТАТЕЛЬНЫХ ПОЛИГОНА"),
        ]
        for idx, (value, label) in enumerate(cards):
            cards_layout.addWidget(StatCard(value, label), 0, idx)
        layout.addLayout(cards_layout)

        history = SectionBox("ПРЕДЫДУЩИЕ ВЕРСИИ ОБРАЗЦА: МИ-35")
        history.layout.addWidget(QLabel("MI-35M (2020): модернизация авионики, повышена устойчивость к помехам."))
        history.layout.addWidget(QLabel("MI-35M2 (2022): новый бортовой вычислитель, улучшен контур автопилота."))
        history.layout.addWidget(QLabel("MI-35M3 (2024): облегчённый композитный модуль крыла, снижена масса на 8%."))
        history.layout.addWidget(QLabel("MI-35M4 (2025): интеграция защищённого канала телеметрии и AI-предиктора отказов."))
        layout.addWidget(history)

        tech = SectionBox("ТЕХНИЧЕСКИЕ ХАРАКТЕРИСТИКИ ОБРАЗЦА")
        tech_grid = QGridLayout()
        tech_grid.setHorizontalSpacing(24)
        tech_grid.setVerticalSpacing(8)
        specs = [
            ("Модель", "МИ-35M4"),
            ("Макс. скорость", "1 460 км/ч"),
            ("Рабочая высота", "15 245 м"),
            ("Дальность", "1 900 км"),
            ("Двигатель", "2 × ТРДДФ-9М"),
            ("Наработка ресурса", "2 720 ч"),
        ]
        for row, (k, v) in enumerate(specs):
            key = QLabel(k)
            key.setObjectName("specKey")
            val = QLabel(v)
            val.setObjectName("specVal")
            tech_grid.addWidget(key, row, 0)
            tech_grid.addWidget(val, row, 1)
        tech.layout.addLayout(tech_grid)
        layout.addWidget(tech)

        journal_title = QLabel("ЖУРНАЛ ИСПЫТАНИЙ")
        journal_title.setObjectName("journalTitle")
        layout.addWidget(journal_title)

        table = QTableWidget(5, 6)
        table.setObjectName("journalTable")
        table.setHorizontalHeaderLabels(["ID", "Испытание", "Объект", "Дата", "Ответственный", "Статус"])
        table_data = [
            ["50.MK1", "Исп. система", "Су-30МК1", "30 Апр", "Алексей Осмин", "Завершено"],
            ["B5-52-1", "Вау-52-1", "Миг-35", "29 Апр", "Дмитрий Пелов", "В процессе"],
            ["Су-57", "Контур связи", "Су-57", "28 Апр", "Дмитрий Пелов", "На активе"],
            ["Су-35", "Авионика", "Су-35", "27 Апр", "Андрей Левинов", "Ожидание"],
            ["Су-57", "Двигатель", "Су-57", "26 Апр", "Михаил Радцев", "На активе"],
        ]
        for r, row in enumerate(table_data):
            for c, value in enumerate(row):
                table.setItem(r, c, QTableWidgetItem(value))

        table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(table)
        return panel

    def _build_top_tabs(self) -> QWidget:
        container = QFrame()
        container.setObjectName("topTabs")
        layout = QHBoxLayout(container)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)

        tabs = ["Главная", "Испытания", "Лётные испытания", "Оборудование", "Аналитика", "Настройки"]
        for i, tab in enumerate(tabs):
            btn = QPushButton(tab)
            btn.setObjectName("tabBtn")
            if i == 0:
                btn.setProperty("active", True)
            btn.setCursor(Qt.PointingHandCursor)
            layout.addWidget(btn)

        layout.addStretch()
        return container

    def _build_right_panel(self) -> QWidget:
        panel = QFrame()
        panel.setObjectName("right")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(14, 16, 14, 16)
        layout.setSpacing(12)

        flights = SectionBox("ПРОГРАММНЫЕ ПОЛЁТЫ — СЕГОДНЯ")
        for row in [
            "Су-30МК1 — В полёте",
            "Миг-35 — 99 вылетов",
            "Су-57 — Вакур",
            "МИГ-29Т — #158",
        ]:
            item = QLabel(f"• {row}")
            item.setObjectName("flightItem")
            flights.layout.addWidget(item)
        layout.addWidget(flights)

        current = SectionBox("ТЕКУЩИЙ ПОЛЁТ #ТЕСТ-245")
        current.layout.addWidget(QLabel("Борт: МИ-35"))
        current.layout.addWidget(QLabel("Высота: 15 245 м"))
        current.layout.addWidget(QLabel("Скорость: 1 460 км/ч"))
        current.layout.addWidget(QLabel("Топливо: 62%"))

        radar = QLabel("   ✈\n╭──────────╮\n│ ТРАЕКТОРИЯ │\n╰──────────╯")
        radar.setObjectName("radar")
        radar.setAlignment(Qt.AlignCenter)
        radar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        current.layout.addWidget(radar)

        layout.addWidget(current)
        layout.addStretch()
        return panel

    @staticmethod
    def _stylesheet() -> str:
        return """
        * {
            color: #f2f7ff;
            font-family: 'Segoe UI', 'Inter', sans-serif;
            font-size: 13px;
        }

        QMainWindow, QWidget {
            background: #0b1220;
        }

        #sidebar {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #0f2a4d, stop:1 #081a31);
            border-right: 1px solid #1e3a5f;
        }

        #center {
            background: #0f1f36;
        }

        #right {
            background: #0c1a2f;
            border-left: 1px solid #1e3a5f;
        }

        #logo {
            font-size: 18px;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 8px;
        }

        #menuBtn {
            text-align: left;
            padding: 10px 12px;
            border-radius: 8px;
            border: 1px solid #254a77;
            background: #112846;
            color: #e8f0fb;
            font-weight: 600;
        }

        #menuBtn[active="true"] {
            background: #1b63b8;
            border-color: #2c78d1;
            color: #ffffff;
        }

        #menuBtn:hover {
            background: #173a64;
        }

        #topTabs {
            background: #122946;
            border: 1px solid #24466e;
            border-radius: 10px;
        }

        #tabBtn {
            padding: 8px 12px;
            border-radius: 8px;
            border: none;
            background: transparent;
            color: #d8e7ff;
            font-weight: 600;
        }

        #tabBtn[active="true"] {
            background: #205ea8;
            color: #ffffff;
        }

        #tabBtn:hover {
            background: #173c68;
        }

        #statCard {
            border-radius: 10px;
            border: 1px solid #2b4f79;
            background: #132a46;
        }

        #cardValue {
            color: #ffffff;
            font-size: 36px;
            font-weight: 700;
        }

        #cardLabel {
            color: #bcd4f4;
            font-size: 12px;
            font-weight: 700;
        }

        #sectionBox {
            background: #122946;
            border: 1px solid #2a4d77;
            border-radius: 10px;
        }

        #sectionTitle {
            font-size: 15px;
            font-weight: 700;
            color: #ffffff;
        }

        #specKey {
            color: #9ec0ea;
            font-weight: 600;
        }

        #specVal {
            color: #ffffff;
            font-weight: 700;
        }

        #journalTitle {
            font-size: 20px;
            font-weight: 700;
            color: #ffffff;
            margin-top: 2px;
        }

        #journalTable {
            background: #122846;
            border: 1px solid #2d507a;
            border-radius: 10px;
            gridline-color: #355a86;
            selection-background-color: #1e62af;
        }

        QHeaderView::section {
            background: #173a64;
            color: #ffffff;
            border: none;
            padding: 7px;
            font-weight: 700;
        }

        QTableWidget::item {
            padding: 6px;
        }

        #flightItem {
            color: #d8e8ff;
            font-weight: 600;
        }

        #radar {
            min-height: 170px;
            background: #0f223b;
            border: 1px dashed #4c76a4;
            border-radius: 10px;
            color: #d6e8ff;
            font-family: 'Consolas', monospace;
            font-size: 15px;
        }
        """


def main() -> None:
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))
    window = DashboardWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
