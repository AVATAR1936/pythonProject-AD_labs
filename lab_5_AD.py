import matplotlib
matplotlib.use('TkAgg')
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, CheckButtons
from scipy.signal import iirfilter, filtfilt

plt.ion()

# Початкові параметри
init_amp = 1.0
init_freq = 1.0
init_phase = 0.0
init_noise_mean = 0.0
init_noise_std = 0.1
show_noise = True

init_order = 4
init_cutoff = 0.05

t = np.linspace(0, 2 * np.pi, 1000)

def gen_noise(mean, std):
    return np.random.normal(mean, std, size=t.shape)

noise = gen_noise(init_noise_mean, init_noise_std)
last_noise_params = (init_noise_mean, init_noise_std)

def create_filter(order, cutoff):
    b, a = iirfilter(order, cutoff, btype='low', ftype='butter')
    return b, a

b, a = create_filter(init_order, init_cutoff)

def filter_signal(x):
    return filtfilt(b, a, x)

fig, ax = plt.subplots()
plt.subplots_adjust(left=0.3, bottom=0.45)

y_clean = init_amp * np.sin(init_freq * t + init_phase)
y_noisy = y_clean + noise
line_noisy, = ax.plot(t, y_noisy, label='Зашумлена')
line_filtered, = ax.plot(t, filter_signal(y_noisy), label='Фільтрована')
line_clean, = ax.plot(t, y_clean, '--', label='Чиста')
ax.set_title('Гармоніка з шумом та фільтрацією')
ax.legend()

ax_amp = plt.axes([0.3, 0.35, 0.6, 0.03])
amp_slider = Slider(ax_amp, 'Амплітуда', 0.1, 5.0, valinit=init_amp)

ax_freq = plt.axes([0.3, 0.30, 0.6, 0.03])
freq_slider = Slider(ax_freq, 'Частота', 0.1, 10.0, valinit=init_freq)

ax_phase = plt.axes([0.3, 0.25, 0.6, 0.03])
phase_slider = Slider(ax_phase, 'Фаза', 0.0, 2*np.pi, valinit=init_phase)

ax_mean = plt.axes([0.3, 0.20, 0.6, 0.03])
mean_slider = Slider(ax_mean, 'Шум μ', -1.0, 1.0, valinit=init_noise_mean)

ax_std = plt.axes([0.3, 0.15, 0.6, 0.03])
std_slider = Slider(ax_std, 'Шум σ', 0.01, 1.0, valinit=init_noise_std)

ax_order = plt.axes([0.3, 0.10, 0.6, 0.03])
order_slider = Slider(ax_order, 'Порядок фільтра', 1, 10, valinit=init_order, valstep=1)

ax_cutoff = plt.axes([0.3, 0.05, 0.6, 0.03])
cutoff_slider = Slider(ax_cutoff, 'Cutoff', 0.01, 0.5, valinit=init_cutoff)

ax_check = plt.axes([0.05, 0.6, 0.2, 0.15])
check = CheckButtons(ax_check, ['Показати шум'], [show_noise])

ax_reset = plt.axes([0.8, 0.01, 0.1, 0.04])
reset_button = Button(ax_reset, 'Reset', color='lightgoldenrodyellow', hovercolor='0.975')

def update(val):
    global noise, last_noise_params, b, a
    amp = amp_slider.val
    freq = freq_slider.val
    ph = phase_slider.val
    m = mean_slider.val
    s = std_slider.val
    order = int(order_slider.val)
    cutoff = cutoff_slider.val
    show = check.get_status()[0]

    b, a = create_filter(order, cutoff)

    if (m, s) != last_noise_params:
        noise = gen_noise(m, s)
        last_noise_params = (m, s)

    y_clean = amp * np.sin(freq * t + ph)
    y = y_clean + noise if show else y_clean
    y_filt = filter_signal(y)

    # Оновлення ліній
    line_clean.set_ydata(y_clean)
    line_noisy.set_ydata(y)
    line_filtered.set_ydata(y_filt)
    ax.relim()
    ax.autoscale_view()
    fig.canvas.draw_idle()

for widget in [amp_slider, freq_slider, phase_slider, mean_slider, std_slider, order_slider, cutoff_slider]:
    widget.on_changed(update)

check.on_clicked(update)

def reset(event):
    for s in [amp_slider, freq_slider, phase_slider, mean_slider, std_slider, order_slider, cutoff_slider]:
        s.reset()
    if not check.get_status()[0]:
        check.set_active(0)
    update(None)

reset_button.on_clicked(reset)

plt.show(block=True)

# Інструкції
# 1. Переконайтеся, що у вас встановлений бекенд TkAgg (`pip install tk`).
# 2. Запускайте скрипт як звичайний Python-файл або в інтерпритаторі Pycharm (на якому це тестувалось).
# 3. Ви побачите повноцінне вікно Matplotlib з інтерактивними слайдерами, кнопкою та чекбоксом.
# 4. Змінюйте параметри під графіком для налаштування гармоніки та шуму.
# 5. Використовуйте кнопку "Reset" для повернення до початкових налаштувань.