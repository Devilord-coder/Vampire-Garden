from src.settings import settings

SCREEN_WIDTH = settings.width
SCREEN_HEIGHT = settings.height

TILE_SCALING = 1  # Если тайлы 64x64, а хотим чтобы на экране были 64x64 — ставим 1.0

# Физика и движение
GRAVITY = 0.5           # Пикс/с^2

# Качество жизни прыжка
COYOTE_TIME = 0.08        # Сколько после схода с платформы можно ещё прыгнуть
JUMP_BUFFER = 0.12        # Если нажали прыжок чуть раньше приземления, мы его «запомним» (тоже лайфхак для улучшения качества жизни игрока)
MAX_JUMPS = 1             # С двойным прыжком всё лучше, но не сегодня

# ---------- Камера ----------
CAMERA_LERP = 0.12
DEAD_ZONE_W = int(SCREEN_WIDTH * 0.35)
DEAD_ZONE_H = int(SCREEN_HEIGHT * 0.45)

# --------- Персонаж ---------
PLAYER_SCALING = 1.2
PLAYER_JUMP_SPEED = 10
PLAYER_WALK_SPEED = 3
PLAYER_RUN_SPEED = 6