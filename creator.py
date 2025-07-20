import os
import json
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QListWidget, QRadioButton,
    QFileDialog, QGroupBox, QListWidgetItem, QMessageBox
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QIcon

class TestCreatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test Creator")
        self.setMinimumSize(800, 600)
        
        # Current test data
        self.test_data = []
        self.current_question = None
        self.test_folder = None
        
        # Setup UI
        self.init_ui()
        
    def init_ui(self):
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)
        
        # Left panel - Questions list
        left_panel = QWidget()
        left_panel.setMinimumWidth(200)
        left_layout = QVBoxLayout(left_panel)
        
        self.questions_list = QListWidget()
        self.questions_list.itemSelectionChanged.connect(self.select_question)
        left_layout.addWidget(QLabel("Questions:"))
        left_layout.addWidget(self.questions_list)
        
        # Question buttons
        btn_layout = QHBoxLayout()
        self.add_question_btn = QPushButton("Add Question")
        self.add_question_btn.clicked.connect(self.add_question)
        btn_layout.addWidget(self.add_question_btn)
        
        self.remove_question_btn = QPushButton("Remove")
        self.remove_question_btn.clicked.connect(self.remove_question)
        btn_layout.addWidget(self.remove_question_btn)
        left_layout.addLayout(btn_layout)
        
        # Test actions
        test_btn_layout = QVBoxLayout()
        self.new_test_btn = QPushButton("New Test")
        self.new_test_btn.clicked.connect(self.new_test)
        test_btn_layout.addWidget(self.new_test_btn)
        
        self.load_test_btn = QPushButton("Load Test")
        self.load_test_btn.clicked.connect(self.load_test)
        test_btn_layout.addWidget(self.load_test_btn)
        
        self.save_test_btn = QPushButton("Save Test")
        self.save_test_btn.clicked.connect(self.save_test)
        test_btn_layout.addWidget(self.save_test_btn)
        left_layout.addLayout(test_btn_layout)
        
        left_layout.addStretch()
        main_layout.addWidget(left_panel)
        
        # Right panel - Question editor
        self.right_panel = QWidget()
        self.right_panel.setEnabled(False)
        right_layout = QVBoxLayout(self.right_panel)
        
        # Question text
        question_group = QGroupBox("Question")
        q_layout = QVBoxLayout(question_group)
        
        self.question_text = QLineEdit()
        self.question_text.setPlaceholderText("Enter your question here...")
        q_layout.addWidget(self.question_text)
        
        # Question image
        img_layout = QHBoxLayout()
        self.question_image_label = QLabel("No image selected")
        self.question_image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.question_image_label.setMinimumSize(200, 150)
        self.question_image_label.setStyleSheet("border: 1px dashed #999;")
        
        img_btn_layout = QVBoxLayout()
        self.set_question_img_btn = QPushButton("Set Image")
        self.set_question_img_btn.clicked.connect(lambda: self.set_image("question"))
        img_btn_layout.addWidget(self.set_question_img_btn)
        
        self.clear_question_img_btn = QPushButton("Clear")
        self.clear_question_img_btn.clicked.connect(lambda: self.clear_image("question"))
        img_btn_layout.addWidget(self.clear_question_img_btn)
        
        img_layout.addWidget(self.question_image_label)
        img_layout.addLayout(img_btn_layout)
        q_layout.addLayout(img_layout)
        
        right_layout.addWidget(question_group)
        
        # Answers section
        answers_group = QGroupBox("Answers")
        a_layout = QVBoxLayout(answers_group)
        
        # Answers list
        self.answers_list = QListWidget()
        self.answers_list.setMinimumHeight(150)
        self.answers_list.itemSelectionChanged.connect(self.select_answer)
        a_layout.addWidget(self.answers_list)
        
        # Answer buttons
        ans_btn_layout = QHBoxLayout()
        self.add_answer_btn = QPushButton("Add Answer")
        self.add_answer_btn.clicked.connect(self.add_answer)
        ans_btn_layout.addWidget(self.add_answer_btn)
        
        self.remove_answer_btn = QPushButton("Remove")
        self.remove_answer_btn.clicked.connect(self.remove_answer)
        ans_btn_layout.addWidget(self.remove_answer_btn)
        a_layout.addLayout(ans_btn_layout)
        
        # Selected answer editor
        self.answer_editor = QWidget()
        self.answer_editor.setEnabled(False)
        ans_edit_layout = QVBoxLayout(self.answer_editor)
        
        self.answer_text = QLineEdit()
        self.answer_text.setPlaceholderText("Answer text...")
        ans_edit_layout.addWidget(self.answer_text)
        
        # Answer image
        ans_img_layout = QHBoxLayout()
        self.answer_image_label = QLabel("No image")
        self.answer_image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.answer_image_label.setMinimumSize(100, 100)
        self.answer_image_label.setStyleSheet("border: 1px dashed #999;")
        
        ans_img_btn_layout = QVBoxLayout()
        self.set_answer_img_btn = QPushButton("Set Image")
        self.set_answer_img_btn.clicked.connect(lambda: self.set_image("answer"))
        ans_img_btn_layout.addWidget(self.set_answer_img_btn)
        
        self.clear_answer_img_btn = QPushButton("Clear")
        self.clear_answer_img_btn.clicked.connect(lambda: self.clear_image("answer"))
        ans_img_btn_layout.addWidget(self.clear_answer_img_btn)
        
        ans_img_layout.addWidget(self.answer_image_label)
        ans_img_layout.addLayout(ans_img_btn_layout)
        ans_edit_layout.addLayout(ans_img_layout)
        
        # Correct answer radio
        self.correct_answer_radio = QRadioButton("Correct Answer")
        ans_edit_layout.addWidget(self.correct_answer_radio)
        
        # Save answer button
        self.save_answer_btn = QPushButton("Save Answer")
        self.save_answer_btn.clicked.connect(self.save_answer)
        ans_edit_layout.addWidget(self.save_answer_btn)
        
        a_layout.addWidget(self.answer_editor)
        right_layout.addWidget(answers_group)
        
        main_layout.addWidget(self.right_panel)
        
        # Status bar
        self.statusBar().showMessage("Ready. Create a new test or load an existing one.")
    
    def new_test(self):
        self.test_data = []
        self.test_folder = None
        self.questions_list.clear()
        self.right_panel.setEnabled(False)
        self.statusBar().showMessage("New test created. Add your first question.")
    
    def load_test(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Test Folder")
        if not folder:
            return
            
        test_file = os.path.join(folder, "test.json")
        if not os.path.exists(test_file):
            QMessageBox.warning(self, "Error", "No test.json found in selected folder")
            return
            
        try:
            with open(test_file, "r") as f:
                self.test_data = json.load(f)
            self.test_folder = folder
            self.update_questions_list()
            self.right_panel.setEnabled(True)
            self.statusBar().showMessage(f"Loaded test from: {folder}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load test: {str(e)}")
    
    def save_test(self):
        if not self.test_data:
            QMessageBox.warning(self, "Error", "No test data to save")
            return
            
        if not self.test_folder:
            self.test_folder = QFileDialog.getExistingDirectory(self, "Select Test Folder")
            if not self.test_folder:
                return
                
        # Create images folder if needed
        imgs_folder = os.path.join(self.test_folder, "imgs")
        if not os.path.exists(imgs_folder):
            os.makedirs(imgs_folder)
        
        # Save test.json
        test_file = os.path.join(self.test_folder, "test.json")
        try:
            with open(test_file, "w") as f:
                json.dump(self.test_data, f, indent=2)
            self.statusBar().showMessage(f"Test saved to: {test_file}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save test: {str(e)}")
    
    def add_question(self):
        new_question = {
            "question": "New Question",
            "question_image": "",
            "answers": {},
            "answers_images": []
        }
        self.test_data.append(new_question)
        self.update_questions_list()
        self.questions_list.setCurrentRow(len(self.test_data) - 1)
        self.right_panel.setEnabled(True)
    
    def remove_question(self):
        current_row = self.questions_list.currentRow()
        if current_row >= 0:
            self.test_data.pop(current_row)
            self.update_questions_list()
            if self.test_data:
                self.questions_list.setCurrentRow(min(current_row, len(self.test_data) - 1))
            else:
                self.right_panel.setEnabled(False)
    
    def update_questions_list(self):
        self.questions_list.clear()
        for i, q in enumerate(self.test_data):
            item = QListWidgetItem(f"Q{i+1}: {q['question'][:30]}")
            item.setData(Qt.ItemDataRole.UserRole, i)
            self.questions_list.addItem(item)
    
    def select_question(self):
        if not self.questions_list.selectedItems():
            return
            
        row = self.questions_list.currentRow()
        self.current_question = self.test_data[row]
        
        # Update question editor
        self.question_text.setText(self.current_question["question"])
        
        # Load question image if exists
        if self.current_question["question_image"] and self.test_folder:
            img_path = os.path.join(self.test_folder, "imgs", self.current_question["question_image"])
            if os.path.exists(img_path):
                pixmap = QPixmap(img_path)
                self.question_image_label.setPixmap(pixmap.scaled(200, 150, Qt.AspectRatioMode.KeepAspectRatio))
                self.question_image_label.setText("")
            else:
                self.question_image_label.setText("Image missing")
                self.question_image_label.setPixmap(QPixmap())
        else:
            self.question_image_label.setText("No image selected")
            self.question_image_label.setPixmap(QPixmap())
        
        # Update answers list
        self.update_answers_list()
    
    def update_answers_list(self):
        self.answers_list.clear()
        answers = list(self.current_question["answers"].items())
        for i, (answer, correct) in enumerate(answers):
            prefix = "✓ " if correct else "  "
            item = QListWidgetItem(f"{prefix}A{i+1}: {answer}")
            item.setData(Qt.ItemDataRole.UserRole, i)
            self.answers_list.addItem(item)
    
    def add_answer(self):
        if not self.current_question:
            return
            
        # Add a new answer
        answer_text = f"Answer {len(self.current_question['answers']) + 1}"
        self.current_question["answers"][answer_text] = 0
        self.current_question["answers_images"].append("")
        self.update_answers_list()
        self.answers_list.setCurrentRow(len(self.current_question["answers"]) - 1)
    
    def remove_answer(self):
        if not self.answers_list.selectedItems():
            return
            
        row = self.answers_list.currentRow()
        answers_list = list(self.current_question["answers"].keys())
        if 0 <= row < len(answers_list):
            # Remove the answer
            answer_text = answers_list[row]
            del self.current_question["answers"][answer_text]
            self.current_question["answers_images"].pop(row)
            self.update_answers_list()
    
    def select_answer(self):
        if not self.answers_list.selectedItems():
            self.answer_editor.setEnabled(False)
            return
            
        row = self.answers_list.currentRow()
        answers_list = list(self.current_question["answers"].items())
        if 0 <= row < len(answers_list):
            self.answer_editor.setEnabled(True)
            answer_text, is_correct = answers_list[row]
            self.answer_text.setText(answer_text)
            self.correct_answer_radio.setChecked(is_correct == 1)
            
            # Load answer image if exists
            if self.current_question["answers_images"][row] and self.test_folder:
                img_path = os.path.join(self.test_folder, "imgs", self.current_question["answers_images"][row])
                if os.path.exists(img_path):
                    pixmap = QPixmap(img_path)
                    self.answer_image_label.setPixmap(pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio))
                    self.answer_image_label.setText("")
                else:
                    self.answer_image_label.setText("Image missing")
                    self.answer_image_label.setPixmap(QPixmap())
            else:
                self.answer_image_label.setText("No image")
                self.answer_image_label.setPixmap(QPixmap())
    
    def save_answer(self):
        if not self.answers_list.selectedItems():
            return
            
        row = self.answers_list.currentRow()
        answers_list = list(self.current_question["answers"].items())
        if 0 <= row < len(answers_list):
            # Get the old answer text
            old_answer_text = answers_list[row][0]
            
            # Update the answer text
            new_answer_text = self.answer_text.text().strip()
            if not new_answer_text:
                QMessageBox.warning(self, "Error", "Answer text cannot be empty")
                return
                
            # If the text changed, update the dictionary
            if old_answer_text != new_answer_text:
                # Move the value to the new key
                value = self.current_question["answers"][old_answer_text]
                del self.current_question["answers"][old_answer_text]
                self.current_question["answers"][new_answer_text] = value
            
            # Update correctness
            for i, key in enumerate(self.current_question["answers"].keys()):
                if i == row:
                    self.current_question["answers"][key] = 1 if self.correct_answer_radio.isChecked() else 0
                elif self.correct_answer_radio.isChecked():
                    # Unset other correct answers
                    self.current_question["answers"][key] = 0
            
            self.update_answers_list()
    
    def set_image(self, img_type):
        if not self.test_folder:
            QMessageBox.warning(self, "Error", "Please save the test first to set images")
            return
            
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            f"Select {img_type.capitalize()} Image",
            "", 
            "Images (*.png *.jpg *.jpeg *.bmp)"
        )
        
        if not file_path:
            return
            
        # Determine destination path
        imgs_folder = os.path.join(self.test_folder, "imgs")
        filename = os.path.basename(file_path)
        dest_path = os.path.join(imgs_folder, filename)
        
        # Copy the image
        try:
            # Create folder if needed
            if not os.path.exists(imgs_folder):
                os.makedirs(imgs_folder)
                
            # Copy the file
            with open(file_path, "rb") as src, open(dest_path, "wb") as dst:
                dst.write(src.read())
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to copy image: {str(e)}")
            return
        
        # Update the UI and data
        if img_type == "question":
            self.current_question["question_image"] = filename
            pixmap = QPixmap(dest_path)
            self.question_image_label.setPixmap(pixmap.scaled(200, 150, Qt.AspectRatioMode.KeepAspectRatio))
            self.question_image_label.setText("")
        elif img_type == "answer" and self.answers_list.selectedItems():
            row = self.answers_list.currentRow()
            self.current_question["answers_images"][row] = filename
            pixmap = QPixmap(dest_path)
            self.answer_image_label.setPixmap(pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio))
            self.answer_image_label.setText("")
    
    def clear_image(self, img_type):
        if img_type == "question":
            self.current_question["question_image"] = ""
            self.question_image_label.setText("No image selected")
            self.question_image_label.setPixmap(QPixmap())
        elif img_type == "answer" and self.answers_list.selectedItems():
            row = self.answers_list.currentRow()
            self.current_question["answers_images"][row] = ""
            self.answer_image_label.setText("No image")
            self.answer_image_label.setPixmap(QPixmap())
    
    def closeEvent(self, event):
        if self.test_data:
            reply = QMessageBox.question(
                self, "Save Changes?",
                "You have unsaved changes. Would you like to save before exiting?",
                QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel
            )
            
            if reply == QMessageBox.StandardButton.Save:
                self.save_test()
                event.accept()
            elif reply == QMessageBox.StandardButton.Cancel:
                event.ignore()
            else:
                event.accept()
        else:
            event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TestCreatorApp()
    window.show()
    sys.exit(app.exec())


"""
THIS WAS CREATED BY AI BC I AM FUCKING LAZY

"""