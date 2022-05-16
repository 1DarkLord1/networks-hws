import PySimpleGUI as sg

from constants import TEXT_SIZE, INPUT_FIELD_SIZE

client_layout = [
    [
        sg.Text('Введите IP адрес получателя:', size=(TEXT_SIZE, 1)),
        sg.InputText(enable_events=True, key='-IP-', size=(INPUT_FIELD_SIZE, 1)),
    ],
    [
        sg.Text('Введите порт отправки:', size=(TEXT_SIZE, 1)),
        sg.InputText(enable_events=True, key='-PORT-', size=(INPUT_FIELD_SIZE, 1)),
    ],
    [
        sg.Text('Введите число пакетов для отправки:', size=(TEXT_SIZE, 1)),
        sg.InputText(enable_events=True, key='-PKT NUM-', size=(INPUT_FIELD_SIZE, 1)),
    ],
    [sg.Button('Отправить', key='-SEND-')],
]

server_layout = [
    [
        sg.Text('Введите IP для получения:', size=(TEXT_SIZE, 1)),
        sg.InputText(enable_events=True, key='-IP-', size=(INPUT_FIELD_SIZE, 1)),
    ],
    [
        sg.Text('Введите порт получения:', size=(TEXT_SIZE, 1)),
        sg.InputText(enable_events=True, key='-PORT-', size=(INPUT_FIELD_SIZE, 1)),
    ],
    [
        sg.Text('Число полученных пакетов:', size=(TEXT_SIZE, 1)),
        sg.Text('', size=(TEXT_SIZE, 1), key='-PKT RECEIVED-'),
    ],
    [
        sg.Text('Скорость соединения:', size=(TEXT_SIZE, 1)),
        sg.Text('', size=(TEXT_SIZE, 1), key='-SPEED-'),
    ],
    [sg.Button('Установить адрес', key='-ADDR-')],
    [sg.Button('Получить', key='-RECEIVE-')],
]
