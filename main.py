# -*- coding: utf-8 -*-
import sys
from PySide6 import QtCore, QtGui, QtWidgets
import numpy as np
from collections import deque

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
        # *** SỬA LOGIC CLICK ĐỂ CHÍNH XÁC HƠN ***
        if self.imgLabel.underMouse():
            # Tính toán vị trí click tương đối bên trong imgLabel
            pos_global = event.globalPos()
            pos_widget = self.imgLabel.mapFromGlobal(pos_global)
            
            # Chỉ emit nếu click nằm trong phạm vi của imgLabel
            if self.imgLabel.rect().contains(pos_widget):
                self.clicked.emit(pos_widget)
        super().mousePressEvent(event)

    clicked = QtCore.Signal(QtCore.QPoint)


class LeftSidebar(QtWidgets.QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("LeftSidebar")
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        # *** CẬP NHẬT STYLESHEET ***
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

            QComboBox, QSpinBox, QLineEdit, QDoubleSpinBox, QListWidget {
                height: 36px;
                background: #fff;
                color: #111;
                border: 1px solid #cfcfcf;
                border-radius: 10px;
                padding-left: 12px;
            }
            QComboBox:hover, QSpinBox:hover, QLineEdit:hover, QDoubleSpinBox:hover, QListWidget:hover { 
                border-color: #000; 
            }
            
            /* === QListWidget (cho danh sách điểm mầm) === */
            QListWidget {
                height: 120px; /* Chiều cao cố định */
                padding: 5px;
            }
            QListWidget::item { 
                padding: 5px 8px; 
                border-radius: 5px;
            }
            QListWidget::item:selected { 
                background: #000; 
                color: #fff; 
            }
            
            /* === Nút Xoá Điểm mầm === */
            QPushButton#btnClearSeeds {
                background: #f7f7f7;
                color: #c92a2a;
                border: 1px solid #eee;
                border-radius: 10px;
                height: 36px;
                font-weight: 700;
            }
            QPushButton#btnClearSeeds:hover { background: #f0f0f0; border-color: #ddd; }


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

            QSpinBox, QDoubleSpinBox {
                padding-right: 30px;
            }
            QSpinBox::up-button, QSpinBox::down-button,
            QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {
                subcontrol-origin: border;
                subcontrol-position: top right;
                width: 26px;
                border-left: 1px solid #dcdcdc;
                background: #f5f5f5;
            }
            QSpinBox::up-button, QDoubleSpinBox::up-button {
                border-top-right-radius: 10px;
                height: 18px;
            }
            QSpinBox::down-button, QDoubleSpinBox::down-button {
                border-bottom-right-radius: 10px;
                height: 18px;
                subcontrol-position: bottom right;
            }
            QSpinBox::up-button:hover, QSpinBox::down-button:hover,
            QDoubleSpinBox::up-button:hover, QDoubleSpinBox::down-button:hover { 
                background: #eaeaea; 
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

        # Upload ảnh
        self.btnUpload = QtWidgets.QPushButton("Upload ảnh")
        self.btnUpload.setObjectName("btnUpload")
        self.btnUpload.setCursor(QtCore.Qt.PointingHandCursor)
        layout.addWidget(self.btnUpload)

        # Ngưỡng (Basic)
        self.basicTLabel = self._label("Ngưỡng (Threshold)")
        layout.addWidget(self.basicTLabel)
        self.spnThresh = QtWidgets.QSpinBox()
        self.spnThresh.setRange(0, 255)
        self.spnThresh.setValue(10)
        layout.addWidget(self.spnThresh)

        # Hệ số k (Statistical)
        self.statKLabel = self._label("Hệ số k (của σ)")
        layout.addWidget(self.statKLabel)
        self.spnStatK = QtWidgets.QDoubleSpinBox()
        self.spnStatK.setRange(0.1, 10.0)
        self.spnStatK.setValue(2.0)
        self.spnStatK.setSingleStep(0.1)
        self.spnStatK.setDecimals(1)
        layout.addWidget(self.spnStatK)

        # Loại lân cận
        layout.addWidget(self._label("Loại lân cận"))
        self.cardNeighbor = self._card_with_radios(
            ["Loại lân cận 4 (N4)", "Loại lân cận 8 (N8)"], default_index=0)
        layout.addWidget(self.cardNeighbor)

        # Loại thuật toán
        layout.addWidget(self._label("Loại thuật toán"))
        self.cardAlgo = self._card_with_radios(
            ["Nở vùng cơ bản (1 điểm mầm)", "Nở vùng thống kê (nhiều điểm)"], default_index=0)
        layout.addWidget(self.cardAlgo)

        # Gợi ý
        note = QtWidgets.QLabel("Hãy click vào ảnh để chọn điểm mầm")
        note.setProperty("class", "note")
        layout.addWidget(note)

        # *** THAY ĐỔI: Chuyển sang QListWidget ***
        layout.addWidget(self._label("Các điểm mầm:"))
        self.lstSeed = QtWidgets.QListWidget()
        self.lstSeed.setFixedHeight(120)
        layout.addWidget(self.lstSeed)

        # *** THÊM MỚI: Nút Xoá Điểm mầm ***
        self.btnClearSeeds = QtWidgets.QPushButton("Xoá các điểm mầm")
        self.btnClearSeeds.setObjectName("btnClearSeeds")
        self.btnClearSeeds.setCursor(QtCore.Qt.PointingHandCursor)
        layout.addWidget(self.btnClearSeeds)

        layout.addStretch()

        # Bắt đầu
        self.btnStart = QtWidgets.QPushButton("Bắt đầu")
        self.btnStart.setCursor(QtCore.Qt.PointingHandCursor)
        self.btnStart.setProperty("class", "primary")
        layout.addWidget(self.btnStart)

        # Kết nối sự kiện thay đổi thuật toán
        self.cardAlgo.button_group.idClicked.connect(self.toggle_algo_params)
        self.toggle_algo_params(0)  # Khởi tạo trạng thái ban đầu

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

    @QtCore.Slot(int)
    def toggle_algo_params(self, algo_id: int):
        """Ẩn/hiện tham số theo thuật toán được chọn"""
        is_basic = (algo_id == 0)
        
        # Thuật toán CƠ BẢN: hiện Threshold
        self.basicTLabel.setVisible(is_basic)
        self.spnThresh.setVisible(is_basic)
        
        # Thuật toán THỐNG KÊ: hiện k
        self.statKLabel.setVisible(not is_basic)
        self.spnStatK.setVisible(not is_basic)


class MainWindow(QtWidgets.QWidget):
    
    # *** THAY ĐỔI: Thêm điểm mầm vào danh sách ***
    def handle_seed_click(self, point: QtCore.QPoint):
        x, y = point.x(), point.y()
        item_text = f"{x},{y}"
        
        # Kiểm tra xem đã chọn thuật toán cơ bản và đã có 1 điểm chưa
        algo_idx = self._get_selected_index(self.left_widget.cardAlgo)
        if algo_idx == 0 and self.left_widget.lstSeed.count() > 0:
            # Nếu là thuật toán cơ bản, xoá điểm cũ, thêm điểm mới
            self.left_widget.lstSeed.clear()
            self.left_widget.lstSeed.addItem(item_text)
        else:
            # Nếu là thống kê, cho phép thêm nhiều
            self.left_widget.lstSeed.addItem(item_text)

    # *** THÊM MỚI: Hàm xoá điểm mầm ***
    def clear_seeds(self):
        self.left_widget.lstSeed.clear()

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
        scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        scroll.setFocusPolicy(QtCore.Qt.NoFocus)
        scroll.viewport().setAttribute(QtCore.Qt.WA_AcceptTouchEvents, False)

        root.addWidget(scroll, 1)
        self.left_widget.btnUpload.clicked.connect(self.upload_image)
        self.left_widget.btnStart.clicked.connect(self.run_region_growing)
        # *** THÊM MỚI: Kết nối nút Xoá ***
        self.left_widget.btnClearSeeds.clicked.connect(self.clear_seeds)


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

        # *** THÊM MỚI: Danh sách màu để tô (cho thuật toán Thống Kê) ***
        self.region_colors = [
            QtGui.QColor(255, 0, 0),    # Red
            QtGui.QColor(0, 255, 0),    # Green
            QtGui.QColor(0, 0, 255),    # Blue
            QtGui.QColor(255, 255, 0),  # Yellow
            QtGui.QColor(0, 255, 255),  # Cyan
            QtGui.QColor(255, 0, 255),  # Magenta
            QtGui.QColor(255, 128, 0),  # Orange
            QtGui.QColor(128, 0, 255),  # Purple
            QtGui.QColor(0, 128, 0),    # Dark Green
            QtGui.QColor(255, 192, 203) # Pink
        ]

    def upload_image(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Chọn ảnh", "", "Images (*.png *.jpg *.jpeg *.bmp)"
        )
        if file_path:
            pixmap = QtGui.QPixmap(file_path)
            if not pixmap.isNull():
                self.panelInput.set_image(pixmap)
                self.panelOutput.set_image(QtGui.QPixmap())
                # *** THAY ĐỔI: Xoá danh sách điểm mầm cũ ***
                self.left_widget.lstSeed.clear()

    def _get_selected_index(self, card_frame):
        try:
            return card_frame.button_group.checkedId()
        except Exception:
            return 0

    def run_region_growing(self):
        """Hàm chính - Gọi thuật toán phù hợp"""
        
        # *** THAY ĐỔI: Lấy danh sách điểm mầm từ QListWidget ***
        seed_items = []
        for i in range(self.left_widget.lstSeed.count()):
            seed_items.append(self.left_widget.lstSeed.item(i).text())

        if not seed_items:
            QtWidgets.QMessageBox.warning(self, "Thiếu điểm mầm", 
                                          "Vui lòng click vào ảnh để chọn ít nhất một điểm mầm.")
            return

        # *** THAY ĐỔI: Parse danh sách điểm mầm ***
        seeds_scaled = [] # Tọa độ trên ảnh đã scale (trong label)
        try:
            for item in seed_items:
                sx, sy = [int(s) for s in item.split(",")]
                seeds_scaled.append((sx, sy))
        except Exception:
            QtWidgets.QMessageBox.warning(self, "Sai định dạng điểm mầm", 
                                          "Đã có lỗi xảy ra khi đọc danh sách điểm mầm.")
            return

        pix = self.panelInput.imgLabel.pixmap()
        if pix is None:
            QtWidgets.QMessageBox.warning(self, "Chưa có ảnh", 
                                          "Vui lòng upload ảnh đầu vào trước.")
            return

        neighbor_idx = self._get_selected_index(self.left_widget.cardNeighbor)
        algo_idx = self._get_selected_index(self.left_widget.cardAlgo)

        # Chuyển đổi ảnh
        qimg_gray = pix.toImage().convertToFormat(QtGui.QImage.Format_Grayscale8)
        qimg_orig = pix.toImage().convertToFormat(QtGui.QImage.Format_ARGB32)
        w, h = qimg_gray.width(), qimg_gray.height()

        # *** THAY ĐỔI: Tính toán lại tọa độ TẤT CẢ điểm mầm ***
        seeds_original = [] # Tọa độ trên ảnh gốc
        label_pixmap = self.panelInput.imgLabel.pixmap()
        if not label_pixmap:
            return
            
        label_w, label_h = label_pixmap.width(), label_pixmap.height()
        label_rect = self.panelInput.imgLabel.contentsRect()

        offset_x = (label_rect.width() - label_w) // 2
        offset_y = (label_rect.height() - label_h) // 2
        
        scale_x = w / label_w
        scale_y = h / label_h

        for sx_s, sy_s in seeds_scaled:
            sx_on_scaled = sx_s - offset_x
            sy_on_scaled = sy_s - offset_y

            sx = int(sx_on_scaled * scale_x)
            sy = int(sy_on_scaled * scale_y)

            if not (0 <= sx < w and 0 <= sy < h):
                QtWidgets.QMessageBox.warning(self, "Seed ngoài vùng",
                                              f"Điểm mầm ({sx_s},{sy_s}) sau khi tính toán ra tọa độ ({sx},{sy}) "
                                              f"không nằm trong ảnh ({w}×{h}).")
                return
            seeds_original.append((sx, sy))
        
        # Chuyển ảnh sang numpy array
        img_array = np.zeros((h, w), dtype=np.uint8)
        for y in range(h):
            for x in range(w):
                img_array[y, x] = QtGui.QColor(qimg_gray.pixel(x, y)).red()

        # === BẮT ĐẦU LOGIC PHÂN NHÁNH ===
        result = QtGui.QImage(qimg_orig) # Bắt đầu với ảnh gốc
        alpha_overlay = 150
        
        if algo_idx == 0:
            # --- THUẬT TOÁN CƠ BẢN (Chỉ dùng 1 seed) ---
            
            # Chỉ lấy điểm mầm ĐẦU TIÊN
            sx, sy = seeds_original[0] 
            if len(seeds_original) > 1:
                self.left_widget.lstSeed.setCurrentRow(0)
                QtWidgets.QMessageBox.information(self, "Lưu ý",
                    "Thuật toán Cơ bản chỉ hỗ trợ 1 điểm mầm.\n"
                    f"Đang sử dụng điểm mầm đầu tiên trong danh sách.")

            thresh = self.left_widget.spnThresh.value()
            
            # Gọi hàm CƠ BẢN (bản gốc của bạn, trả về region)
            region, _, _ = self._execute_basic_growth(
                img_array, sx, sy, thresh, neighbor_idx
            )
            
            if region is None:
                QtWidgets.QMessageBox.critical(self, "Lỗi", "Không thể thực thi thuật toán cơ bản.")
                return

            # Vẽ overlay MỘT MÀU (đỏ)
            for y in range(h):
                for x in range(w):
                    if region[y, x]:
                        orig_col = QtGui.QColor(result.pixel(x, y))
                        a = alpha_overlay / 255.0
                        r = int(a * 255 + (1 - a) * orig_col.red())
                        g = int((1 - a) * orig_col.green())
                        b = int((1 - a) * orig_col.blue())
                        result.setPixelColor(x, y, QtGui.QColor(r, g, b))
        
        else:
            # --- THUẬT TOÁN THỐNG KÊ (Dùng nhiều seed) ---
            labels_array = np.zeros((h, w), dtype=np.int32)
            current_label_id = 1
            k = self.left_widget.spnStatK.value()

            # Lặp qua TẤT CẢ các điểm mầm
            for sx, sy in seeds_original:
                if labels_array[sy, sx] > 0: # Đã thuộc vùng khác
                    continue
                
                # Gọi hàm thống kê (đã được sửa đổi để nhận labels_array)
                self._execute_statistical_growth_multi(
                    img_array, sx, sy, labels_array, current_label_id, k, neighbor_idx
                )
                current_label_id += 1
            
            # Vẽ overlay NHIỀU MÀU
            for y in range(h):
                for x in range(w):
                    label_id = labels_array[y, x]
                    if label_id > 0:
                        # Lấy màu dựa trên ID của vùng
                        color_index = (label_id - 1) % len(self.region_colors)
                        color = self.region_colors[color_index]
                        
                        orig_col = QtGui.QColor(result.pixel(x, y))
                        a = alpha_overlay / 255.0
                        r = int(a * color.red() + (1 - a) * orig_col.red())
                        g = int(a * color.green() + (1 - a) * orig_col.green())
                        b = int(a * color.blue() + (1 - a) * orig_col.blue())
                        result.setPixelColor(x, y, QtGui.QColor(r, g, b))

        # --- Hiển thị kết quả cuối cùng ---
        out_pix = QtGui.QPixmap.fromImage(result)
        self.panelOutput.set_image(out_pix)
        
        # (Không cần dòng này nữa)
        # algo_name = "Cơ bản" if algo_idx == 0 else "Thống kê"

    def _execute_basic_growth(self, img_array, sx, sy, thresh, neighbor_idx):
        """
        Thuật toán nở vùng CƠ BẢN (Giữ nguyên bản gốc)
        - So sánh với giá trị SEED GỐC
        - Trả về 'region' (boolean array)
        """
        h, w = img_array.shape
        visited = np.zeros((h, w), dtype=bool)
        region = np.zeros((h, w), dtype=bool)

        if neighbor_idx == 0:
            neighbors = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # N4
        else:
            neighbors = [(1, 0), (-1, 0), (0, 1), (0, -1), 
                         (1, 1), (-1, 1), (1, -1), (-1, -1)]  # N8

        queue = deque([(sx, sy)])
        visited[sy, sx] = True
        region[sy, sx] = True
        region_count = 1
        seed_value = int(img_array[sy, sx])

        while queue:
            x, y = queue.popleft()

            for dx, dy in neighbors:
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h and not visited[ny, nx]:
                    visited[ny, nx] = True
                    neighbor_val = int(img_array[ny, nx])

                    # So sánh với SEED GỐC
                    if abs(neighbor_val - seed_value) <= thresh:
                        region[ny, nx] = True
                        region_count += 1
                        queue.append((nx, ny))

        return region, seed_value, region_count

    # *** THAY ĐỔI: Sửa đổi hàm Thống kê để nhận 'labels_array' ***
    def _execute_statistical_growth_multi(self, img_array, sx, sy, labels_array, label_id, k_mult, neighbor_idx):
        """
        Thuật toán nở vùng THỐNG KÊ (Bản đa điểm mầm)
        - Sửa đổi 'labels_array' tại chỗ với 'label_id'
        - Không trả về 'region'
        """
        h, w = img_array.shape
        
        # Bỏ qua nếu điểm mầm này đã thuộc vùng khác
        if labels_array[sy, sx] > 0:
            return 0

        if neighbor_idx == 0:
            neighbors = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # N4
        else:
            neighbors = [(1, 0), (-1, 0), (0, 1), (0, -1), 
                         (1, 1), (-1, 1), (1, -1), (-1, -1)]  # N8

        queue = deque([(sx, sy)])
        labels_array[sy, sx] = label_id # Đánh dấu seed thuộc vùng này

        seed_value = int(img_array[sy, sx])
        region_sum = float(seed_value)
        region_sum_sq = float(seed_value ** 2)
        region_count = 1

        # Tham số điều khiển
        min_std_dev = 3.0  # Std tối thiểu để tránh threshold quá nhỏ
        max_region_size = (h * w) // 2  # Không quá 50% ảnh
        max_std_dev = 50.0  # Dừng nếu vùng quá không đồng nhất

        while queue and region_count < max_region_size:
            x, y = queue.popleft()

            # Tính thống kê động của vùng hiện tại
            mean = region_sum / region_count
            variance = (region_sum_sq / region_count) - (mean ** 2)
            std_dev = np.sqrt(max(0, variance))

            # Điều kiện dừng: Vùng quá không đồng nhất
            if std_dev > max_std_dev:
                continue # Dừng mở rộng từ pixel này, nhưng tiếp tục các pixel khác trong queue

            # Sử dụng std_dev tối thiểu
            effective_std_dev = max(min_std_dev, std_dev)
            
            # Ngưỡng động: k × σ
            threshold = k_mult * effective_std_dev

            for dx, dy in neighbors:
                nx, ny = x + dx, y + dy
                
                # Điều kiện: Trong ảnh VÀ chưa được gán nhãn (labels_array == 0)
                if 0 <= nx < w and 0 <= ny < h and labels_array[ny, nx] == 0:
                    neighbor_val = int(img_array[ny, nx])

                    # So sánh với TRUNG BÌNH vùng
                    if abs(neighbor_val - mean) <= threshold:
                        labels_array[ny, nx] = label_id # Gán nhãn vùng
                        queue.append((nx, ny))
                        
                        # Cập nhật thống kê tích lũy
                        region_sum += neighbor_val
                        region_sum_sq += (neighbor_val ** 2)
                        region_count += 1
                    else:
                        # Đánh dấu là đã thăm nhưng không thuộc (nhãn âm)
                        # để không xét lại.
                        labels_array[ny, nx] = -1

        # Hàm này sửa labels_array tại chỗ, không cần trả về
        return region_count


def main():
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("Region Growing UI - PySide6")
    w = MainWindow()
    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()