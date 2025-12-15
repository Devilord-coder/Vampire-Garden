import screeninfo


class Settings:
    def __init__(self):
        # self.fps = 60 в arcade это не требуется через delta_time уже учитываем частоту кадров
        monitor = screeninfo.get_monitors()[0]
        self.resolution = self.width, self.height = monitor.width, monitor.height  # Разрешение экрана
        # Минимальное разрешение экрана
        self.resolution_min = self.width_min, self.height_min = 800, 600
        self.resizable = True  # Флажок для редактирования размера окна
        self.fullscreen = False  # Полноэкранный режим экрана тогда берется размер экрана

        self.title = "Vampire Garden"  # Название приложения

        self.reboot = False  # Флажок для перезагрузки приложения


settings = Settings()
