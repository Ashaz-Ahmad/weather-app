from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QRadioButton, QDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from weather import get_weather

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter a city name: ", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather")
        self.temperature_label = QLabel(self)
        self.feels_like = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        self.settings_button = QPushButton("Settings")
        self.init_ui()
        self.temperature_unit = "Celsius"

    def init_ui(self):
        self.setWindowTitle("Weather App")
        self.setWindowIcon(QIcon("app icon.ico"))

        vbox = QVBoxLayout()

        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.feels_like)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)
        vbox.addWidget(self.settings_button)

        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.feels_like.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.feels_like.setObjectName("feels_like")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")
        self.settings_button.setObjectName("settings_button")

        self.setStyleSheet("""
            QLabel, QPushButton{
                font-family: arial;
            }
            QLabel#city_label{
                font-size: 70px;   
            }
            QLineEdit#city_input{
                font-size: 40px;
            }
            QPushButton#get_weather_button{
                font-size: 35px;
                font-weight: bold;
            }
            QLabel#temperature_label{
                font-size: 80px;    
            }
            QLabel#feels_like{
                font-size: 40px;    
            }
            QLabel#emoji_label{
                font-size: 115px;
                font-family: Segoe UI Emoji;
            }
            QLabel#description_label{
                font-size: 60px;
            }
            QPushButton#settings_button{
                font-size: 35px;
            }
        """)

        self.get_weather_button.clicked.connect(self.get_city)
        self.settings_button.clicked.connect(self.open_settings)

    def get_city(self):
        city = self.city_input.text()
        get_weather(self, city)

    def display_error(self, error_message):
        self.temperature_label.setStyleSheet("font-size: 45px;")
        self.temperature_label.setText(error_message)
        self.emoji_label.clear()
        self.description_label.clear()
        self.feels_like.clear()

    def open_settings(self):
        dialog = SettingsDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.temperature_unit = dialog.get_temperature_unit()

    def display_weather(self, data):
        self.temperature_label.setStyleSheet("font-size: 80px;")
        temperature_k = (data["main"]["temp"])
        feels_like_k = (data["main"]["feels_like"])

        if self.temperature_unit == "Fahrenheit":
            temperature = (temperature_k - 273.15) * (9/5) + 32
            feels_like = (feels_like_k - 273.15) * (9/5) + 32
            self.temperature_label.setText(f"{temperature:.0f}°F")
            self.feels_like.setText(f"Feels like: {feels_like:.0f}°F")
        else:
            temperature = (temperature_k - 273.15)
            feels_like = (feels_like_k - 273.15)
            self.temperature_label.setText(f"{temperature:.0f}°C")
            self.feels_like.setText(f"Feels like: {feels_like:.0f}°C")

        weather_id = data["weather"][0]["id"]
        weather_description = data["weather"][0]["description"]
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.description_label.setText(weather_description)

    @staticmethod
    def get_weather_emoji(weather_id):
        if 200 <= weather_id <= 232:
            return "⛈️"
        elif 300 <= weather_id <= 321:
            return "🌦️"
        elif 500 <= weather_id <= 531:
            return "🌧️"
        elif 600 <= weather_id <= 622:
            return "🌨️"
        elif 701 <= weather_id <= 741:
            return "🌫️"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "💨"
        elif weather_id == 781:
            return "🌪️"
        elif weather_id == 800:
            return "☀️"
        elif 801 <= weather_id <= 804:
            return "☁️"
        else:
            return ""

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setWindowIcon(QIcon("settings.ico"))
        self.instructions = QLabel("Pick a unit of temperature:", self)

        self.resize(350, 400)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        self.celsius_radio = QRadioButton("Celsius")
        self.fahrenheit_radio = QRadioButton("Fahrenheit")

        self.celsius_radio.setChecked(True)

        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)

        vbox = QVBoxLayout()
        vbox.setAlignment(Qt.AlignTop)

        vbox.addWidget(self.instructions)
        vbox.addWidget(self.celsius_radio)
        vbox.addWidget(self.fahrenheit_radio)
        vbox.addWidget(self.ok_button)

        self.setLayout(vbox)

    def get_temperature_unit(self):
        if self.celsius_radio.isChecked():
            return "Celsius"
        else:
            return "Fahrenheit"