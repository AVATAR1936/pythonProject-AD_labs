import numpy as np
import matplotlib.pyplot as plt

# Завдання 1: Метод Найменших Квадратів (МНК)

print("--- Завдання 1: Метод Найменших Квадратів ---")
np.random.seed(42)  # Для відтворюваності результатів (прибрати для отримання нових значень)
num_points = 100
k_orig = 2.0
b_orig = 5.0

x = 10 * np.random.rand(num_points)
# Генерація y навколо прямої y = k_orig * x + b_orig з додаванням шуму
noise = np.random.randn(num_points) * 3
y = k_orig * x + b_orig + noise
print(f"Згенеровано {num_points} точок навколо прямої y = {k_orig}x + {b_orig}")

def least_squares_fit(x_data, y_data):
    """
    Обчислює параметри k та b для лінійної регресії y = kx + b
    методом найменших квадратів.
    """
    if len(x_data) != len(y_data) or len(x_data) == 0:
        print("Помилка: Розміри масивів x та y повинні співпадати і бути не порожніми.")
        return None, None

    n = len(x_data)
    sum_x = np.sum(x_data)
    sum_y = np.sum(y_data)
    sum_xy = np.sum(x_data * y_data)
    sum_x_sq = np.sum(x_data**2)

    # Обчислення k та b
    denominator = n * sum_x_sq - sum_x**2
    if np.isclose(denominator, 0):
        print("Помилка: Знаменник близький до нуля, неможливо обчислити параметри (можливо, всі x однакові).")
        return None, None

    k = (n * sum_xy - sum_x * sum_y) / denominator
    b = (sum_y - k * sum_x) / n

    return k, b

# Обчислення та порівняння параметрів МНК
k_custom, b_custom = least_squares_fit(x, y)
k_np, b_np = np.polyfit(x, y, 1) # Поліном ступеня 1 від NumPy

print("\n--- Параметри МНК ---")
print(f"Початкові:       k = {k_orig:.4f}, b = {b_orig:.4f}")
if k_custom is not None and b_custom is not None:
    print(f"МНК (функція):  k = {k_custom:.4f}, b = {b_custom:.4f}")
else:
    print("МНК (функція):  Не вдалося обчислити")
print(f"NumPy polyfit:  k = {k_np:.4f}, b = {b_np:.4f}")


# Завдання 2: Градієнтний спуск
print("\n--- Завдання 2: Градієнтний спуск ---")

# 1. Функція градієнтного спуску
def gradient_descent(x_data, y_data, learning_rate, n_iter):
    """
    Реалізує градієнтний спуск для лінійної регресії y = kx + b.

    Args:
        x_data (np.array): Вхідні ознаки.
        y_data (np.array): Цільова змінна.
        learning_rate (float): Швидкість навчання.
        n_iter (int): Кількість ітерацій.
    """
    n_samples = len(y_data)
    if n_samples == 0 or len(x_data) != n_samples:
        print("Помилка: Некоректні вхідні дані для градієнтного спуску.")
        return None, None, []

    k = 0.0
    b = 0.0
    errors = []

    for i in range(n_iter):
        # Прогноз
        y_pred = k * x_data + b

        # Розрахунок помилки (MSE - Mean Squared Error)
        error = (1 / n_samples) * np.sum((y_pred - y_data.reshape(y_pred.shape)) ** 2)
        errors.append(error)

        # Розрахунок градієнтів
        dk = (2 / n_samples) * np.sum(x_data * (y_pred - y_data))
        db = (2 / n_samples) * np.sum(y_pred - y_data)

        k = k - learning_rate * dk
        b = b - learning_rate * db

    return k, b, errors

learning_rate = 0.01 # Менший крок навчання для стабільності
n_iterations = 1000

k_gd, b_gd, cost_history = gradient_descent(x, y, learning_rate, n_iterations)

if k_gd is not None and b_gd is not None:
    print(f"\n--- Параметри Градієнтного спуску (lr={learning_rate}, iter={n_iterations}) ---")
    print(f"Знайдені:        k = {k_gd:.4f}, b = {b_gd:.4f}")
    print(f"Помилка (MSE) на останній ітерації: {cost_history[-1]:.4f}")

    # Побудова графіку похибки від кількості ітерацій
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, len(cost_history) + 1), cost_history, marker='.', linestyle='-')
    plt.xlabel("Номер ітерації")
    plt.ylabel("Помилка (MSE)")
    plt.title(f"Зміна помилки (MSE) під час Градієнтного спуску\n(learning_rate={learning_rate})")
    plt.grid(True)
    plt.show()

    print("\n--- Висновки по графіку похибки ---")
    print("1. Графік показує, що середньоквадратична помилка (MSE) зменшується з кожною ітерацією.")
    print("2. Швидкість зменшення помилки сповільнюється, що вказує на наближення до мінімуму.")

else:
    print("\nГрадієнтний спуск не вдалося виконати.")

# Загальний графік та порівняння
plt.figure(figsize=(12, 7))
plt.scatter(x, y, label='Згенеровані дані', alpha=0.6, color='skyblue')

x_line = np.linspace(min(x), max(x), 100)

# Початкова лінія
plt.plot(x_line, k_orig * x_line + b_orig, 'r--', linewidth=2, label=f'Початкова: y = {k_orig:.2f}x + {b_orig:.2f}')

# Лінія МНК (функція)
if k_custom is not None and b_custom is not None:
    plt.plot(x_line, k_custom * x_line + b_custom, 'g-', linewidth=2, label=f'МНК (функція): y = {k_custom:.2f}x + {b_custom:.2f}')

# Лінія NumPy polyfit
plt.plot(x_line, k_np * x_line + b_np, 'orange', linestyle=':', linewidth=3, label=f'NumPy polyfit: y = {k_np:.2f}x + {b_np:.2f}')

# Лінія Градієнтного спуску
if k_gd is not None and b_gd is not None:
    plt.plot(x_line, k_gd * x_line + b_gd, 'm-.', linewidth=2, label=f'Град. спуск: y = {k_gd:.2f}x + {b_gd:.2f}')

plt.xlabel("X")
plt.ylabel("Y")
plt.title("Порівняння методів лінійної регресії")
plt.legend()
plt.grid(True)
plt.ylim(min(y) - 5, max(y) + 5) # Налаштування меж для кращої візуалізації
plt.xlim(min(x) - 1, max(x) + 1)
plt.show()

print("\n--- Загальне порівняння результатів ---")
print(f"Метод            | k       | b")
print(f"-----------------|---------|---------")
print(f"Початкові        | {k_orig:<7.4f} | {b_orig:<7.4f}")
if k_custom is not None and b_custom is not None:
    print(f"МНК (функція)    | {k_custom:<7.4f} | {b_custom:<7.4f}")
else:
    print(f"МНК (функція)    | N/A     | N/A")
print(f"NumPy polyfit    | {k_np:<7.4f} | {b_np:<7.4f}")
if k_gd is not None and b_gd is not None:
    print(f"Град. спуск      | {k_gd:<7.4f} | {b_gd:<7.4f}")
else:
    print(f"Град. спуск      | N/A     | N/A")

print("\nВисновки порівняння:")
print("- Метод найменших квадратів (реалізований вручну та за допомогою NumPy) дає практично однакові результати.")
if k_gd is not None and k_custom is not None:
    diff_k = abs(k_gd - k_custom)
    diff_b = abs(b_gd - b_custom)
    print(f"- Градієнтний спуск, будучи ітеративним методом, також знайшов параметри, дуже близькі до результатів МНК (різниця k: {diff_k:.4f}, різниця b: {diff_b:.4f}).")
else:
     print("- Градієнтний спуск, будучи ітеративним методом, також може знаходити параметри, близькі до МНК, але потребує налаштування гіперпараметрів.")
