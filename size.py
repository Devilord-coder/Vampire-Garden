from PIL import Image

def get_image_size(image_path):
    """
    Получает и выводит размер изображения.
    
    Args:
        image_path (str): Путь к файлу изображения
    """
    try:
        # Открываем изображение
        with Image.open(image_path) as img:
            # Получаем размеры изображения
            width, height = img.size
            
            # Выводим информацию о размере
            print(f"Путь к изображению: {image_path}")
            print(f"Размер изображения: {width} x {height} пикселей")
            print(f"Ширина: {width} пикселей")
            print(f"Высота: {height} пикселей")
            print(f"Формат: {img.format}")
            print(f"Цветовой режим: {img.mode}")
            
            # Дополнительно можно вывести размер файла на диске
            import os
            file_size = os.path.getsize(image_path)
            print(f"Размер файла: {file_size} байт ({file_size/1024:.2f} КБ)")
            
            return width, height
            
    except FileNotFoundError:
        print(f"Ошибка: Файл '{image_path}' не найден.")
    except Exception as e:
        print(f"Ошибка при открытии изображения: {e}")

# Пример использования
if __name__ == "__main__":
    # Укажите путь к вашему изображению
    image_path ="resources/buttons/exit/shop_exit.png"  # Замените на путь к вашему изображению
    
    # Альтернативный вариант - запросить путь у пользователя
    # image_path = input("Введите путь к изображению: ")
    
    get_image_size(image_path)