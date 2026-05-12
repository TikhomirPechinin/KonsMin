# ИИ-консультант профсоюза ХГУ (минимальная версия)

Простой консультант для VK, который отвечает на сообщения через YandexGPT. Без базы данных, без кнопок — только приём сообщений и ответ через нейросеть.

---

## Требования к серверу

- Ubuntu 22.04/24.04 LTS
- Python 3.11 или выше
- Доступ в интернет
- Открытый порт 8000

---

## Полная инструкция по установке и запуску

### Шаг 1. Подключись к серверу

```
ssh ваш_пользователь@IP_сервера
```
Шаг 2. Обнови систему и установи Python
```
sudo apt update
sudo apt upgrade -y
sudo apt install python3.11 python3.11-venv python3-pip -y
```
Шаг 3. Скачай проект с GitHub
```
git clone https://github.com/TikhomirPechinin/profsociety-bot-minimal.git
cd profsociety-bot-minimal
```
Шаг 4. Создай виртуальное окружение
```
python3.11 -m venv venv
source venv/bin/activate
```
Шаг 5. Установи зависимости
```
pip install -r requirements.txt
```
Шаг 6. Настрой переменные окружения
Скопируй пример конфигурации:

```
cp .env.example .env
```
Открой файл для редактирования:

```
nano .env
```
Заполни своими данными:

```
# VK
VK_ACCESS_TOKEN=ваш_токен_сообщества
CONFIRMATION_STRING=ваша_строка_подтверждения

# YandexGPT
YANDEX_FOLDER_ID=ваш_folder_id
YANDEX_API_KEY=ваш_api_ключ
```
Сохрани: Ctrl+O, Enter, Ctrl+X

Шаг 7. Настрой Callback API в VK
Зайди в управление своим сообществом ВКонтакте

Перейди в раздел Управление → Callback API

В поле «Адрес» укажи:

text
http://IP_твоего_сервера:8000/webhook
Включи событие «Входящие сообщения»

Нажми «Подтвердить»

Шаг 8. Запусти консультанта
```
python3 app.py
```
Ты увидишь:

text
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:8000
Шаг 9. Проверь работу
Напиши любое сообщение в личные сообщения сообщества. Консультант должен ответить через YandexGPT.

Как остановить консультанта
Нажми Ctrl+C в терминале.

Как запустить в фоновом режиме (чтобы не держать терминал открытым)
Через screen
```
screen -S consultant
python3 app.py
```
# Нажми Ctrl+A, затем D — выйдешь, оставив консультанта работать
Вернуться к окну:

```
screen -r consultant
```
Или через systemd
```
sudo nano /etc/systemd/system/consultant.service
```
Вставь:

ini
[Unit]
Description=Profsociety Consultant
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/profsociety-bot-minimal
ExecStart=/home/ubuntu/profsociety-bot-minimal/venv/bin/python app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
Запусти:

```
sudo systemctl daemon-reload
sudo systemctl start consultant
sudo systemctl enable consultant
sudo systemctl status consultant
```
Просмотр логов
```
# Если через screen — внутри окна
# Если через systemd
sudo journalctl -u consultant -f
```
Обновление консультанта
```
cd ~/profsociety-bot-minimal
git pull
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart consultant  # или перезапусти вручную
```