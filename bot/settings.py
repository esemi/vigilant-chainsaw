
# максимальное растояние для удочки
from pathlib import Path

FISHING_DISTANCE = 150.0

# сколько времени жмём на кнопку для заброски крючка в воду при рыбалке
FISHING_CLICK_DURATION = 0.5

# пауза перед поиском поплавка на воде
FISHING_BOBBER_SEARCH_DELAY = 1.0

# сколько тиков максимум ждём клёва (поплавок погрузился в воду)
FISHING_MAX_NIBBLE_WAIT_TICKS = 100

# отступ от шаблона поплавка под водой во все стороны
FISHING_BOBBER_SEARCH_ZONE_OFFSET = 20


TMP_FOLDER = Path(__file__).parent.joinpath('../data/debug/')
