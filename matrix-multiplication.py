import numpy as np
import time


def print_snake_text(text, delay=0.1):
    """Печатает текст по одной букве с задержкой."""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()


def get_user_input():
    while True:
        try:
            first_mat_length = tuple(
                map(int, input('Введите размерность первой матрицы(например "2 2" или "2 3"): ').strip().split()))
            second_mat_length = tuple(map(int, input('Введите размерность второй матрицы: ').strip().split()))

            if len(first_mat_length) != 2 or len(second_mat_length) != 2:
                print('Пожалуйста, введите ровно 2 числа для каждой матрицы.')
                continue

            if first_mat_length[1] != second_mat_length[0]:  # проверка на возможность умножения матриц
                print(f'Ошибка: для умножения двух матриц число столбцов первой матрицы {first_mat_length[1]} '
                      f'должно равняться числу строк второй матрицы {second_mat_length[0]}.')
                continue

            new_iteration = False
            for n in range(len(first_mat_length)):
                if first_mat_length[n] <= 0 or second_mat_length[n] <= 0:
                    new_iteration = True
                    break
            if new_iteration:
                print_snake_text('Пожалуйста, введите действительные числа.', delay=0.04)
                continue

            mode_selection = input(
                'Вы хотели бы ввести свою матрицу или сгенерировать случайную(св/сл): ').strip().lower()
            if mode_selection not in ['своя', 'св', 'случайная', 'случ', 'сл']:
                print('Пожалуйста, введите "св" (свою) или "сл" (случайную).')
                continue

            return first_mat_length, second_mat_length, mode_selection

        except ValueError:
            print('Ошибка: Введите только целые числа, разделенные пробелом.')
        except Exception as e:
            print(f"Ошибка: {e}")


def create_random_matrix(shape, min_value, max_value):
    return np.random.randint(min_value, max_value + 1, size=shape)


def input_matrix(name, shape):
    rows, cols = shape
    print_snake_text(f'Введите элементы {name} ({rows}x{cols}), по строкам.', delay=0.04)
    matrix = []
    for i in range(rows):
        while True:
            try:
                row = list(map(int, input(f'Строка {i + 1} (через пробел): ').strip().split()))
                if len(row) != cols:
                    print(f'Нужно ввести ровно {cols} чисел.')
                    continue
                matrix.append(row)
                break
            except ValueError:
                print('Введите только целые числа.')
    return np.array(matrix)


def matrix_manual_dot(matrix1, matrix2):
    """Ручное умножение 2 матриц."""
    result_arr = np.zeros((matrix1.shape[0], matrix2.shape[1]), dtype=int)  # создание матрицы-результата из нулей
    for row in range(matrix1.shape[0]):  # проходим по каждой строке
        for col in range(matrix2.shape[1]):  # проходим по каждому столбцу
            # получаем i-ю строку и j-й столбец
            row1 = matrix1[row]  # вектор-строка
            col2 = matrix2[:, col]  # вектор-столбец

            # получение скалярного произведения
            dot_product = 0
            for i in range(len(row1)):
                dot_product += row1[i] * col2[i]

            # записывание результата в ячейку
            result_arr[row][col] = dot_product

    return result_arr


def matrix_normal_dot(matrix1, matrix2):
    return np.dot(matrix1, matrix2)


if __name__ == "__main__":
    welcome_message = """
    Здравствуйте. Эта программа была написана для закрепления знаний(которых нет) по перемножению матриц и из-за того что мне нечего делать.
    Суть в том, чтобы продемонстрировать разницу во времени выполнения двух подходов перемножения матриц относительно любых
    размерностей(спросите разрешение у своего устройства, оно может обидеться:D). Я их так и назвал: "ручной метод" - это тот, который написал я
    и "быстрый метод", который является однострочным и включен в numpy.

    К слову, если этот текст выводится отрывисто, то это значит, что ему мешает буферизация. Запустите в терминале для лучшего опыта: "python -u matrix-multiplication.py".
    """
    print_snake_text(welcome_message, delay=0.01)
    time.sleep(0.5)

    first_shape, second_shape, mode = get_user_input()

    if mode in ['свою', 'св']:
        print_snake_text('Я рад, что вы хотите попробовать с собственной матрицей. Начнем.', delay=0.04)
        time.sleep(0.5)
        mat1 = input_matrix('первой матрицы', first_shape)
        mat2 = input_matrix('второй матрицы', second_shape)
    else:
        print_snake_text('Хороший выбор. Поехали.', delay=0.04)
        time.sleep(0.5)
        try:
            min_val, max_val = map(int, input(
                'Введите минимальное и максимальное числа диапазона значений в матрице через пробел(напр.: "0 10"): ').strip().split())
        except ValueError:
            print('Неверный диапазон. Будут использованы значения по умолчанию(0-10).')
            min_val, max_val = 0, 10

        if max_val < min_val:
            print('Максимальное значение превышает минимальное. Будут использованы значения по умолчанию(0-10).')
            min_val, max_val = 0, 10

        mat1 = create_random_matrix(first_shape, min_val, max_val)
        mat2 = create_random_matrix(second_shape, min_val, max_val)

    print_snake_text(f'Первая матрица: \n{mat1}', delay=0.04)
    print_snake_text(f'Вторая матрица: \n{mat2}', delay=0.04)
    print_snake_text('Произвожу вычисления...', delay=0.04)

    # проверка скорости 'ручного' подхода
    start_manual_time = time.time()
    result_arr = matrix_manual_dot(mat1, mat2)
    end_manual_time = time.time()
    execution_manual_time = end_manual_time - start_manual_time

    print_snake_text(f'Результат умножения двух матриц: \n{result_arr}', delay=0.04)

    # проверка скорости 'быстрого' подхода
    start_normal_time = time.time()
    result_arr1 = matrix_normal_dot(mat1, mat2)
    end_normal_time = time.time()
    execution_normal_time = end_normal_time - start_normal_time

    # определение победителя по скорости(нужно ли это вообще)
    message_competition_winner = None
    if execution_manual_time < execution_normal_time:
        message_competition_winner = 'Свершилось чудо! Победителем оказался "ручной подход"! Этого никто не мог предположить...'
    elif execution_manual_time > execution_normal_time:
        message_competition_winner = 'Расходимся. Выиграл "быстрый подход". Как всегда ничего интересного...'
    else:
        message_competition_winner = 'ЧТО? Два подхода... Они одинаковы... Невероятно!'

    print_snake_text('В соревновании за первое место по скорости побеждает...', delay=0.04)
    print_snake_text('Барабанная дробь...', delay=0.1)
    print_snake_text(f'{message_competition_winner}', delay=0.04)

    watch_stats = False
    try:
        statistics = input('Вы хотели бы взглянуть на статистику(да/нет)? ').strip().lower()
        if statistics in ['да', 'д']:
            watch_stats = True
        else:
            print_snake_text('Жаль...', delay=0.04)
    except ValueError:
        print('Вы ввели что то не то, приму это за "да".')
        watch_stats = True

    if watch_stats:
        print_snake_text(f'Ручное умножение -> {execution_manual_time} секунд.', delay=0.04)
        print_snake_text(f'Быстрое умножение -> {execution_normal_time} секунд.', delay=0.04)
        print_snake_text(f'Результаты совпадают? {np.array_equal(result_arr, result_arr1)}', delay=0.04)

    print_snake_text('Спасибо за тест этой программы:). Пока.', delay=0.04)

