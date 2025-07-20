import os
import json
import random
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QPushButton, QFrame, QButtonGroup, QSpacerItem, QSizePolicy,
    QFileDialog, QStackedWidget
)
from PyQt6.QtCore import Qt, QSize, QTimer
from PyQt6.QtGui import QFont, QPixmap, QIcon

class QuizApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quiz Game")
        self.setMinimumSize(QSize(800, 500))
        self.bg_color = "#DCE1DE"
        self.fg_color = "#A1A5A3"
        self.text_color = "#2F2F2F"
        self.test_data = []
        self.current_question = 0
        self.score = 0
        self.test_path = ""
        
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        self.init_folder_ui()
        self.init_quiz_ui()

    def init_folder_ui(self):
        folder_widget = QWidget()
        folder_widget.setStyleSheet(f"background-color: {self.bg_color};")
        layout = QVBoxLayout(folder_widget)
        
        title = QLabel("Quiz Game")
        title.setStyleSheet(f"font-size: 24px; color: {self.text_color};")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        self.folder_btn = QPushButton("Select Test Folder")
        self.folder_btn.setStyleSheet(f"""
            background-color: {self.fg_color};
            color: {self.text_color};
            border-radius: 24px;
            padding: 15px;
            font-size: 16px;
        """)
        self.folder_btn.clicked.connect(self.select_folder)
        layout.addWidget(self.folder_btn)
        
        self.folder_label = QLabel("No folder selected")
        self.folder_label.setStyleSheet(f"color: {self.text_color};")
        layout.addWidget(self.folder_label)
        
        self.start_btn = QPushButton("Start Quiz")
        self.start_btn.setStyleSheet(f"""
            background-color: {self.fg_color};
            color: {self.text_color};
            border-radius: 24px;
            padding: 15px;
            font-size: 16px;
        """)
        self.start_btn.setEnabled(False)
        self.start_btn.clicked.connect(self.start_quiz)
        layout.addWidget(self.start_btn)
        
        layout.addStretch()
        self.stacked_widget.addWidget(folder_widget)

    def init_quiz_ui(self):
        quiz_widget = QWidget()
        quiz_widget.setStyleSheet(f"background-color: {self.bg_color}; padding: 20px;")
        main_layout = QHBoxLayout(quiz_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        self.left_panel = QFrame()
        self.left_panel.setStyleSheet(f"""
            background-color: {self.fg_color};
            color: {self.text_color};
            border-radius: 24px;
            padding: 20px;
        """)
        self.left_panel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.left_layout = QVBoxLayout()
        self.left_panel.setLayout(self.left_layout)
        
        self.question_label = QLabel()
        self.question_label.setWordWrap(True)
        self.question_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.question_label.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        self.left_layout.addWidget(self.question_label)
        
        self.question_image = QLabel()
        self.question_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.left_layout.addWidget(self.question_image)
        self.left_layout.addStretch()
        main_layout.addWidget(self.left_panel, 40)

        right_panel = QFrame()
        right_panel.setStyleSheet("background: transparent;")
        right_layout = QVBoxLayout()
        right_panel.setLayout(right_layout)
        right_layout.setContentsMargins(20, 20, 20, 20)
        right_layout.setSpacing(20)

        self.button_container = QWidget()
        self.button_container.setStyleSheet("background: transparent;")
        self.button_layout = QVBoxLayout()
        self.button_container.setLayout(self.button_layout)
        self.button_layout.setSpacing(20)
        self.button_layout.setContentsMargins(0, 0, 0, 0)
        
        right_layout.addWidget(self.button_container)
        right_layout.addStretch()

        self.score_label = QLabel(f"Score: {self.score}/{len(self.test_data)}")
        self.score_label.setStyleSheet(f"color: {self.text_color}; font-size: 16px;")
        self.score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right_layout.addWidget(self.score_label)
        
        main_layout.addWidget(right_panel, 60)
        self.answer_buttons = []
        self.button_group = QButtonGroup()
        self.stacked_widget.addWidget(quiz_widget)

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Test Folder")
        if folder:
            self.test_path = folder
            self.folder_label.setText(f"Selected: {os.path.basename(folder)}")
            if os.path.exists(os.path.join(folder, "test.json")):
                self.start_btn.setEnabled(True)
            else:
                self.start_btn.setEnabled(False)
                self.folder_label.setText("Error: No test.json found")

    def start_quiz(self):
        with open(os.path.join(self.test_path, "test.json"), "r") as f:
            self.test_data = json.load(f)
        self.stacked_widget.setCurrentIndex(1)
        self.show_question()

    def show_question(self):
        for button in self.answer_buttons:
            button.deleteLater()
        self.answer_buttons = []
        self.button_group = QButtonGroup()
        self.question_image.clear()
        
        if self.current_question >= len(self.test_data):
            self.show_results()
            return
            
        question = self.test_data[self.current_question]
        self.question_label.setText(question["question"])

        if question["question_image"]:
            img_path = os.path.join(self.test_path, "imgs", question["question_image"])
            if os.path.exists(img_path):
                pixmap = QPixmap(img_path)
                self.question_image.setPixmap(pixmap.scaled(300, 300, Qt.AspectRatioMode.KeepAspectRatio))

        answers = list(zip(question["answers"].items(), question["answers_images"]))
        random.shuffle(answers)
        self.correct_answer = None

        for i, ((answer, is_correct), img_name) in enumerate(answers):
            button = QPushButton(answer)
            button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {self.fg_color};
                    color: {self.text_color};
                    border-radius: 24px;
                    padding: 20px;
                    font-size: 14px;
                    text-align: left;
                    border: none;
                    min-height: 60px;
                }}
                QPushButton:hover {{
                    background-color: #B8BCBA;
                }}
            """)
            
            if img_name:
                img_path = os.path.join(self.test_path, "imgs", img_name)
                if os.path.exists(img_path):
                    icon = QPixmap(img_path).scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatio)
                    button.setIcon(QIcon(icon))
                    button.setIconSize(QSize(40, 40))

            button.clicked.connect(lambda _, a=answer: self.check_answer(a))
            self.answer_buttons.append(button)
            self.button_group.addButton(button, i)
            self.button_layout.addWidget(button)
            
            if is_correct:
                self.correct_answer = answer

        self.button_layout.addStretch()

    def check_answer(self, selected_answer):
        for button in self.answer_buttons:
            button.setEnabled(False)
            if button.text() == self.correct_answer:
                button.setStyleSheet(f"""
                    background-color: #8BC34A;
                    color: {self.text_color};
                    border-radius: 24px;
                    padding: 20px;
                """)
            elif button.text() == selected_answer and selected_answer != self.correct_answer:
                button.setStyleSheet(f"""
                    background-color: #FF5252;
                    color: white;
                    border-radius: 24px;
                    padding: 20px;
                """)

        if selected_answer == self.correct_answer:
            self.score += 1
            self.score_label.setText(f"Score: {self.score}/{len(self.test_data)}")

        self.current_question += 1
        if self.current_question < len(self.test_data):
            QTimer.singleShot(1500, self.show_question)
        else:
            QTimer.singleShot(1500, self.show_results)

    def show_results(self):
        percentage = (self.score / len(self.test_data)) * 100
        result_text = f"""
        <div style='text-align:center;'>
            <h2>Quiz Completed!</h2>
            <p style='font-size:18px;'>
                Your score: {self.score}/{len(self.test_data)}<br>
                ({percentage:.1f}%)
            </p>
        </div>
        """
        self.question_label.setText(result_text)
        self.question_image.clear()
        for button in self.answer_buttons:
            button.deleteLater()
        self.answer_buttons = []

if __name__ == "__main__":
    app = QApplication([])
    window = QuizApp()
    window.show()
    app.exec()