def scale(current_size, current_monitor_height, base_monitor_height=900):
    '''Метод для вычисления масштабирования картинок, кнопок, карт и тд'''
    
    new_size = current_monitor_height * current_size / base_monitor_height
    return new_size / current_size