import random
import json
from time import sleep


class Human:
    def __init__(self, name):
        self.name = name
        self.money = 20
        self.gladness = 50
        self.car = None

    def greeting(self, human):
        print(f"Hello {human.name}, I am {self.name}")

    def drive(self):
        if self.car:
            self.car.drive()

    def work(self):
        # Сделать случайное добавление денег и отнятие счастья
        self.money += random.randint(5, 10)
        self.gladness -= random.randint(2, 5)

    def rest(self):
        # Сделать случайное отнятие денег и добавление счастья
        self.money -= random.randint(3, 7)
        self.gladness += random.randint(2, 5)


class House:
    def __init__(self):
        self.humans = []

    def add(self, human):
        if not human in self.humans:
            self.humans.append(human)

    def greetingAll(self):
        for human in self.humans:
            for some_human in self.humans:
                if human != some_human:
                    human.greeting(some_human)


class Car:
    def __init__(self, name, year, price):
        self.name = name
        self.year = year
        self.price = price
        self.owner = None

    def drive(self):
        print(f"{self.name} едет")

    def buy(self, human):
        if not self.owner:
            if human.money >= self.price:
                self.owner = human
                human.car = self
                print(f"{human.name} купил {self.name}")
            else:
                print(f"{human.name} не хватает средств на {self.name}")
        else:
            print(f"У {self.name} уже есть хозяин - {self.owner.name}")


class Player(Human):
    def __init__(self, name, h, w):
        super().__init__(name)
        self.height = h
        self.weight = w

    def save(self):
        with open('./save.json', 'w') as f:
            data = {}
            data["name"] = self.name
            data["h"] = self.height
            data["w"] = self.weight
            json.dump(data, f)

    def actions(self):
        print("Выберите действие: ")
        print("1. Отдохнуть")
        print("2. Пойти на работу")
        print("3. Купить машину")
        print("4. Баланс")
        print("5.Поесть")
        print("6. Ничего не делать")
        print("7. Пойти гулять")

    def day(self):
        choice = int(input("-> "))
        if choice == 1:
            self.rest()
        elif choice == 2:
            self.work()
        elif choice == 3:
            # Показываем какие есть машины
            print("Машины: ")
            for i in range(len(autopark)):
                print(f"{i + 1}. {autopark[i].name}")
            # выбираем машину и покупаем
            choice = int(input("-> "))
            if choice > 0 and choice < len(autopark):
                autopark[choice - 1].buy(self)
        elif choice == 4:
            print(f"Баланс: {self.money}")
            self.day()
        else:
            self.day()


class Thief(Human):
    def __init__(self, name):
        super().__init__(name)
        # strengh = рандомное число 1-10
        self.strength = random.randint(1, 10)

    def steal(self, human):
        # забирает деньги у человека равные strengh
        human.money -= self.strength
        # добавляет их себе
        self.money += self.strength
        # сообщаем, что вор обокрал кого-то
        print(f"Вор украл деньги у {human.name}")



house = None
autopark = None
player = None
thief = None


def game_start():
    global house, autopark, thief
    house = House()
    thief = Thief("Vladislav")

    h1 = Human("Sergey")
    h2 = Human("Ivan")
    h3 = Human("Dima")
    h4 = Human("Petr")
    h5 = Human("Nastya")
    h6 = Human("Katya")
    h7 = Human("Alex")
    h8 = Human("Kristina")

    house.add(h1)
    house.add(h2)
    house.add(h3)
    house.add(h4)
    house.add(h5)
    house.add(h6)
    house.add(h7)
    house.add(h8)

    autopark = [
        Car("BMW", 2019, 200),
        Car("Bentli", 2019, 100),
        Car("Bugatti", 2019, 300),
    ]


def create_player():
    global player
    h = input("Введите рост персонажа: ")
    w = input("Введите вес персонажа: ")
    name = input("Введите имя персонажа: ")
    player = Player(name, h, w)
    player.save()


def init_player():
    global player
    with open('./save.json') as json_file:
        data = json.load(json_file)
        if not data:
            create_player()
        else:
            player = Player(data["name"], data["h"], data["w"])
    house.add(player)


game_start()
init_player()

day = 1
while True:
    print("Day: ", day)
    player.actions()
    player.day()
    for human in house.humans:
        if human == player:
            continue
        actions = [human.rest, human.work]
        random.choice(actions)()
        if random.randint(1, 100) <= 5:
            print(f"{human.name} хочет купить машину")
            random.choice(autopark).buy(human)
    # с шансом 20% вор крадет деньги
    if random.randint(1, 100) <= 20:
# у случайного человека, который живет в доме
thief.steal(random.choice(house.humans))
day += 1
# сообщаем, что вора словили
print(f"Вор был словлен")
# сообщаем, что человеку вернули денги
print(f"Вернули денги {human.name}")