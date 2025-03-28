from PyQt5.QtWidgets import *

class ParamsController:
    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.view.params_btn.clicked.connect(self.open_params)
        self.model.params_loaded.connect(self.params_loaded)

        # Load default
        self.model.process_params_file("app/resources/last_params.json")

    def open_params(self):
        file_path, _ = QFileDialog.getOpenFileName(self.view, "Open File", "", "All Files (*)")
        if file_path:
            if self.model.process_params_file(file_path):
                self.view.params_file_input.setPlainText(file_path)
            else:
                QMessageBox.information(self.view, "Error", "File format incorrect")

    def params_loaded(self):
        result = ""
        for field_name in self.model.params_payload.field_names:
            value = getattr(self.model.params_payload.data, field_name)
            result += f"{field_name}: {value}\n"
        self.view.file_view.setPlainText(result)