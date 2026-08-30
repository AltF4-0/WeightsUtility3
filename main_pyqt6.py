#!/usr/bin/env python3
import os
import sys

from PyQt6.QtCore import (
    QMimeData,
    QRectF,
    Qt,
    QTimer,
    pyqtSignal,
)
from PyQt6.QtGui import (
    QColor,
    QDragEnterEvent,
    QDropEvent,
    QFont,
    QIcon,
    QPainter,
)
from PyQt6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from excel_modifier import modify_excel
from pdf_modifier import modify_pdf
from theme import (
DARK_STYLESHEET,
LIGHT_STYLESHEET,
)

# Resource paths
BASE_DIR = os.path.expanduser("~")
os.chdir(BASE_DIR)

def resource_path(relative):
    base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, relative)

# Toggle Widgets
class ToggleSwitch(QWidget):
    def __init__(self, label: str, parent=None):
        super().__init__(parent)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        self._track = QPushButton()
        self._track.setFixedSize(52, 28)
        self._track.setCheckable(True)
        self._track.setCursor(Qt.CursorShape.PointingHandCursor)
        self._track.setObjectName("toggleOff")
        self._track.toggled.connect(self._on_toggle)

        self._label = QLabel(label)
        self._label.setFont(QFont("Segoe UI", 12))

        layout.addWidget(self._track)
        layout.addWidget(self._label)

    def _on_toggle(self, checked: bool):
        self._track.setObjectName("toggleOn" if checked else "toggleOff")
        style = self._track.style()
        if style is not None:
            style.unpolish(self._track)
            style.polish(self._track)
        self._track.update()

    def isChecked(self) -> bool:
        return self._track.isChecked()


# Theme toggle
class ThemeToggle(QWidget):
    toggled = pyqtSignal(bool)

    def __init__(self, parent=None, dark_mode: bool = False):
        super().__init__(parent)
        self.setFixedSize(40, 20)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self._dark_mode = dark_mode
        self._notch_pos = 1.0 if dark_mode else 0.0
        self._notch_target = self._notch_pos

        self._timer = QTimer(self)
        self._timer.setInterval(15)
        self._timer.timeout.connect(self._animate_step)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._dark_mode = not self._dark_mode
            self._notch_target = 1.0 if self._dark_mode else 0.0
            self._timer.start()
            self.toggled.emit(self._dark_mode)

    def _animate_step(self):
        step = 0.18
        diff = self._notch_target - self._notch_pos
        if abs(diff) < 0.01:
            self._notch_pos = self._notch_target
            self._timer.stop()
        else:
            self._notch_pos += diff * step
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        track_rect = QRectF(0, 0, self.width(), self.height())
        track_color = QColor("#4A4D50") if self._dark_mode else QColor("#D3CFC7")
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(track_color)
        painter.drawRoundedRect(track_rect, self.height() / 2, self.height() / 2)

        notch_d = self.height() - 4
        travel = self.width() - notch_d - 4
        notch_x = 2 + travel * self._notch_pos
        notch_rect = QRectF(notch_x, 2, notch_d, notch_d)

        notch_color = QColor("#8A8D90") if self._dark_mode else QColor("#B0ABA1")
        painter.setBrush(notch_color)
        painter.drawEllipse(notch_rect)

        painter.setPen(QColor("#DCE4EE") if self._dark_mode else QColor("#5A5650"))
        font = QFont(self.font())
        font.setPixelSize(9)
        font.setBold(True)
        painter.setFont(font)
        label = "D" if self._dark_mode else "L"
        painter.drawText(notch_rect, Qt.AlignmentFlag.AlignCenter, label)


# Drag & Drop Widgets
class DropBox(QFrame):

    def __init__(self, title: str, extensions: tuple[str, ...], parent=None):
        super().__init__(parent)
        self.extensions = extensions
        self.path: str | None = None

        self._placeholder = title

        self.setObjectName("dropBox")
        self.setAcceptDrops(True)
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFixedHeight(60)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)

        self._path_label = QLabel(self._placeholder)
        self._path_label.setObjectName("dropBoxPath")
        self._path_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._path_label.setWordWrap(False)
        self._path_label.setFont(QFont("Segoe UI", 10))
        self._path_label.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)

        layout.addWidget(self._path_label, stretch=1)

    def _extract_valid_path(self, mime: QMimeData | None) -> str | None:
        if mime is None or not mime.hasUrls():
            return None
        urls = mime.urls()
        if len(urls) != 1:
            return None
        local_path = urls[0].toLocalFile()
        if not local_path or not os.path.isfile(local_path):
            return None
        if not local_path.lower().endswith(self.extensions):
            return None
        return local_path

    def dragEnterEvent(self, event: QDragEnterEvent):
        if self._extract_valid_path(event.mimeData()):
            self._set_active(True)
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        self._set_active(False)

    def dropEvent(self, event: QDropEvent):
        path = self._extract_valid_path(event.mimeData())
        self._set_active(False)
        if path:
            self.path = path
            self._set_filename_text(os.path.basename(path))
            event.acceptProposedAction()
        else:
            event.ignore()

    def clear(self):
        self.path = None
        self._path_label.setText(self._placeholder)

    def _set_filename_text(self, filename: str):
        metrics = self._path_label.fontMetrics()
        available = max(self.width() - 20, 40)
        elided = metrics.elidedText(filename, Qt.TextElideMode.ElideMiddle, available)
        self._path_label.setText(elided)

    def _set_active(self, active: bool):
        self.setObjectName("dropBoxActive" if active else "dropBox")
        style = self.style()
        if style is not None:
            style.unpolish(self)
            style.polish(self)
        self.update()


# Main Window
class MainWindow(QMainWindow):
    def __init__(self, app: QApplication):
        super().__init__()
        self._app = app
        self.setWindowTitle("WeightsUtility3")
        self.setMinimumSize(360, 256)
        self.resize(512, 420)
        self._build_ui()

    # UI construction
    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root_layout = QHBoxLayout(central)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        root_layout.addWidget(self._build_left_panel(), stretch=1)
        root_layout.addWidget(self._build_right_panel(), stretch=6)

    def _build_left_panel(self) -> QWidget:
        panel = QFrame()
        panel.setObjectName("leftPanel")

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(12, 16, 12, 16)
        layout.setSpacing(0)

        # Title
        title = QLabel("Weights Utility")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        layout.addWidget(title)

        # Credits
        credits = QLabel("By Callum Cross")
        credits.setAlignment(Qt.AlignmentFlag.AlignCenter)
        credits.setFont(QFont("Segoe UI", 10))
        credits.setStyleSheet("color: #AAAAAA; margin-bottom: 8px;")
        layout.addWidget(credits)

        # Theme toggle
        self.theme_toggle = ThemeToggle(dark_mode=True)
        self.theme_toggle.toggled.connect(self._on_theme_toggled)
        layout.addWidget(self.theme_toggle, alignment=Qt.AlignmentFlag.AlignHCenter)

        layout.addSpacing(16)

        # Toggles
        self.toggle_weight_sheet = ToggleSwitch("Weight Sheet")
        self.toggle_stickers = ToggleSwitch("Stickers")

        for tog in (self.toggle_weight_sheet, self.toggle_stickers):
            layout.addWidget(tog)
            layout.addSpacing(12)

        layout.addStretch()

        # Go Button
        self.go_button = QPushButton("Go")
        self.go_button.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        self.go_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.go_button.setFixedHeight(42)
        self.go_button.clicked.connect(self._execute)
        layout.addWidget(self.go_button)

        return panel

    def _build_right_panel(self) -> QWidget:
        outer = QFrame()
        outer.setObjectName("rightOuter")

        outer_layout = QVBoxLayout(outer)
        outer_layout.setContentsMargins(24, 24, 24, 24)

        inner = QFrame()
        inner.setObjectName("rightInner")
        inner_layout = QVBoxLayout(inner)
        inner_layout.setContentsMargins(12, 12, 12, 12)
        inner_layout.setSpacing(8)

        # Terminal Area
        self.terminal = QLabel()
        self.terminal.setObjectName("terminal")
        self.terminal.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.terminal.setWordWrap(True)
        self.terminal.setFont(QFont("Consolas", 10))
        self.terminal.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        inner_layout.addWidget(self.terminal, stretch=1)

        # Drag & Drop
        drop_row = QHBoxLayout()
        drop_row.setSpacing(8)

        self.excel_drop = DropBox(".xls", (".xls", ".xlsx"))
        self.pdf_drop = DropBox(".pdf", (".pdf",))

        drop_row.addWidget(self.excel_drop)
        drop_row.addWidget(self.pdf_drop)
        inner_layout.addLayout(drop_row)

        outer_layout.addWidget(inner)
        return outer

    # Theme handling
    def _on_theme_toggled(self, is_dark: bool):
        self._app.setStyleSheet(DARK_STYLESHEET if is_dark else LIGHT_STYLESHEET)

    # Path and execution logic
    def _log(self, message: str):
        current = self.terminal.text()
        self.terminal.setText((current + "\n" + message).strip())

    def _execute(self):
        self.terminal.setText("")
        self.go_button.setEnabled(False)
        QApplication.processEvents()

        try:
            self._log(f"Working dir: {os.getcwd()}")
            QApplication.processEvents()

            if self.toggle_weight_sheet.isChecked():
                if self.excel_drop.path:
                    self._log(f"Entering modify_excel… (source: {self.excel_drop.path})")
                else:
                    self._log("Entering modify_excel… (source: Downloads, default)")
                QApplication.processEvents()
                modify_excel(path=self.excel_drop.path)
                self._log("Spreadsheet done.")
                QApplication.processEvents()

            if self.toggle_stickers.isChecked():
                if self.pdf_drop.path:
                    self._log(f"Entering modify_pdf… (source: {self.pdf_drop.path})")
                else:
                    self._log("Entering modify_pdf… (source: Downloads, default)")
                QApplication.processEvents()
                modify_pdf(path=self.pdf_drop.path)
                self._log("Stickers done.")
                QApplication.processEvents()

        except Exception as e:  # noqa: BLE001
            self._log(f"ERROR: {type(e).__name__}: {e}")

        finally:
            self._log("Done.")
            self.go_button.setEnabled(True)

# Entry point
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet(DARK_STYLESHEET)
    app.setDesktopFileName("WeightsUtility3")
    app.setWindowIcon(QIcon(resource_path("weightsutility3.png")))
    window = MainWindow(app)
    window.show()
    sys.exit(app.exec())
