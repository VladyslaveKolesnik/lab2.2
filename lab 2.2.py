from dataclasses import dataclass
from enum import Enum
from typing import List

# Enum для кімнат
class Room(Enum):
    KITCHEN = "Кухня"
    BEDROOM = "Спальня"
    GARAGE = "Гараж"

#  Використання dataclasses для зберігання даних (спрощено)
@dataclass
class DeviceConfig:
    brand: str
    short_id: str  # Замість мак-адреси просто короткий ідентифікатор

# Базовий клас
class Device:
    def __init__(self, name: str, room: Room, config: DeviceConfig):
        # 2. Приватність стану (атрибути захищені підкресленням)
        self.name = name  
        self.room = room
        self.config = config
        self._is_on = False

    #  Декоратор @property (Гетер)
    @property
    def name(self) -> str:
        return self._name

    #  Декоратор @setter з логічною валідацією
    @name.setter
    def name(self, value: str):
        if len(value.strip()) < 3:
            #  Генерування ValueError
            raise ValueError("Назва має містити хоча б 3 символи.")
        self._name = value.strip()

    def turn_on(self):
        self._is_on = True
        print(f"Пристрій [{self.name}] увімкнено.")

# Нащадок 1
class SmartLight(Device):
    def __init__(self, name: str, room: Room, config: DeviceConfig, brightness: int = 100):
        super().__init__(name, room, config)
        self.brightness = brightness 
        self._previous_state = False

    @property
    def brightness(self) -> int:
        return self._brightness

    @brightness.setter
    def brightness(self, value: int):
        if not (0 <= int(value) <= 100):
            raise ValueError("Яскравість має бути від 0 до 100.")
        self._brightness = int(value)

    def turn_on(self):
        self._is_on = True
        print(f"Світло [{self.name}] у кімнаті [{self.room.value}] увімкнено. Яскравість: {self.brightness}%.")

# Нащадок 2
class SmartThermostat(Device):
    def __init__(self, name: str, room: Room, config: DeviceConfig, temperature: float = 22.0):
        super().__init__(name, room, config)
        self.temperature = temperature 
        self._previous_temp = 22.0

    @property
    def temperature(self) -> float:
        return self._temperature

    @temperature.setter
    def temperature(self, value: float):
        if not (10.0 <= float(value) <= 35.0):
            raise ValueError("Температура має бути від 10 до 35 градусів.")
        self._temperature = float(value)

    def turn_on(self):
        self._is_on = True
        print(f"Термостат [{self.name}] у кімнаті [{self.room.value}] увімкнено. Температура: {self.temperature} C.")

# Композиція
class HomeHub:
    def __init__(self):
        self.devices: List[Device] = []

    def add_device(self, device: Device):
        self.devices.append(device)
        print(f"Пристрій '{device.name}' (Кімната: {device.room.value}) додано до хабу.")

# Контекст-менеджер "Нічний режим"
class NightMode:
    def __init__(self, hub: HomeHub):
        self.hub = hub

    def __enter__(self):
        print("\n--- Нічний режим увімкнено ---")
        for dev in self.hub.devices:
            if isinstance(dev, SmartLight):
                dev._previous_state = dev._is_on
                dev._is_on = False
                print(f"Вимкнено світло: {dev.name} у {dev.room.value}")
            elif isinstance(dev, SmartThermostat):
                dev._previous_temp = dev.temperature
                dev.temperature = 18.0
                print(f"Температуру для [{dev.name}] у {dev.room.value} знижено до 18.0 C")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("--- Нічний режим вимкнено ---\n")

# Функція для вибору кімнати користувачем
def select_room():
    print("Оберіть кімнату: 1 - Кухня, 2 - Спальня, 3 - Гараж")
    choice = input("Ваш вибір (1/2/3): ")
    if choice == '1': 
        return Room.KITCHEN
    elif choice == '2': 
        return Room.BEDROOM
    elif choice == '3': 
        return Room.GARAGE
    else: 
        return Room.BEDROOM  # за замовчуванням


#  Блок демонстрації
if __name__ == "__main__":
    hub = HomeHub()
    
    #  Обробка помилок
    try:
        print("\n--- Створення лампи ---")
        l_name = input("Введіть назву лампи: ")
        l_room = select_room()
        l_bright = input("Введіть яскравість (0-100): ")
        
        conf_light = DeviceConfig(brand="Xiaomi", short_id="L-01")
        light = SmartLight(name=l_name, room=l_room, config=conf_light, brightness=l_bright)
        hub.add_device(light)
        print(vars(light))

        print("\n--- Створення термостата ---")
        t_name = input("Введіть назву термостата: ")
        t_room = select_room()
        t_temp = input("Введіть температуру (10-35): ")
        
        conf_thermo = DeviceConfig(brand="Bosch", short_id="T-01")
        thermo = SmartThermostat(name=t_name, room=t_room, config=conf_thermo, temperature=t_temp)
        hub.add_device(thermo)
        print(vars(thermo))

        with NightMode(hub):
            pass

    except ValueError as e:
        print(f"\nПомилка: {e}")
    except Exception as e:
        print(f"\nНепередбачувана помилка: {e}")