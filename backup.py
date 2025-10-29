# -*- coding: utf-8 -*-
import sys
from PySide6 import QtCore, QtGui, QtWidgets
import numpy as np

APP_BG = "#f4f4f4"
PANEL_BG = "#e0e0e0"
HEADER_BG = "#111111"
HEADER_FG = "#ffffff"
PINK = "#ffffff"


class HeaderPanel(QtWidgets.QFrame):
    def __init__(self, title: str, parent=None):
        super().__init__(parent)
        self.setObjectName("HeaderPanel")
        self.setStyleSheet(f"""
            QFrame#HeaderPanel {{ background: {PANEL_BG}; border-radius: 18px; }}
        """)
        outer = QtWidgets.QVBoxLayout(self)
        outer.setContentsMargins(20, 18, 20, 18)
        outer.setSpacing(14)

        # === Header ===
        header = QtWidgets.QFrame()
        header.setObjectName("HeaderBar")
        header.setFixedHeight(46)
        header.setStyleSheet(f"QFrame#HeaderBar {{ background: {HEADER_BG}; border-radius: 12px; }}")
        h = QtWidgets.QHBoxLayout(header)
        h.setContentsMargins(16, 6, 16, 6)
        lbl = QtWidgets.QLabel(title)
        lbl.setStyleSheet("color:#fff; font-weight:800; font-size:18px; letter-spacing:0.5px;")
        h.addWidget(lbl)
        h.addStretch()

        # === Ảnh hiển thị ===
        self.imgLabel = QtWidgets.QLabel()
        self.imgLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.imgLabel.setStyleSheet(f"background: {PINK}; border-radius: 10px;")
        self.imgLabel.setMinimumSize(500, 430)

        outer.addWidget(header)
        outer.addWidget(self.imgLabel, 1)

    def set_image(self, qpixmap: QtGui.QPixmap):
        target_size = self.imgLabel.size()
        scaled_pixmap = qpixmap.scaled(
            target_size,
            QtCore.Qt.KeepAspectRatio,
            QtCore.Qt.SmoothTransformation
        )
        self.imgLabel.setPixmap(scaled_pixmap)

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        if self.imgLabel.underMouse():
            pos = event.pos() - self.imgLabel.pos()
            self.clicked.emit(pos)
        super().mousePressEvent(event)

    clicked = QtCore.Signal(QtCore.QPoint)


class LeftSidebar(QtWidgets.QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("LeftSidebar")
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.setStyleSheet("""
            QLabel, QRadioButton, QCheckBox { background: transparent; }

            QFrame#LeftSidebar {
                background: #ffffff;
                border-radius: 18px;
            }

            QLabel.section {
                color: #111;
                font-weight: 800;
                font-size: 15px;
                margin: 6px 0;
            }
            QLabel.note { color: #444; font-size: 12px; }

            QPushButton#btnUpload {
                background: #d9d9d9;
                color: #111;
                border-radius: 14px;
                height: 56px;
                font-weight: 800;
            }
            QPushButton#btnUpload:hover { background: #cfcfcf; }

            QComboBox, QSpinBox, QLineEdit {
                height: 36px;
                background: #fff;
                color: #111;
                border: 1px solid #cfcfcf;
                border-radius: 10px;
            }
            QComboBox:hover, QSpinBox:hover, QLineEdit:hover { border-color: #000; }
            QLineEdit { padding: 0 12px; }
            QLineEdit::placeholder { color: #999; }

            QComboBox {
                padding: 0 38px 0 12px;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 30px;
                border-left: 1px solid #dcdcdc;
                border-top-right-radius: 10px;
                border-bottom-right-radius: 10px;
                background: #f5f5f5;
            }
            QComboBox::drop-down:hover { background: #eaeaea; }
            QComboBox::down-arrow {
                image: url(arrow-down-angle.svg);
                width: 12px;
                height: 12px;
                margin-right: 6px;
            }

            QComboBox QAbstractItemView {
                background: #fff;
                color: #111;
                border: 1px solid #cfcfcf;
                selection-background-color: #000;
                selection-color: #fff;
                outline: 0;
                border-radius: 8px;
            }
            QComboBox QAbstractItemView::item {
                height: 28px; padding: 4px 10px;
            }

            QSpinBox {
                padding-right: 30px;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                subcontrol-origin: border;
                subcontrol-position: top right;
                width: 26px;
                border-left: 1px solid #dcdcdc;
                background: #f5f5f5;
            }
            QSpinBox::up-button {
                border-top-right-radius: 10px;
                height: 18px;
            }
            QSpinBox::down-button {
                border-bottom-right-radius: 10px;
                height: 18px;
                subcontrol-position: bottom right;
            }
            QSpinBox::up-button:hover, QSpinBox::down-button:hover { background: #eaeaea; }

            QSpinBox::up-arrow, QSpinBox::down-arrow {
                image: none;
                width: 0; height: 0;
                border-left: 6px solid transparent;
                border-right: 6px solid transparent;
                margin-right: 6px;
            }
            QSpinBox::up-arrow {
                image: url(arrow-angle-pointing-up.svg);
                width: 12px;
                height: 12px;
                margin-right: 6px;
            }
            QSpinBox::down-arrow {
                image: url(arrow-down-angle.svg);
                width: 12px;
                height: 12px;
                margin-right: 6px;
            }

            QGroupBox { border: none; background: transparent; }
            QRadioButton, QCheckBox { color: #111; font-size: 14px; spacing: 6px; }
            QRadioButton::indicator {
                width: 16px; height: 16px;
                border: 2px solid #444; border-radius: 8px;
                background: #fff; margin-right: 8px;
            }
            QRadioButton::indicator:checked { background: #000; border-color: #000; }
            QRadioButton::indicator:disabled { background: #eee; border-color: #ccc; }

            QPushButton.primary {
                background: #000; color: #fff;
                border-radius: 16px; height: 56px;
                font-weight: 900; font-size: 18px;
            }
        """)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(16)

        self.btnUpload = QtWidgets.QPushButton("Upload ảnh")
        self.btnUpload.setObjectName("btnUpload")
        self.btnUpload.setCursor(QtCore.Qt.PointingHandCursor)
        layout.addWidget(self.btnUpload)

        layout.addWidget(self._label("Ngưỡng (Threshold)"))
        self.spnThresh = QtWidgets.QSpinBox()
        self.spnThresh.setRange(0, 255)
        self.spnThresh.setValue(10)
        layout.addWidget(self.spnThresh)

        # Thêm tham số cho thống kê
        layout.addWidget(self._label("Hệ số std (k) - Chỉ cho thống kê"))
        self.spnStdFactor = QtWidgets.QSpinBox()
        self.spnStdFactor.setRange(1, 10)
        self.spnStdFactor.setValue(2)
        layout.addWidget(self.spnStdFactor)

        layout.addWidget(self._label("Loại lân cận"))
        self.cardNeighbor = self._card_with_radios(
            ["Loại lân cận 4 (N4)", "Loại lân cận 8 (N8)"], default_index=0)
        layout.addWidget(self.cardNeighbor)

        layout.addWidget(self._label("Loại thuật toán"))
        self.cardAlgo = self._card_with_radios(
            ["Nở vùng cơ bản", "Nở vùng thống kê"], default_index=0)
        layout.addWidget(self.cardAlgo)

        note = QtWidgets.QLabel("Hãy click vào ảnh để chọn điểm mầm")
        note.setProperty("class", "note")
        layout.addWidget(note)

        layout.addWidget(self._label("Điểm mầm:"))
        self.txtSeed = QtWidgets.QLineEdit()
        self.txtSeed.setPlaceholderText("211,375")
        self.txtSeed.setAlignment(QtCore.Qt.AlignCenter)
        self.txtSeed.setReadOnly(True)
        layout.addWidget(self.txtSeed)

        layout.addStretch()

        self.btnStart = QtWidgets.QPushButton("Bắt đầu")
        self.btnStart.setCursor(QtCore.Qt.PointingHandCursor)
        self.btnStart.setProperty("class", "primary")
        layout.addWidget(self.btnStart)

    def _label(self, text) -> QtWidgets.QLabel:
        lab = QtWidgets.QLabel(text)
        lab.setProperty("class", "section")
        return lab

    def _card_with_radios(self, items, default_index=0) -> QtWidgets.QFrame:
        card = QtWidgets.QFrame()
        card.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        card.setStyleSheet("""
            QFrame {
                background: #ffffff;
                border: 1px solid #eeeeee;
                border-radius: 10px;
            }
        """)
        lay = QtWidgets.QVBoxLayout(card)
        lay.setContentsMargins(10, 8, 10, 8)
        lay.setSpacing(6)

        group = QtWidgets.QButtonGroup(card)
        group.setExclusive(True)

        for i, text in enumerate(items):
            rb = QtWidgets.QRadioButton(text)
            rb.setChecked(i == default_index)
            lay.addWidget(rb)
            group.addButton(rb, i)

        card.button_group = group
        return card


class MainWindow(QtWidgets.QWidget):
    def handle_seed_click(self, point: QtCore.QPoint):
        x, y = point.x(), point.y()
        self.left_widget.txtSeed.setText(f"{x},{y}")

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Thuật toán nở vùng")
        self.resize(1400, 820)
        self.setMinimumHeight(820)
        self.setStyleSheet("""
            QWidget { background: #f4f4f4; font-family: 'Inter', 'Segoe UI', Arial; font-size: 15px; }
        """)

        root = QtWidgets.QHBoxLayout(self)
        root.setContentsMargins(24, 16, 24, 16)
        root.setSpacing(18)

        self.left_widget = LeftSidebar()
        self.left_widget.setMinimumWidth(340)
        self.left_widget.setMaximumWidth(400)
        self.left_widget.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)

        scroll = QtWidgets.QScrollArea()
        scroll.setWidget(self.left_widget)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QtWidgets.QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        scroll.setFocusPolicy(QtCore.Qt.NoFocus)
        scroll.viewport().setAttribute(QtCore.Qt.WA_AcceptTouchEvents, False)

        root.addWidget(scroll, 1)
        self.left_widget.btnUpload.clicked.connect(self.upload_image)
        self.left_widget.btnStart.clicked.connect(self.run_algorithm)

        main_area = QtWidgets.QFrame()
        main_area.setStyleSheet("QFrame { background: #f4f4f4; border: none; }")
        main_area.setAttribute(QtCore.Qt.WA_StyledBackground, True)

        main_layout = QtWidgets.QVBoxLayout(main_area)
        main_layout.setSpacing(18)
        main_layout.setContentsMargins(0, 0, 0, 0)

        group_frame = QtWidgets.QFrame()
        group_frame.setStyleSheet("QFrame { background: transparent; border: none; }")
        group_layout = QtWidgets.QVBoxLayout(group_frame)
        group_layout.setContentsMargins(0, 0, 0, 0)
        group_layout.setSpacing(18)

        header = QtWidgets.QFrame()
        header.setStyleSheet("""
            QFrame { background: #dadada; border-radius: 20px; }
            QLabel { font-size: 36px; font-weight: 900; letter-spacing: 1px; }
        """)
        header.setFixedHeight(76)
        hh = QtWidgets.QHBoxLayout(header)
        hh.setContentsMargins(24, 8, 24, 8)
        hh.addStretch()
        hh.addWidget(QtWidgets.QLabel("THUẬT TOÁN NỞ VÙNG"))
        hh.addStretch()
        group_layout.addWidget(header)

        imgs_frame = QtWidgets.QFrame()
        imgs_frame.setStyleSheet("QFrame { background: transparent; border: none; }")
        imgs_layout = QtWidgets.QHBoxLayout(imgs_frame)
        imgs_layout.setContentsMargins(0, 0, 0, 0)
        imgs_layout.setSpacing(18)

        self.panelInput = HeaderPanel("Ảnh gốc")
        self.panelInput.clicked.connect(self.handle_seed_click)
        self.panelOutput = HeaderPanel("Kết quả")
        imgs_layout.addWidget(self.panelInput, 1)
        imgs_layout.addWidget(self.panelOutput, 1)

        group_layout.addWidget(imgs_frame, 1)
        main_layout.addWidget(group_frame, 1)

        root.addWidget(main_area, 2)

    def upload_image(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Chọn ảnh", "", "Images (*.png *.jpg *.jpeg *.bmp)"
        )
        if file_path:
            pixmap = QtGui.QPixmap(file_path)
            if not pixmap.isNull():
                self.panelInput.set_image(pixmap)

    def _get_selected_index(self, card_frame):
        try:
            return card_frame.button_group.checkedId()
        except Exception:
            return 0

    def run_algorithm(self):
        algo_idx = self._get_selected_index(self.left_widget.cardAlgo)

        if algo_idx == 0:
            self.run_region_growing_basic()
        else:
            self.run_region_growing_statistical()

    def run_region_growing_basic(self):
        seed_text = self.left_widget.txtSeed.text().strip()
        if not seed_text:
            QtWidgets.QMessageBox.warning(self, "Thiếu điểm mầm", "Vui lòng click vào ảnh để chọn điểm mầm.")
            return
        try:
            sx, sy = [int(s) for s in seed_text.split(",")]
        except Exception:
            QtWidgets.QMessageBox.warning(self, "Sai định dạng điểm mầm", "Định dạng đúng: x,y (ví dụ: 211,375)")
            return

        pix = self.panelInput.imgLabel.pixmap()
        if pix is None:
            QtWidgets.QMessageBox.warning(self, "Chưa có ảnh", "Vui lòng upload ảnh đầu vào trước.")
            return

        thresh = self.left_widget.spnThresh.value()
        neighbor_idx = self._get_selected_index(self.left_widget.cardNeighbor)

        qimg_gray = pix.toImage().convertToFormat(QtGui.QImage.Format_Grayscale8)
        qimg_orig = pix.toImage().convertToFormat(QtGui.QImage.Format_ARGB32)
        w, h = qimg_gray.width(), qimg_gray.height()

        label_pixmap = self.panelInput.imgLabel.pixmap()
        if label_pixmap:
            label_w, label_h = label_pixmap.width(), label_pixmap.height()
            label_rect = self.panelInput.imgLabel.contentsRect()

            offset_x = (label_rect.width() - label_w) // 2
            offset_y = (label_rect.height() - label_h) // 2

            sx_on_scaled = sx - offset_x
            sy_on_scaled = sy - offset_y

            scale_x = w / label_w
            scale_y = h / label_h
            sx = int(sx_on_scaled * scale_x)
            sy = int(sy_on_scaled * scale_y)

        if not (0 <= sx < w and 0 <= sy < h):
            QtWidgets.QMessageBox.warning(self, "Seed ngoài vùng",
                                          f"Điểm mầm ({sx},{sy}) không nằm trong ảnh ({w}×{h}).\n"
                                          f"Vui lòng click vào vùng ảnh.")
            return

        img_array = np.zeros((h, w), dtype=np.uint8)
        for y in range(h):
            for x in range(w):
                img_array[y, x] = QtGui.QColor(qimg_gray.pixel(x, y)).red()

        seed_value = int(img_array[sy, sx])
        visited = np.zeros((h, w), dtype=bool)
        region = np.zeros((h, w), dtype=bool)

        from collections import deque
        queue = deque([(sx, sy)])
        visited[sy, sx] = True
        region[sy, sx] = True

        if neighbor_idx == 0:
            neighbors = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # N4
        else:
            neighbors = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]  # N8

        while queue:
            x, y = queue.popleft()

            for dx, dy in neighbors:
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h and not visited[ny, nx]:
                    visited[ny, nx] = True
                    neighbor_val = int(img_array[ny, nx])

                    if abs(neighbor_val - seed_value) <= thresh:
                        region[ny, nx] = True
                        queue.append((nx, ny))

        result = self._create_result_image(qimg_orig, region, w, h)
        self.panelOutput.set_image(result)

    def run_region_growing_statistical(self):
        seed_text = self.left_widget.txtSeed.text().strip()
        if not seed_text:
            QtWidgets.QMessageBox.warning(self, "Thiếu điểm mầm", "Vui lòng click vào ảnh để chọn điểm mầm.")
            return
        try:
            sx, sy = [int(s) for s in seed_text.split(",")]
        except Exception:
            QtWidgets.QMessageBox.warning(self, "Sai định dạng điểm mầm", "Định dạng đúng: x,y (ví dụ: 211,375)")
            return

        pix = self.panelInput.imgLabel.pixmap()
        if pix is None:
            QtWidgets.QMessageBox.warning(self, "Chưa có ảnh", "Vui lòng upload ảnh đầu vào trước.")
            return

        thresh = self.left_widget.spnThresh.value()
        k = self.left_widget.spnStdFactor.value()
        neighbor_idx = self._get_selected_index(self.left_widget.cardNeighbor)

        qimg_gray = pix.toImage().convertToFormat(QtGui.QImage.Format_Grayscale8)
        qimg_orig = pix.toImage().convertToFormat(QtGui.QImage.Format_ARGB32)
        w, h = qimg_gray.width(), qimg_gray.height()

        label_pixmap = self.panelInput.imgLabel.pixmap()
        if label_pixmap:
            label_w, label_h = label_pixmap.width(), label_pixmap.height()
            label_rect = self.panelInput.imgLabel.contentsRect()

            offset_x = (label_rect.width() - label_w) // 2
            offset_y = (label_rect.height() - label_h) // 2

            sx_on_scaled = sx - offset_x
            sy_on_scaled = sy - offset_y

            scale_x = w / label_w
            scale_y = h / label_h
            sx = int(sx_on_scaled * scale_x)
            sy = int(sy_on_scaled * scale_y)

        if not (0 <= sx < w and 0 <= sy < h):
            QtWidgets.QMessageBox.warning(self, "Seed ngoài vùng",
                                          f"Điểm mầm ({sx},{sy}) không nằm trong ảnh ({w}×{h}).")
            return

        img_array = np.zeros((h, w), dtype=np.uint8)
        for y in range(h):
            for x in range(w):
                img_array[y, x] = QtGui.QColor(qimg_gray.pixel(x, y)).red()

        visited = np.zeros((h, w), dtype=bool)
        region = np.zeros((h, w), dtype=bool)

        from collections import deque
        queue = deque([(sx, sy)])
        visited[sy, sx] = True
        region[sy, sx] = True

        region_values = [float(img_array[sy, sx])]

        if neighbor_idx == 0:
            neighbors = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        else:
            neighbors = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]

        while queue:
            x, y = queue.popleft()

            mean = np.mean(region_values)
            std = np.std(region_values) if len(region_values) > 1 else 0

            for dx, dy in neighbors:
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h and not visited[ny, nx]:
                    visited[ny, nx] = True
                    neighbor_val = float(img_array[ny, nx])

                    if abs(neighbor_val - mean) <= k * std + thresh:
                        region[ny, nx] = True
                        region_values.append(neighbor_val)
                        queue.append((nx, ny))

        result = self._create_result_image(qimg_orig, region, w, h)
        self.panelOutput.set_image(result)

    def _create_result_image(self, qimg_orig, region, w, h):
        result = QtGui.QImage(qimg_orig)
        alpha_overlay = 150

        for y in range(h):
            for x in range(w):
                if region[y, x]:
                    orig_col = QtGui.QColor(result.pixel(x, y))
                    a = alpha_overlay / 255.0
                    r = int(a * 255 + (1 - a) * orig_col.red())
                    g = int((1 - a) * orig_col.green())
                    b = int((1 - a) * orig_col.blue())
                    result.setPixelColor(x, y, QtGui.QColor(r, g, b))

        return QtGui.QPixmap.fromImage(result)

def main():
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("Region Growing UI - PySide6")
    w = MainWindow()
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()