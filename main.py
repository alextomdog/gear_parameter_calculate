import sys
from PyQt5.QtWidgets import QApplication, QWidget, \
    QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, \
    QComboBox, QFrame
from PyQt5.QtCore import Qt
import math
import pyperclip


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "gear calculator"
        self.window_size = (450, 500)

        self.m = 2
        self.z = 20

        self.container = None

        self.pressure_angle = 20
        self.clearance_coefficient = 0.25
        self.addendum_modification_factor = 1

        self.label_pitch_circle_diameter_value = 0
        self.label_top_circle_diameter_value = 0
        self.label_root_circle_diameter_value = 0
        self.label_basic_circle_diameter_value = 0
        self.label_basic_circle_radius_value = 0

        self.label_function_dx_content_template = "m*z*cos(pi/9)/2*sin(t)-m*z*cos(pi/9)/2*t*cos(t)"
        self.label_function_dx_content = "m*z*cos(pi/9)/2*sin(t)-m*z*cos(pi/9)/2*t*cos(t)"
        self.label_function_dy_content_template = "m*z*cos(pi/9)/2*cos(t)+m*z*cos(pi/9)/2*t*sin(t)"
        self.label_function_dy_content = "m*z*cos(pi/9)/2*cos(t)+m*z*cos(pi/9)/2*t*sin(t)"

        self.label_center_distance_value = 0
        self.label_offset_distance_value_1 = 0
        self.label_offset_distance_value_2 = 0

        self.notification_container_list = []

        self.init_ui()
        self.handle_calculate_button_click()

    def init_ui(self):
        self.container = QVBoxLayout()  # 使用QVBoxLayout作为主布局

        row1 = QHBoxLayout()

        label_m = QLabel("输入模数:")
        row1.addWidget(label_m)
        input_m = QLineEdit()

        def set_m(text):
            self.m = text

        input_m.textChanged.connect(set_m)
        input_m.setText(str(self.m))
        row1.addWidget(input_m)
        label_gear = QLabel("输入齿数:")

        row1.addWidget(label_gear)
        input_gear = QLineEdit()

        def set_z(text):
            self.z = text

        input_gear.setText(str(self.z))
        input_gear.textChanged.connect(set_z)
        row1.addWidget(input_gear)

        calc_button = QPushButton("计算")
        calc_button.clicked.connect(self.handle_calculate_button_click)
        row1.addWidget(calc_button)

        self.container.addLayout(row1)

        # -------------------------------------------------------------------------

        row2 = QHBoxLayout()
        label_pressure_coefficient = QLabel("压力角系数")
        row2.addWidget(label_pressure_coefficient)
        combo_box_pressure_coefficient = QComboBox()
        combo_box_pressure_coefficient.addItems(["20"])
        combo_box_pressure_coefficient.activated[str].connect(
            self.handle_pressure_coefficient_combobox_changed
        )
        row2.addWidget(combo_box_pressure_coefficient)

        row2.addSpacing(10)

        label_clearance_coefficient = QLabel("顶隙系数: ")
        row2.addWidget(label_clearance_coefficient)
        combo_box_clearance_coefficient = QComboBox()
        combo_box_clearance_coefficient.addItems(["0.25"])
        combo_box_clearance_coefficient.activated[str].connect(
            self.on_combobox__clearance_coefficient_activated)
        row2.addWidget(combo_box_clearance_coefficient)

        row2.addSpacing(10)

        label_addendum_modification_factor = QLabel("齿顶高系数:")
        row2.addWidget(label_addendum_modification_factor)
        input_addendum_modification_factor = QComboBox()
        input_addendum_modification_factor.addItems(["1"])
        input_addendum_modification_factor.activated[str].connect(
            self.on_combobox__addendum_modification_factor_activated)
        row2.addWidget(input_addendum_modification_factor)

        self.container.addLayout(row2)

        self.create_separator()

        # ----------------------------------------------------------------
        self.create_line_widget("基础圆直径: ", "label_basic_circle_diameter_value")
        # self.create_line_widget("基础圆半径: ", "label_basic_circle_radius_value")
        self.create_line_widget("齿顶圆直径：", "label_top_circle_diameter_value")
        self.create_line_widget("齿根圆直径：", "label_root_circle_diameter_value")
        self.create_line_widget("分度圆直径: ", "label_pitch_circle_diameter_value")

        self.create_separator()
        self.create_functional_line("方程驱动曲线dx:", "label_function_dx_content")
        self.create_separator()
        self.create_functional_line("方程驱动曲线dy:", "label_function_dy_content")
        self.create_separator()

        self.create_line_widget("中心距离: ", "label_center_distance_value")
        self.create_line_widget("镜像角度偏移距离1:", "label_offset_distance_value_1")
        self.create_line_widget("镜像角度偏移距离2:", "label_offset_distance_value_2")

        self.setLayout(self.container)
        self.setWindowTitle(self.title)
        self.resize(*self.window_size)
        self.setFixedWidth(self.window_size[0])
        self.setFixedHeight(self.window_size[1])

    def create_line_widget(self,
                           label_value: str,
                           reference_value_label):
        current_row = QHBoxLayout()
        current_label = QLabel(label_value)
        current_row.addWidget(current_label)

        response_label = QLabel(str(getattr(self, reference_value_label)))
        current_row.addWidget(response_label)

        current_row.addStretch()

        copy_button = QPushButton("复制")
        current_row.addWidget(copy_button)

        def handler_callback():
            label_value = getattr(self, reference_value_label)
            pyperclip.copy(label_value)

        copy_button.clicked.connect(handler_callback)
        current_row.addWidget(copy_button)

        self.container.addLayout(current_row)

        def update_label(label: QLabel, reference_value_label):
            def update():
                label.setText(str(getattr(self, reference_value_label)))

            return update

        self.notification_container_list.append(
            update_label(response_label, reference_value_label))

    def create_functional_line(self, label_content, reference_value_label):
        row1 = QHBoxLayout()
        row1.addWidget(QLabel(label_content))

        def handler_callback():
            label_value = getattr(self, reference_value_label)
            pyperclip.copy(label_value)

        copy_button = QPushButton("复制")
        copy_button.clicked.connect(handler_callback)
        row1.addWidget(copy_button)

        row2 = QHBoxLayout()
        label_value = getattr(self, reference_value_label)
        response_label = QLabel(str(label_value))
        row2.addWidget(response_label)

        self.container.addLayout(row1)
        self.container.addLayout(row2)

        def update_label(label: QLabel, reference_value_label):
            def update():
                label.setText(str(getattr(self, reference_value_label)))

            return update

        self.notification_container_list.append(
            update_label(response_label, reference_value_label))

    def create_separator(self):
        # 添加水平分隔线
        line = QFrame()
        line.setFrameShape(QFrame.HLine)  # 设置为水平线
        line.setFrameShadow(QFrame.Sunken)  # 设置分隔线的样式
        self.container.addWidget(line)

    def rounding_decimal(self, rounded_number: float, decimal_number: int = 2) -> float:
        rounded_number = round(float(rounded_number), decimal_number)
        return rounded_number

    def handle_pressure_coefficient_combobox_changed(self, text):
        self.pressure_angle = text

    def on_combobox__clearance_coefficient_activated(self, text):
        self.clearance_coefficient_coefficient = text

    def on_combobox__addendum_modification_factor_activated(self, text):
        self.addendum_modification_factor = text

    def handle_calculate_button_click(self):
        self.label_pitch_circle_diameter_value = float(self.z) * float(self.m)
        self.label_pitch_circle_diameter_value = self.rounding_decimal(
            self.label_pitch_circle_diameter_value)

        self.label_function_dy_content = self.label_function_dy_content_template.replace(
            "m", str(self.m)).replace("z", str(self.z)).replace("9", str(self.rounding_decimal(180 / float(self.pressure_angle), 1)))
        self.label_function_dx_content = self.label_function_dx_content_template.replace(
            "m", str(self.m)).replace("z", str(self.z)).replace("9", str(self.rounding_decimal(180 / float(self.pressure_angle), 1)))

        self.label_top_circle_diameter_value = float(
            (float(self.z) + 2 * float(self.addendum_modification_factor)) * (float(self.m)))
        self.label_top_circle_diameter_value = self.rounding_decimal(
            self.label_top_circle_diameter_value
        )

        self.label_root_circle_diameter_value = float(
            (float(self.z) - 2 * float(self.addendum_modification_factor) -
             2*float(self.clearance_coefficient)) * float(self.m)
        )
        self.label_root_circle_diameter_value = self.rounding_decimal(
            self.label_root_circle_diameter_value
        )

        self.label_basic_circle_diameter_value = float(
            self.m) * float(self.z) * math.cos(math.pi / float(180.0 / self.pressure_angle))
        self.label_basic_circle_diameter_value = self.rounding_decimal(
            self.label_basic_circle_diameter_value
        )

        self.label_basic_circle_radius_value = self.label_basic_circle_diameter_value / 2
        self.label_basic_circle_radius_value = self.rounding_decimal(
            self.label_basic_circle_radius_value
        )

        self.label_center_distance_value = float(self.m) * float(self.z) / 2
        self.label_center_distance_value = self.rounding_decimal(
            self.label_center_distance_value)

        self.label_offset_distance_value_1 = 360 / float(self.z) / 4
        self.label_offset_distance_value_1 = self.rounding_decimal(
            self.label_offset_distance_value_1
        )
        self.label_offset_distance_value_2 = 360 / float(self.z) / 4 * 3
        self.label_offset_distance_value_2 = self.rounding_decimal(
            self.label_offset_distance_value_2
        )

        for notification_callback in self.notification_container_list:
            notification_callback()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.setWindowFlags(
        main_window.windowFlags() | Qt.WindowStaysOnTopHint)
    main_window.show()
    sys.exit(app.exec_())
