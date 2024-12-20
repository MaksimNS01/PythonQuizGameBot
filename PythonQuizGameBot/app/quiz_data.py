# Структура квиза
quiz_data = [
    # Вопрос 1
    {
        'question': 'Что такое Python?',
        'options': ['Тип данных', 'Музыкальный инструмент', 'Змея на английском', 'Язык программирования'],
        'correct_option': 3
    },
    # Вопрос 2
    {
        'question': 'Какой тип данных используется для хранения целых чисел?',
        'options': ['int', 'float', 'str', 'natural'],
        'correct_option': 0
    },
    # Вопрос 3
    {
        'question': 'Как получить данные от пользователя?',
        'options': ['get()', 'input()', 'read()', 'cin()', 'readLine()'],
        'correct_option': 1
    },
    # Вопрос 4
    {
        'question': 'Какая функция выводит что-либо в консоль?',
        'options': ['print()', 'out()', 'write()', 'log()'],
        'correct_option': 0
    },
    # Вопрос 5
    {
        'question': 'Какая библиотека отвечает за время?',
        'options': ['clock', 'localtime', 'time', 'Time'],
        'correct_option': 2
    },
    # Вопрос 6
    {
        'question': 'Сколько библиотек можно импортировать в один проект?',
        'options': ['Не более 3', 'Не более 10', 'Не более 5', 'Не более 23', 'Неограниченное количество'],
        'correct_option': 4
    },
    # Вопрос 7
    {
        'question': 'Для чего в Python используется встроенная функция enumerate() для последовательностей?',
        'options': ['Определение кол-ва элементов', 'Итерирация по элементам и индексам', 'Сортировка элементов по id'],
        'correct_option': 1
    },
    # Вопрос 8
    {
        'question': 'Как вывести список методов и атрибутов объекта x?',
        'options': ['help(x)', 'info(x)', '?x', 'dir(x)'],
        'correct_option': 3
    },
    # Вопрос 9
    {
        'question': 'При объявлении класса с помощью оператора class что пишется в круглых скобках после имени класса?',
        'options': ['Имена аргументов __init__', 'Имена аргументов класса', 'Имена суперклассов', 'Имена дочерних классов'],
        'correct_option': 2
    },
    # Вопрос 10
    {
        'question': 'Имеется кортеж вида T = (4, 2, 3). Какая из операций приведёт к тому, что имя T будет ссылаться на кортеж (1, 2, 3)?',
        'options': ['T[0] = 1', 'T = (1) + T[1:]', 'T = (1,) + T[1:]', 'T.startswith(1)'],
        'correct_option': 2
    }
]
