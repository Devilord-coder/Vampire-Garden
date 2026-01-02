from PIL import Image
import os

def resize_image(input_path, output_path, width=None, height=None, scale=None, keep_aspect_ratio=True):
    """
    Изменяет размер изображения.
    
    Args:
        input_path (str): Путь к исходному изображению
        output_path (str): Путь для сохранения измененного изображения
        width (int): Новая ширина (в пикселях)
        height (int): Новая высота (в пикселях)
        scale (float): Масштаб (например, 0.5 для уменьшения в 2 раза)
        keep_aspect_ratio (bool): Сохранять ли соотношение сторон
    """
    try:
        # Открываем изображение
        with Image.open(input_path) as img:
            original_width, original_height = img.size
            
            print(f"Исходный размер: {original_width} x {original_height} пикселей")
            print(f"Формат: {img.format}")
            
            # Определяем новый размер
            if scale is not None:
                # Изменение по масштабу
                new_width = int(original_width * scale)
                new_height = int(original_height * scale)
            elif width is not None and height is not None:
                # Заданы оба размера
                new_width = width
                new_height = height
            elif width is not None:
                # Задана только ширина
                if keep_aspect_ratio:
                    ratio = width / original_width
                    new_width = width
                    new_height = int(original_height * ratio)
                else:
                    new_width = width
                    new_height = original_height
            elif height is not None:
                # Задана только высота
                if keep_aspect_ratio:
                    ratio = height / original_height
                    new_width = int(original_width * ratio)
                    new_height = height
                else:
                    new_width = original_width
                    new_height = height
            else:
                print("Ошибка: Не указаны параметры для изменения размера.")
                return
            
            print(f"Новый размер: {new_width} x {new_height} пикселей")
            
            # Изменяем размер
            resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Сохраняем изображение
            resized_img.save(output_path)
            
            print(f"✓ Изображение сохранено: {output_path}")
            
            # Показываем информацию о размере файла
            original_size = os.path.getsize(input_path)
            new_size = os.path.getsize(output_path)
            
            print(f"Исходный размер файла: {original_size/1024:.2f} КБ")
            print(f"Новый размер файла: {new_size/1024:.2f} КБ")
            print(f"Изменение: {((new_size - original_size)/original_size)*100:.1f}%")
            
            return resized_img
            
    except FileNotFoundError:
        print(f"Ошибка: Файл '{input_path}' не найден.")
    except Exception as e:
        print(f"Ошибка при обработке изображения: {e}")


# Пример использования
if __name__ == "__main__":
    # Пример 1: Уменьшить изображение в 2 раза
    resize_image(
        input_path= "resources/Background/paper.png",
        output_path= "resources/Background/paper.png",
        width=1350,
        height=700
    )