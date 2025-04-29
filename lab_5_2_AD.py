import numpy as np
from scipy.signal import iirfilter, filtfilt
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

t = np.linspace(0, 2 * np.pi, 1000)

def gen_noise(mean, std):
    return np.random.normal(mean, std, size=t.shape)

# Butterworth-фільтр
def create_filter(order, cutoff):
    b, a = iirfilter(order, cutoff, btype='low', ftype='butter')
    return b, a

def filter_signal(x, b, a):
    return filtfilt(b, a, x)

# Ковзне середнє (власна реалізація)
def my_moving_average(x, window_size=5):
    result = np.zeros_like(x)
    half = window_size // 2
    for i in range(len(x)):
        start = max(0, i - half)
        end = min(len(x), i + half + 1)
        result[i] = np.mean(x[start:end])
    return result

app = dash.Dash(__name__)
app.title = "Lab 5.2 — Інтерактивна фільтрація"

app.layout = html.Div([
    html.H2("Інтерактивна гармоніка з шумом та фільтрацією"),

    html.Div([
        dcc.Graph(id='clean-graph', style={'width': '32%', 'display': 'inline-block'}),
        dcc.Graph(id='noisy-graph', style={'width': '32%', 'display': 'inline-block'}),
        dcc.Graph(id='filtered-graph', style={'width': '32%', 'display': 'inline-block'}),
    ]),

    html.Div([
        html.Label("Тип гармоніки"),
        dcc.Dropdown(
            id='waveform',
            options=[
                {'label': 'Синус', 'value': 'sin'},
                {'label': 'Косинус', 'value': 'cos'}
            ],
            value='sin'
        ),

        html.Label("Тип фільтра"),
        dcc.Dropdown(
            id='filter_type',
            options=[
                {'label': 'Butterworth', 'value': 'butter'},
                {'label': 'Ковзне середнє', 'value': 'moving_avg'}
            ],
            value='butter'
        ),

        html.Label("Амплітуда"),
        dcc.Slider(0.1, 5.0, 0.1, id='amp', value=1.0, marks={i: str(i) for i in range(1, 6)}, tooltip={"placement": "bottom"}),

        html.Label("Частота"),
        dcc.Slider(0.1, 10.0, 0.1, id='freq', value=1.0, marks={i: str(i) for i in range(1, 11)}, tooltip={"placement": "bottom"}),

        html.Label("Фаза"),
        dcc.Slider(0, 2*np.pi, 0.1, id='phase', value=0.0,  marks={0: '0', 3.14: 'π', round(2*np.pi, 2): '2π'}, tooltip={"placement": "bottom"}),

        html.Label("Шум (μ)"),
        dcc.Slider(
            -1.0, 1.0, 0.05, id='noise_mean', value=0.0,
            marks={-1: '-1', 0: '0', 1: '1'}
        ),

        html.Label("Шум (σ)"),
        dcc.Slider(
            0.01, 1.0, 0.01, id='noise_std', value=0.1,
            marks={0.01: '0.01', 0.5: '0.5', 1.0: '1.0'}
        ),

        html.Label("Порядок фільтра (або ширина вікна)"),
        dcc.Slider(
            1, 10, 1, id='order', value=4,
            marks={i: str(i) for i in range(1, 11)}
        ),

        html.Label("Cutoff (лише для Butterworth)"),
        dcc.Slider(
            0.01, 0.5, 0.01, id='cutoff', value=0.05,
            marks={0.01: '0.01', 0.25: '0.25', 0.5: '0.5'}
        ),
    ], style={'padding': 20, 'width': '60%'})
])

@app.callback(
    [Output('clean-graph', 'figure'),
     Output('noisy-graph', 'figure'),
     Output('filtered-graph', 'figure')],
    Input('waveform', 'value'),
    Input('amp', 'value'),
    Input('freq', 'value'),
    Input('phase', 'value'),
    Input('noise_mean', 'value'),
    Input('noise_std', 'value'),
    Input('order', 'value'),
    Input('cutoff', 'value'),
    Input('filter_type', 'value'),
)
def update_plot(waveform, amp, freq, phase, noise_mean, noise_std, order, cutoff, filter_type):
    noise = gen_noise(noise_mean, noise_std)
    y_clean = amp * (np.sin(freq * t + phase) if waveform == 'sin' else np.cos(freq * t + phase))
    y_noisy = y_clean + noise

    if filter_type == 'butter':
        b, a = create_filter(int(order), cutoff)
        y_filtered = filter_signal(y_noisy, b, a)
    elif filter_type == 'moving_avg':
        window = int(order) * 2 + 1
        y_filtered = my_moving_average(y_noisy, window_size=window)
    else:
        y_filtered = y_noisy

    def make_fig(y, title):
        return {
            'data': [{'x': t, 'y': y, 'type': 'line', 'name': title}],
            'layout': {'title': title, 'margin': {'l': 40, 'r': 10, 't': 40, 'b': 30}}
        }

    return make_fig(y_clean, "Чистий сигнал"), make_fig(y_noisy, "Зашумлений сигнал"), make_fig(y_filtered, "Фільтрований сигнал")

if __name__ == '__main__':
    app.run(debug=True)
