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
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(4)

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
        self.layout.setSpacing(8)

        title_label = QLabel(title)
        title_label.setObjectName("sectionTitle")
        self.layout.addWidget(title_label)


class DashboardWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("АСУ испытаний авиационной техники")
        self.resize(1600, 900)
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
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)

        logo = QLabel("АСУ ИСПЫТАНИЙ\nАВИАЦИОННОЙ ТЕХНИКИ")
        logo.setObjectName("logo")
        layout.addWidget(logo)

        items = [
            "Главная",
            "Испытания",
            "Оборудование",
            "Лётчики-испытатели",
            "Отчёты",
            "Аналитика",
            "Документы",
            "НТД",
        ]
        for i, item in enumerate(items):
            btn = QPushButton(item)
            btn.setObjectName("menuBtn")
            if i == 0:
                btn.setProperty("active", True)
            btn.setCursor(Qt.PointingHandCursor)
            layout.addWidget(btn)

        layout.addStretch()

        tasks = SectionBox("Задачи на сегодня")
        for t in [
            "09:00 — Тест наземного контура",
            "10:40 — Ресурс крыла",
            "13:20 — Полётное задание №158",
            "16:10 — Сверка отчётов",
        ]:
            tasks.layout.addWidget(QLabel(f"• {t}"))
        layout.addWidget(tasks)
        return panel

    def _build_center(self) -> QWidget:
        panel = QFrame()
        panel.setObjectName("center")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)

        layout.addWidget(self._build_top_tabs())

        cards = QGridLayout()
        cards.setSpacing(10)
        stat = [
            ("24", "ТЕКУЩИХ ИСПЫТАНИЙ"),
            ("198", "УСПЕШНО ЗАВЕРШЕНЫ"),
            ("12", "ТЕСТИРУЕМЫХ САМОЛЁТОВ"),
            ("3", "ИСПЫТАТЕЛЬНЫХ ПОЛИГОНА"),
        ]
        for i, (value, label) in enumerate(stat):
            cards.addWidget(StatCard(value, label), 0, i)
        layout.addLayout(cards)

        history = SectionBox("ПРЕДЫДУЩИЕ ВЕРСИИ ОБРАЗЦА: МИ-35")
        for row in [
            "MI-35M (2020): модернизация авионики, повышена устойчивость к помехам.",
            "MI-35M2 (2022): новый вычислитель и модернизированный автопилот.",
            "MI-35M3 (2024): композитный модуль крыла, снижение массы на 8%.",
            "MI-35M4 (2025): защищённый канал телеметрии, обновлённая система диагностики.",
        ]:
            history.layout.addWidget(QLabel(row))
        layout.addWidget(history)

        tech = SectionBox("ТЕХНИЧЕСКИЕ ХАРАКТЕРИСТИКИ ОБРАЗЦА")
        specs = QGridLayout()
        specs.setHorizontalSpacing(24)
        specs.setVerticalSpacing(6)
        data = [
            ("Модель", "МИ-35M4"),
            ("Макс. скорость", "1 460 км/ч"),
            ("Рабочая высота", "15 245 м"),
            ("Дальность", "1 900 км"),
            ("Двигатель", "2 × ТРДДФ-9М"),
            ("Ресурс", "2 720 ч"),
        ]
        for r, (k, v) in enumerate(data):
            k_lbl = QLabel(k)
            k_lbl.setObjectName("specKey")
            v_lbl = QLabel(v)
            v_lbl.setObjectName("specVal")
            specs.addWidget(k_lbl, r, 0)
            specs.addWidget(v_lbl, r, 1)
        tech.layout.addLayout(specs)
        layout.addWidget(tech)

        title = QLabel("ЖУРНАЛ ИСПЫТАНИЙ")
        title.setObjectName("journalTitle")
        layout.addWidget(title)

        table = QTableWidget(15, 7)
        table.setObjectName("journalTable")
        table.setHorizontalHeaderLabels(
            ["ID", "Вид испытаний", "Испытание", "Объект", "Дата", "Ответственный", "Статус"]
        )
        rows = [
            ["50.MK1", "ГИ", "Исп. система", "Су-30МК1", "30 Апр", "А. Осмин", "Завершено"],
            ["B5-52-1", "ГСИ", "Вау-52-1", "Миг-35", "29 Апр", "Д. Пелов", "В процессе"],
            ["SU57-03", "ПИ", "Контур связи", "Су-57", "28 Апр", "Д. Пелов", "На активе"],
            ["SU35-11", "ПСИ", "Авионика", "Су-35", "27 Апр", "А. Левинов", "Ожидание"],
            ["SU57-14", "КЛИ", "Двигатель", "Су-57", "26 Апр", "М. Радцев", "На активе"],
            ["MI35-02", "СЛИ", "Система БРЭО", "МИ-35", "25 Апр", "О. Гуров", "Завершено"],
            ["SU30-07", "ГИ", "Шасси", "Су-30", "24 Апр", "И. Климов", "Завершено"],
            ["MIG29-09", "ГСИ", "Навигация", "МИГ-29Т", "23 Апр", "В. Линев", "В процессе"],
            ["SU34-01", "ПИ", "Радар", "Су-34", "22 Апр", "К. Орлов", "На активе"],
            ["YAK130-4", "ПСИ", "Канал связи", "Як-130", "21 Апр", "П. Власов", "Ожидание"],
            ["SU25-20", "КЛИ", "Топливная", "Су-25", "20 Апр", "Г. Сазонов", "На активе"],
            ["IL76-12", "СЛИ", "Борт сеть", "Ил-76", "19 Апр", "Н. Колесов", "Завершено"],
            ["TU214-08", "ГИ", "Автопилот", "Ту-214", "18 Апр", "Е. Миронов", "В процессе"],
            ["BE200-10", "ГСИ", "Силовая", "Бе-200", "17 Апр", "С. Карпов", "На активе"],
            ["A50-06", "ПИ", "Борт комплекс", "А-50", "16 Апр", "Р. Дёмин", "Завершено"],
        ]
        for r, row in enumerate(rows):
            for c, value in enumerate(row):
                table.setItem(r, c, QTableWidgetItem(value))

        table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(table)
        return panel

    def _build_top_tabs(self) -> QWidget:
        box = QFrame()
        box.setObjectName("topTabs")
        layout = QHBoxLayout(box)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)

        for i, tab in enumerate(["Главная", "Испытания", "Лётные испытания", "Оборудование", "Аналитика", "Настройки"]):
            btn = QPushButton(tab)
            btn.setObjectName("tabBtn")
            if i == 0:
                btn.setProperty("active", True)
            layout.addWidget(btn)
        layout.addStretch()
        return box

    def _build_right_panel(self) -> QWidget:
        panel = QFrame()
        panel.setObjectName("right")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(14, 16, 14, 16)
        layout.setSpacing(10)

        planned = SectionBox("ЗАПЛАНИРОВАННЫЕ ПОЛЁТЫ — СЕГОДНЯ")
        planned_rows = [
            "Объект: Су-30МК1 | Время: 09:20 | Кол-во: 2 | Цель: проверка РЛС | ПЗ: №154 | Тип: не боевое",
            "Объект: Миг-35 | Время: 11:10 | Кол-во: 1 | Цель: проверка двигателя | ПЗ: №155 | Тип: не боевое",
            "Объект: Су-57 | Время: 14:00 | Кол-во: 3 | Цель: проверка комплекса вооружения | ПЗ: №156 | Тип: боевое",
            "Объект: МИГ-29Т | Время: 16:40 | Кол-во: 1 | Цель: проверка БРЭО | ПЗ: №157 | Тип: не боевое",
        ]
        for item in planned_rows:
            lbl = QLabel(f"• {item}")
            lbl.setWordWrap(True)
            planned.layout.addWidget(lbl)
        layout.addWidget(planned)

        current_type = SectionBox("ТИП ТЕКУЩИХ ИСПЫТАНИЙ")
        current_type.layout.addWidget(QLabel("Испытание: ГСИ (государственные совместные испытания)"))
        current_type.layout.addWidget(QLabel("Цели: подтверждение ЛТХ, проверка устойчивости БРЭО, оценка отказоустойчивости"))
        current_type.layout.addWidget(QLabel("Контрольные параметры: скорость, высота, канал связи, расход топлива"))
        current_type.layout.addWidget(QLabel("Этап: лётная часть, 3-й цикл, телеметрия в норме"))
        layout.addWidget(current_type)

        scheme = SectionBox("СХЕМА ИСПЫТЫВАЕМОГО ОБРАЗЦА")
        scheme_text = QLabel(
            """
                    /\
               ____/  \____
          ____/___/||\___\____
             /  _  ||  _  \\
            /__/ \_||_/ \__\\
               \___/\___/
                /_/  \_\
               МИ-35M4
            """.strip("\n")
        )
        scheme_text.setObjectName("scheme")
        scheme_text.setAlignment(Qt.AlignCenter)
        scheme_text.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        scheme.layout.addWidget(scheme_text)
        layout.addWidget(scheme)

        layout.addStretch()
        return panel

    @staticmethod
    def _stylesheet() -> str:
        return """
        * {
            color: #10253f;
            font-family: 'Segoe UI', 'Inter', sans-serif;
            font-size: 13px;
        }

        QMainWindow, QWidget {
            background: #e8f2ff;
        }

        #sidebar {
            background: #d4e7ff;
            border-right: 1px solid #9fc1ea;
        }

        #center {
            background: #f3f8ff;
        }

        #right {
            background: #e7f1ff;
            border-left: 1px solid #9fc1ea;
        }

        #logo {
            font-size: 18px;
            font-weight: 700;
            color: #0d2f58;
            margin-bottom: 8px;
        }

        #menuBtn {
            text-align: left;
            padding: 9px 12px;
            border-radius: 8px;
            border: 1px solid #8cb4e2;
            background: #ffffff;
            color: #0f355f;
            font-weight: 600;
        }

        #menuBtn[active="true"] {
            background: #bcd9ff;
            border-color: #5f95d6;
        }

        #menuBtn:hover {
            background: #d8eaff;
        }

        #topTabs {
            background: #ffffff;
            border: 1px solid #9ec0e6;
            border-radius: 10px;
        }

        #tabBtn {
            padding: 7px 12px;
            border-radius: 7px;
            border: none;
            background: transparent;
            color: #174273;
            font-weight: 600;
        }

        #tabBtn[active="true"] {
            background: #c5defd;
            color: #0f355f;
        }

        #tabBtn:hover {
            background: #e2efff;
        }

        #statCard {
            border-radius: 10px;
            border: 1px solid #9dc1ea;
            background: #ffffff;
        }

        #cardValue {
            color: #0f355f;
            font-size: 32px;
            font-weight: 700;
        }

        #cardLabel {
            color: #365f8b;
            font-weight: 700;
        }

        #sectionBox {
            background: #ffffff;
            border: 1px solid #9ec0e8;
            border-radius: 10px;
        }

        #sectionTitle {
            font-size: 15px;
            font-weight: 700;
            color: #0f355f;
        }

        #specKey {
            color: #2e5c8f;
            font-weight: 600;
        }

        #specVal {
            color: #0f355f;
            font-weight: 700;
        }

        #journalTitle {
            font-size: 20px;
            font-weight: 700;
            color: #0f355f;
        }

        #journalTable {
            background: #ffffff;
            border: 1px solid #9ec0e8;
            border-radius: 10px;
            gridline-color: #c5daf4;
            selection-background-color: #dcecff;
            selection-color: #0f355f;
        }

        QHeaderView::section {
            background: #d8eaff;
            color: #0f355f;
            border: none;
            padding: 7px;
            font-weight: 700;
        }

        QTableWidget::item {
            padding: 5px;
            color: #10253f;
            background: #ffffff;
        }

        #scheme {
            background: #f8fbff;
            border: 1px dashed #96bbe6;
            border-radius: 10px;
            color: #123b67;
            font-family: 'Consolas', monospace;
            font-size: 14px;
            min-height: 170px;
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
