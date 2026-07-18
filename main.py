#!/usr/bin/env python3
"""
discord-rpc-linux
by 0xmakarov
small GUI for setting a custom Discord Rich Presence on Linux (PySide6 + pypresence). don't mess with something you dont how its working gng
"""

import sys
from typing import Dict, Any

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QLineEdit,
    QCheckBox,
    QPushButton,
    QComboBox,
    QLabel,
    QGroupBox,
    QMessageBox,
    QInputDialog,
    QSystemTrayIcon,
    QMenu,
    QStyle,
)

from presence_manager import PresenceManager
import profiles as profile_store
from pypresence.exceptions import DiscordNotFound, InvalidID, PipeClosed


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("discord-rpc-linux")
        self.resize(460, 640)

        self.presence = PresenceManager()

        self._build_ui()
        self._build_tray()
        self._load_profile_list(select_first=True)

    # ------------------------------------------------------------------ UI
    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)

        # --- Profiles ---
        profile_box = QGroupBox("Profile")
        profile_layout = QHBoxLayout(profile_box)
        self.profile_combo = QComboBox()
        self.profile_combo.currentTextChanged.connect(self._on_profile_selected)
        profile_layout.addWidget(self.profile_combo, stretch=1)

        btn_new = QPushButton("New")
        btn_new.clicked.connect(self._on_new_profile)
        btn_save = QPushButton("Save")
        btn_save.clicked.connect(self._on_save_profile)
        btn_delete = QPushButton("Delete")
        btn_delete.clicked.connect(self._on_delete_profile)
        profile_layout.addWidget(btn_new)
        profile_layout.addWidget(btn_save)
        profile_layout.addWidget(btn_delete)
        root.addWidget(profile_box)

        # --- Main fields ---
        form_box = QGroupBox("Rich Presence")
        form = QFormLayout(form_box)

        self.client_id_edit = QLineEdit()
        self.client_id_edit.setPlaceholderText("Application ID from Discord Developer Portal")
        form.addRow("Client ID:", self.client_id_edit)

        self.details_edit = QLineEdit()
        self.details_edit.setPlaceholderText("First line (e.g. Playing Story Mode)")
        form.addRow("Details:", self.details_edit)

        self.state_edit = QLineEdit()
        self.state_edit.setPlaceholderText("Second line (e.g. Stage 3 - Desert)")
        form.addRow("State:", self.state_edit)

        self.large_image_edit = QLineEdit()
        self.large_image_edit.setPlaceholderText("Large image asset key")
        form.addRow("Large image:", self.large_image_edit)

        self.large_text_edit = QLineEdit()
        self.large_text_edit.setPlaceholderText("Tooltip text")
        form.addRow("Large image text:", self.large_text_edit)

        self.small_image_edit = QLineEdit()
        self.small_image_edit.setPlaceholderText("Small image asset key")
        form.addRow("Small image:", self.small_image_edit)

        self.small_text_edit = QLineEdit()
        self.small_text_edit.setPlaceholderText("Tooltip text")
        form.addRow("Small image text:", self.small_text_edit)

        self.timestamp_check = QCheckBox("Show elapsed time")
        form.addRow("", self.timestamp_check)

        root.addWidget(form_box)

        # --- Buttons (clickable links on your Discord profile) ---
        buttons_box = QGroupBox("Buttons (optional, max 2)")
        buttons_form = QFormLayout(buttons_box)

        self.button1_label_edit = QLineEdit()
        self.button1_url_edit = QLineEdit()
        self.button1_url_edit.setPlaceholderText("https://...")
        buttons_form.addRow("Button 1 - label:", self.button1_label_edit)
        buttons_form.addRow("Button 1 - url:", self.button1_url_edit)

        self.button2_label_edit = QLineEdit()
        self.button2_url_edit = QLineEdit()
        self.button2_url_edit.setPlaceholderText("https://...")
        buttons_form.addRow("Button 2 - label:", self.button2_label_edit)
        buttons_form.addRow("Button 2 - url:", self.button2_url_edit)

        root.addWidget(buttons_box)

        # --- Actions ---
        actions_layout = QHBoxLayout()
        self.activate_btn = QPushButton("Activate Presence")
        self.activate_btn.clicked.connect(self._on_activate)
        self.clear_btn = QPushButton("Clear Presence")
        self.clear_btn.clicked.connect(self._on_clear)
        actions_layout.addWidget(self.activate_btn)
        actions_layout.addWidget(self.clear_btn)
        root.addLayout(actions_layout)

        self.minimize_tray_check = QCheckBox("Minimize to tray on close")
        self.minimize_tray_check.setChecked(True)
        root.addWidget(self.minimize_tray_check)
# mkv mkv mkv mkv
        self.status_label = QLabel("Status: disconnected")
        self.status_label.setAlignment(Qt.AlignCenter)
        root.addWidget(self.status_label)

    def _build_tray(self):
        icon = self.style().standardIcon(QStyle.SP_ComputerIcon)
        self.tray = QSystemTrayIcon(icon, self)
        self.tray.setToolTip("discord-rpc-linux")

        menu = QMenu()
        show_action = menu.addAction("Show window")
        show_action.triggered.connect(self._restore_window)
        clear_action = menu.addAction("Clear Presence")
        clear_action.triggered.connect(self._on_clear)
        quit_action = menu.addAction("Quit")
        quit_action.triggered.connect(self._quit_app)

        self.tray.setContextMenu(menu)
        self.tray.activated.connect(self._on_tray_activated)
        self.tray.show()

    # ---------------------------------------------------------- Profiles
    def _load_profile_list(self, select_first: bool = False):
        self.profile_combo.blockSignals(True)
        self.profile_combo.clear()
        names = list(profile_store.load_all().keys())
        self.profile_combo.addItems(names)
        self.profile_combo.blockSignals(False)

        if names and select_first:
            self.profile_combo.setCurrentIndex(0)
            self._apply_profile_data(profile_store.load_all()[names[0]])
        elif not names:
            self._apply_profile_data(profile_store.new_profile())

    def _current_form_data(self) -> Dict[str, Any]:
        return {
            "client_id": self.client_id_edit.text().strip(),
            "details": self.details_edit.text().strip(),
            "state": self.state_edit.text().strip(),
            "large_image": self.large_image_edit.text().strip(),
            "large_text": self.large_text_edit.text().strip(),
            "small_image": self.small_image_edit.text().strip(),
            "small_text": self.small_text_edit.text().strip(),
            "show_timestamp": self.timestamp_check.isChecked(),
            "button1_label": self.button1_label_edit.text().strip(),
            "button1_url": self.button1_url_edit.text().strip(),
            "button2_label": self.button2_label_edit.text().strip(),
            "button2_url": self.button2_url_edit.text().strip(),
        }

    def _apply_profile_data(self, data: Dict[str, Any]):
        self.client_id_edit.setText(data.get("client_id", ""))
        self.details_edit.setText(data.get("details", ""))
        self.state_edit.setText(data.get("state", ""))
        self.large_image_edit.setText(data.get("large_image", ""))
        self.large_text_edit.setText(data.get("large_text", ""))
        self.small_image_edit.setText(data.get("small_image", ""))
        self.small_text_edit.setText(data.get("small_text", ""))
        self.timestamp_check.setChecked(data.get("show_timestamp", False))
        self.button1_label_edit.setText(data.get("button1_label", ""))
        self.button1_url_edit.setText(data.get("button1_url", ""))
        self.button2_label_edit.setText(data.get("button2_label", ""))
        self.button2_url_edit.setText(data.get("button2_url", ""))

    def _on_profile_selected(self, name: str):
        if not name:
            return
        profiles = profile_store.load_all()
        if name in profiles:
            self._apply_profile_data(profiles[name])

    def _on_new_profile(self):
        name, ok = QInputDialog.getText(self, "New profile", "Profile name:")
        if ok and name.strip():
            name = name.strip()
            profile_store.save_profile(name, profile_store.new_profile())
            self._load_profile_list()
            self.profile_combo.setCurrentText(name)

    def _on_save_profile(self):
        name = self.profile_combo.currentText().strip()
        if not name:
            name, ok = QInputDialog.getText(self, "Save profile", "Profile name:")
            if not (ok and name.strip()):
                return
            name = name.strip()
        profile_store.save_profile(name, self._current_form_data())
        self._load_profile_list()
        self.profile_combo.setCurrentText(name)
        QMessageBox.information(self, "Saved", f"Profile '{name}' saved.")

    def _on_delete_profile(self):
        name = self.profile_combo.currentText().strip()
        if not name:
            return
        confirm = QMessageBox.question(
            self, "Delete profile", f"Delete profile '{name}'?"
        )
        if confirm == QMessageBox.Yes:
            profile_store.delete_profile(name)
            self._load_profile_list(select_first=True)

    # ------------------------------------------------------------ Actions
    def _build_buttons_payload(self):
        buttons = []
        if self.button1_label_edit.text().strip() and self.button1_url_edit.text().strip():
            buttons.append(
                {
                    "label": self.button1_label_edit.text().strip(),
                    "url": self.button1_url_edit.text().strip(),
                }
            )
        if self.button2_label_edit.text().strip() and self.button2_url_edit.text().strip():
            buttons.append(
                {
                    "label": self.button2_label_edit.text().strip(),
                    "url": self.button2_url_edit.text().strip(),
                }
            )
        return buttons

    def _on_activate(self):
        client_id = self.client_id_edit.text().strip()
        if not client_id:
            QMessageBox.warning(self, "Missing Client ID", "Enter the Client ID of your Discord application.")
            return

        try:
            self.presence.connect(client_id)
            self.presence.set_start_timestamp_now()
            self.presence.update(
                details=self.details_edit.text().strip(),
                state=self.state_edit.text().strip(),
                large_image=self.large_image_edit.text().strip(),
                large_text=self.large_text_edit.text().strip(),
                small_image=self.small_image_edit.text().strip(),
                small_text=self.small_text_edit.text().strip(),
                show_timestamp=self.timestamp_check.isChecked(),
                buttons=self._build_buttons_payload(),
            )
            self.status_label.setText("Status: connected, presence active")
        except DiscordNotFound:
            QMessageBox.critical(
                self, "Discord not found",
                "Could not find a running Discord client. Open Discord and try again."
            )
            self.status_label.setText("Status: Discord not found")
        except InvalidID:
            QMessageBox.critical(self, "Invalid Client ID", "Double check the Client ID.")
            self.status_label.setText("Status: invalid Client ID")
        except PipeClosed:
            QMessageBox.critical(self, "Connection lost", "The connection to Discord was closed. Try again.")
            self.status_label.setText("Status: connection lost")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            self.status_label.setText("Status: error")

    def _on_clear(self):
        self.presence.clear()
        self.status_label.setText("Status: presence cleared")

    # -------------------------------------------------------------- Tray
    def _on_tray_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self._restore_window()

    def _restore_window(self):
        self.showNormal()
        self.activateWindow()

    def _quit_app(self):
        self.presence.disconnect()
        QApplication.quit()

    def closeEvent(self, event):
        if self.minimize_tray_check.isChecked():
            event.ignore()
            self.hide()
            self.tray.showMessage(
                "discord-rpc-linux",
                "Still running in the tray. Click the icon to bring it back.",
                QSystemTrayIcon.Information,
                3000,
            )
        else:
            self.presence.disconnect()
            event.accept()


def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
