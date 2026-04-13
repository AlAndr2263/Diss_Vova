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
        layout.setContentsMargins(16, 12, 16, 12)

        value_label = QLabel(value)
        value_label.setObjectName("cardValue")
        label_label = QLabel(label)
        label_label.setObjectName("cardLabel")
        label_label.setWordWrap(True)

        layout.addWidget(value_label)
        layout.addWidget(label_label)


class DashboardWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("АСУ испытаний авиационной техники")
        self.resize(1366, 768)
        self._build_ui()

    def _build_ui(self):
        root = QWidget()
        root_layout = QHBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        sidebar = self._build_sidebar()
        center = self._build_center_panel()
        right = self._build_right_panel()

        root_layout.addWidget(sidebar, 2)
        root_layout.addWidget(center, 8)
        root_layout.addWidget(right, 4)

        self.setCentralWidget(root)
        self.setStyleSheet(self._stylesheet())

    def _build_sidebar(self) -> QWidget:
        panel = QFrame()
        panel.setObjectName("sidebar")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(18, 18, 18, 18)

        title = QLabel("АСУ ИСПЫТАНИЙ\nАВИАЦИОННОЙ ТЕХНИКИ")
        title.setObjectName("logo")
        layout.addWidget(title)

        for item in [
            "Главная",
            "Испытания",
            "Оборудование",
            "Летчики-испытатели",
            "Отчёты",
            "Аналитика",
            "Документы",
        ]:
            b = QPushButton(item)
            b.setObjectName("menuBtn")
            b.setCursor(Qt.PointingHandCursor)
            layout.addWidget(b)

        layout.addStretch()

        task = QLabel("Задачи на сегодня\n\n09:00 Тест\n10:30 Ресурсные\n13:00 Обед\n13:30 Полет")
        task.setObjectName("taskBox")
        layout.addWidget(task)
        return panel

    def _build_center_panel(self) -> QWidget:
        panel = QFrame()
        panel.setObjectName("center")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        header = QLabel("ПАНЕЛЬ УПРАВЛЕНИЯ")
        header.setObjectName("header")
        layout.addWidget(header)

        cards = QGridLayout()
        cards.setSpacing(10)
        data = [
            ("24", "ТЕКУЩИХ ИСПЫТАНИЙ"),
            ("198", "УСПЕШНО ЗАВЕРШЕНЫ"),
            ("12", "ТЕСТИРУЕМЫХ САМОЛЕТОВ"),
            ("3", "ИСПЫТАТЕЛЬНЫХ ПОЛИГОНА"),
        ]
        for i, (v, t) in enumerate(data):
            cards.addWidget(StatCard(v, t), 0, i)
        layout.addLayout(cards)

        week = QFrame()
        week.setObjectName("chart")
        week_layout = QVBoxLayout(week)
        week_layout.addWidget(QLabel("СТАТИСТИКА НЕДЕЛИ"))
        lines = QLabel("▁▃▂▄▅▆▅▇\n▂▂▃▃▄▅▃▄\n▁▂▂▃▃▂▄▅")
        lines.setObjectName("asciiChart")
        week_layout.addWidget(lines)
        layout.addWidget(week)

        table_title = QLabel("ЖУРНАЛ ИСПЫТАНИЙ")
        table_title.setObjectName("section")
        layout.addWidget(table_title)

        table = QTableWidget(5, 6)
        table.setHorizontalHeaderLabels(
            ["ID", "Испытание", "Объект", "Дата", "Ответственный", "Статус"]
        )
        table_data = [
            ["50.MK1", "Исп. система", "Су-30МК1", "30 Апр", "Алексей Осмин", "Завершено"],
            ["B5-52-1", "Вау-52-1", "Миг-35", "29 Апр", "Дмитрий Пелов", "В процессе"],
            ["Су-57", "Су-57", "Су-57", "28 Апр", "Дмитрий Пелов", "На активе"],
            ["Су-35", "Авионика", "Су-35", "27 Апр", "Андрей Левинов", "Застрело"],
            ["Су-57", "Двигатель", "Су-57", "26 Апр", "Михаил Радцев", "На активе"],
        ]
        for r, row in enumerate(table_data):
            for c, v in enumerate(row):
                table.setItem(r, c, QTableWidgetItem(v))

        table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(table)
        return panel

    def _build_right_panel(self) -> QWidget:
        panel = QFrame()
        panel.setObjectName("right")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(14, 16, 14, 16)
        layout.setSpacing(12)

        prog = QFrame()
        prog.setObjectName("box")
        p_layout = QVBoxLayout(prog)
        p_layout.addWidget(QLabel("ПРОГРАММНЫЕ ПОЛЕТЫ — СЕГОДНЯ"))
        for flight in ["Су-30МК1 — В ПОЛЕТЕ", "Миг-35 — 99 вылетов", "Су-57 — Вакур", "МИГ-29Т — #158"]:
            p_layout.addWidget(QLabel(f"• {flight}"))
        layout.addWidget(prog)

        current = QFrame()
        current.setObjectName("box")
        c_layout = QVBoxLayout(current)
        c_layout.addWidget(QLabel("ТЕКУЩИЙ ПОЛЕТ #Тест-245"))
        c_layout.addWidget(QLabel("МИ-35\nВысота: 15 245 м\nСкорость: 1 460 км/ч\nОсталось: 45 мин"))
        map_mock = QLabel("   ✈\n  ╱│╲\n ╱ │ ╲\nГРАФИЧЕСКИЙ РАДАР")
        map_mock.setObjectName("map")
        map_mock.setAlignment(Qt.AlignCenter)
        c_layout.addWidget(map_mock)
        layout.addWidget(current)

        layout.addStretch()
        return panel

    @staticmethod
    def _stylesheet() -> str:
        return """
        * { color: #dfeeff; font-family: 'Segoe UI'; font-size: 13px; }
        QMainWindow, QWidget { background: #0e3a71; }
        #sidebar { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #0f447f, stop:1 #0a2d58); }
        #center { background: #1a4e8f; }
        #right { background: #133e75; }
        #logo { font-size: 18px; font-weight: 700; margin-bottom: 14px; }
        #menuBtn { text-align: left; padding: 10px; border: 1px solid #3569a6; border-radius: 6px; background: #184f8f; }
        #menuBtn:hover { background: #2363ac; }
        #taskBox { border: 1px solid #4f79ac; border-radius: 8px; background: #12457f; padding: 10px; }
        #header { font-size: 26px; font-weight: 700; }
        #section { font-size: 21px; font-weight: 600; margin-top: 8px; }
        #statCard { border: 1px solid #7fb0db; border-radius: 8px; background: #dceffd; color: #234; }
        #cardValue { color: #1b4f8e; font-size: 42px; font-weight: 700; }
        #cardLabel { color: #325274; font-size: 13px; font-weight: 700; }
        #chart { border: 1px solid #6f98c8; border-radius: 8px; background: #2b639f; padding: 8px; }
        #asciiChart { font-family: 'Consolas'; font-size: 24px; color: #c8eeff; }
        #box { border: 1px solid #4d78aa; border-radius: 10px; background: #184d88; padding: 10px; }
        #map { border: 1px dashed #7fa6d4; border-radius: 8px; min-height: 160px; background: #1d558f; }
        QTableWidget { background: #1d568f; gridline-color: #5e87b9; border: 1px solid #5d87b9; border-radius: 8px; }
        QHeaderView::section { background: #2e6aa8; color: #eef7ff; padding: 6px; border: none; }
        QTableWidget::item { padding: 4px; }
        """


def main() -> None:
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))
    window = DashboardWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
