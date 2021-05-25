from pathlib import Path

# максимальное растояние для удочки
FISHING_DISTANCE = 150.0

# сколько времени жмём на кнопку для заброски крючка в воду при рыбалке
FISHING_CLICK_DURATION = 0.5

# пауза перед поиском поплавка на воде
FISHING_BOBBER_SEARCH_DELAY = 2.0

# сколько тиков максимум ждём клёва (поплавок погрузился в воду)
FISHING_MAX_NIBBLE_WAIT_TICKS = 1000

# отступ от шаблона поплавка под водой во все стороны
FISHING_BOBBER_SEARCH_ZONE_OFFSET = 20

# Порог чувствительности попловка при клёве.
# Чем выше - тем больше ряби на воде требуется для тригера на подсекание рыбки
FISHING_NIBBLES_THRESHOLD = 0.20

TMP_FOLDER = Path('/tmp/fishing-bot')
if not TMP_FOLDER.exists():
    TMP_FOLDER.mkdir(exist_ok=True)
