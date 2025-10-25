# -*- coding: utf-8 -*-
import sys
from PySide6 import QtCore, QtGui, QtWidgets

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
        # Lấy kích thước khung
        target_size = self.imgLabel.size()

        # Scale giữ tỉ lệ ảnh, không méo
        scaled_pixmap = qpixmap.scaled(
            target_size,
            QtCore.Qt.KeepAspectRatio,
            QtCore.Qt.SmoothTransformation
        )
        self.imgLabel.setPixmap(scaled_pixmap)


class LeftSidebar(QtWidgets.QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("LeftSidebar")
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.setStyleSheet("""
            /* --- reset --- */
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

            /* Upload */
            QPushButton#btnUpload {
                background: #d9d9d9;
                color: #111;
                border-radius: 14px;
                height: 56px;
                font-weight: 800;
            }
            QPushButton#btnUpload:hover { background: #cfcfcf; }

            /* ===== Input base ===== */
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

            /* ===== QComboBox – hiện đại ===== */
            QComboBox {
                padding: 0 38px 0 12px;                /* chừa chỗ mũi tên */
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
            /* Tam giác mũi tên */
            QComboBox::down-arrow {
                image: url(arrow-down-angle.svg);
                width: 12px;
                height: 12px;
                margin-right: 6px;
            }

            /* Danh sách thả xuống */
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

            /* ===== QSpinBox – hiện đại ===== */
            QSpinBox {
                padding-right: 30px;                   /* chừa chỗ nút up/down */
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
            /* ===== Radio rõ ràng ===== */
            QGroupBox { border: none; background: transparent; }
            QRadioButton, QCheckBox { color: #111; font-size: 14px; spacing: 6px; }
            QRadioButton::indicator {
                width: 16px; height: 16px;
                border: 2px solid #444; border-radius: 8px;
                background: #fff; margin-right: 8px;
            }
            QRadioButton::indicator:checked { background: #000; border-color: #000; }
            QRadioButton::indicator:disabled { background: #eee; border-color: #ccc; }

            /* Button chính */
            QPushButton.primary {
                background: #000; color: #fff;
                border-radius: 16px; height: 56px;
                font-weight: 900; font-size: 18px;
            }
        """)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(16)

        # Upload ảnh
        self.btnUpload = QtWidgets.QPushButton("Upload ảnh")
        self.btnUpload.setObjectName("btnUpload")
        self.btnUpload.setCursor(QtCore.Qt.PointingHandCursor)
        layout.addWidget(self.btnUpload)

        # Kích thước lọc
        layout.addWidget(self._label("Kích thước lọc:"))
        self.cboKernel = QtWidgets.QComboBox()
        self.cboKernel.addItems(["3 × 3", "5 × 5", "7 × 7"])
        layout.addWidget(self.cboKernel)

        # Ngưỡng
        layout.addWidget(self._label("Ngưỡng (Threshold)"))
        self.spnThresh = QtWidgets.QSpinBox()
        self.spnThresh.setRange(0, 255)
        self.spnThresh.setValue(10)
        layout.addWidget(self.spnThresh)

        # Loại lân cận
        layout.addWidget(self._label("Loại lân cận"))
        layout.addWidget(self._card_with_radios(
            ["Loại lân cận 4 (N4)", "Loại lân cận 8 (N8)"], default_index=0))

        # Loại thuật toán
        layout.addWidget(self._label("Loại thuật toán"))
        layout.addWidget(self._card_with_radios(
            ["Nở vùng cơ bản", "Nở vùng thống kê"], default_index=0))

        # Gợi ý
        note = QtWidgets.QLabel("Hãy click vào ảnh để chọn điểm mầm")
        note.setProperty("class", "note")
        layout.addWidget(note)

        # Điểm mầm
        layout.addWidget(self._label("Điểm mầm:"))
        self.txtSeed = QtWidgets.QLineEdit()
        self.txtSeed.setPlaceholderText("211,375")
        self.txtSeed.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.txtSeed)

        layout.addStretch()

        # Bắt đầu
        self.btnStart = QtWidgets.QPushButton("Bắt đầu")
        self.btnStart.setCursor(QtCore.Qt.PointingHandCursor)
        self.btnStart.setProperty("class", "primary")
        layout.addWidget(self.btnStart)

    def _label(self, text) -> QtWidgets.QLabel:
        lab = QtWidgets.QLabel(text)
        lab.setProperty("class", "section")
        return lab

    def _card_with_radios(self, items, default_index=0) -> QtWidgets.QFrame:
        """Tạo thẻ trắng chứa các radio, viền nhẹ để dễ nhìn."""
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

        card.button_group = group  # giữ tham chiếu
        return card

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Thuật toán nở vùng")
        self.resize(1400, 820)
        self.setMinimumHeight(820)  # để không bị cụt menu khi cửa sổ nhỏ quá
        self.setStyleSheet("""
            QWidget { background: #f4f4f4; font-family: 'Inter', 'Segoe UI', Arial; font-size: 15px; }
        """)

        # ==== Tổng layout: ngang (menu trái + nội dung phải) ====
        root = QtWidgets.QHBoxLayout(self)
        root.setContentsMargins(24, 16, 24, 16)
        root.setSpacing(18)

        # ==== Menu bên trái (1/3 chiều rộng) ====
        # Gán thành self để dùng được ở các hàm khác (ví dụ: upload_image)
        self.left_widget = LeftSidebar()
        self.left_widget.setMinimumWidth(340)
        self.left_widget.setMaximumWidth(400)
        self.left_widget.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)

        # Scroll chứa self.left_widget
        scroll = QtWidgets.QScrollArea()
        scroll.setWidget(self.left_widget)  # Cập nhật ở đây
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QtWidgets.QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        scroll.setFocusPolicy(QtCore.Qt.NoFocus)
        scroll.viewport().setAttribute(QtCore.Qt.WA_AcceptTouchEvents, False)

        # Thêm vào layout chính
        root.addWidget(scroll, 1)
        # Kết nối nút upload với hàm xử lý
        self.left_widget.btnUpload.clicked.connect(self.upload_image)

        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QtWidgets.QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        scroll.setFocusPolicy(QtCore.Qt.NoFocus)  # không nhận wheel-focus
        scroll.viewport().setAttribute(QtCore.Qt.WA_AcceptTouchEvents, False)

        root.addWidget(scroll, 1)  # tỉ lệ 1 phần

        # ==== Khu vực nội dung chính (2/3 chiều rộng) ====
        main_area = QtWidgets.QFrame()
        main_area.setStyleSheet("QFrame { background: #f4f4f4; border: none; }")
        main_area.setAttribute(QtCore.Qt.WA_StyledBackground, True)

        main_layout = QtWidgets.QVBoxLayout(main_area)
        main_layout.setSpacing(18)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # --- Nhóm tiêu đề + 2 khung ảnh ---
        group_frame = QtWidgets.QFrame()
        group_frame.setStyleSheet("QFrame { background: transparent; border: none; }")
        group_layout = QtWidgets.QVBoxLayout(group_frame)
        group_layout.setContentsMargins(0, 0, 0, 0)
        group_layout.setSpacing(18)

        # ======= Thanh tiêu đề lớn =======
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

        # ======= Hai khung ảnh (Ảnh gốc – Kết quả) =======
        imgs_frame = QtWidgets.QFrame()
        imgs_frame.setStyleSheet("QFrame { background: transparent; border: none; }")
        imgs_layout = QtWidgets.QHBoxLayout(imgs_frame)
        imgs_layout.setContentsMargins(0, 0, 0, 0)
        imgs_layout.setSpacing(18)

        self.panelInput = HeaderPanel("Ảnh gốc")
        self.panelOutput = HeaderPanel("Kết quả")
        imgs_layout.addWidget(self.panelInput, 1)
        imgs_layout.addWidget(self.panelOutput, 1)

        group_layout.addWidget(imgs_frame, 1)
        main_layout.addWidget(group_frame, 1)

        root.addWidget(main_area, 2)  # tỉ lệ 2 phần (2/3)

        # === Label "Nhóm 04" ở góc trái trên cùng (giữ nguyên nếu bạn đang dùng) ===
        topLeft = QtWidgets.QLabel("Nhóm 04")
        topLeft.setStyleSheet("QLabel { font-weight: 900; font-size: 20px; }")
        # (nếu bạn muốn đặt chồng góc trái, cần dùng layout overlay riêng; còn không, có thể bỏ)
    # hàm upload
    def upload_image(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Chọn ảnh", "", "Images (*.png *.jpg *.jpeg *.bmp)"
        )
        if file_path:
            pixmap = QtGui.QPixmap(file_path)
            if not pixmap.isNull():
                self.panelInput.set_image(pixmap)


def main():
    # (Qt6 vẫn hỗ trợ đặt thuộc tính DPI; có thể bỏ nếu không cần)
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("Region Growing UI - PySide6")
    w = MainWindow()
    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()