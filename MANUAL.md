# Hikka — MANUAL по установке и запуску

Полное руководство по установке, первому запуску, авторизации в Telegram и базовому использованию юзербота Hikka.

---

## Содержание

1. [Требования](#1-требования)
2. [Получение API ID и API Hash](#2-получение-api-id-и-api-hash)
3. [Установка на Linux / VPS / Termux](#3-установка-на-linux--vps--termux)
4. [Установка на Windows](#4-установка-на-windows)
5. [Первый запуск и авторизация](#5-первый-запуск-и-авторизация)
6. [Авторизация через QR-код](#6-авторизация-через-qr-код)
7. [Двухфакторная аутентификация (2FA)](#7-двухфакторная-аутентификация-2fa)
8. [Web-интерфейс настройки](#8-web-интерфейс-настройки)
9. [Базовое использование](#9-базовое-использование)
10. [Управление модулями](#10-управление-модулями)
11. [Обновление](#11-обновление)
12. [Решение проблем](#12-решение-проблем)

---

## 1. Требования

- **Python 3.8–3.12** (рекомендуется 3.12 — протестировано и поддерживается).
  - ⚠️ **Python 3.13 не поддерживается** — пакеты `aiohttp` и `tgcrypto` не собираются на нём без Visual C++ Build Tools.
  - ✅ **Python 3.12 полностью поддерживается** — код исправлен для корректной работы на Windows (кодировка UTF-8 при чтении файлов).
- **Git** — для клонирования репозитория и работы обновлятора.
- **pip** — идёт в комплекте с Python.
- Около **500 МБ** свободного места.
- Аккаунт Telegram, с которого будет работать юзербот.
- API ID и API Hash (см. [раздел 2](#2-получение-api-id-и-api-hash)).

### Системные пакеты (Linux)

```bash
sudo apt update
sudo apt install -y git python3 python3-pip python3-venv libcairo2
```

> `libcairo2` нужен для отрисовки некоторых медиа-фич (QR-коды, превью).

---

## 2. Получение API ID и API Hash

Эти ключи нужны для подключения к Telegram API.

1. Перейдите на https://my.telegram.org и войдите по номеру телефона.
2. Откройте вкладку **API development tools**.
3. Заполните форму:
   - **App title** — любое название (например, `Hikka`).
   - **Short name** — короткое имя латиницей (например, `hikka`).
   - **URL** — можно оставить пустым.
   - **Platform** — выберите `Other`.
   - **Description** — можно оставить пустым.
4. Нажмите **Create application**.
5. Скопируйте значения:
   - **App api_id** — число (например, `1234567`).
   - **App api_hash** — строка (например, `0123456789abcdef0123456789abcdef`).

> ⚠️ **Никому не передавайте эти ключи.** Они привязаны к вашему аккаунту.

---

## 3. Установка на Linux / VPS / Termux

### Вариант A — Установочный скрипт (рекомендуется)

```bash
(wget -qO- https://github.com/troy9221/Hikka/raw/master/install.sh)
```

Скрипт сам определит ОС, установит зависимости и запустит Hikka.

### Вариант B — Ручная установка

```bash
# 1. Установить системные зависимости
sudo apt update
sudo apt install -y git python3 python3-pip python3-venv libcairo2

# 2. Клонировать репозиторий
git clone https://github.com/troy9221/Hikka
cd Hikka

# 3. (Рекомендуется) Создать виртуальное окружение
python3 -m venv venv
source venv/bin/activate

# 4. Установить Python-зависимости
pip install -r requirements.txt

# 5. Запустить Hikka
python3 -m hikka
```

### Termux (Android)

```bash
pkg update
pkg install -y git python libcairo
git clone https://github.com/troy9221/Hikka
cd Hikka
pip install -r requirements.txt
python -m hikka
```

> На Termux web-интерфейс отключён автоматически — настройка идёт через консоль.

---

## 4. Установка на Windows

### Шаг 1. Установить Python

1. Скачайте **Python 3.12** с https://www.python.org/downloads/
   - ✅ Python 3.12 протестирован и полностью поддерживается.
   - ⚠️ Не используйте Python 3.13.
2. При установке отметьте галочку **«Add Python to PATH»**.

### Шаг 2. Установить Git

1. Скачайте с https://git-scm.com/download/win и установите.

### Шаг 3. Клонировать и установить

Откройте **Командную строку** (cmd) или **PowerShell**:

```bat
git clone https://github.com/troy9221/Hikka
cd Hikka
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

> `tgcrypto` (опциональное C-расширение для ускорения криптографии) исключён из
> обязательных зависимостей, т.к. не имеет готовых wheels для Windows.
> Hikka работает и без него (чуть медленнее). На Linux можно установить отдельно:
> `pip install tgcrypto`
>
> Если всё же возникает ошибка сборки `aiohttp` — установите
> [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
> (компонент «Desktop development with C++»).

### Шаг 4. Запуск

```bat
python -m hikka
```

---

## 5. Первый запуск и авторизация

После запуска `python -m hikka` (или `python3 -m hikka` на Linux) начнётся процесс настройки.

### Шаг 1. Ввод API ID и API Hash

Если вы не задали ключи заранее, Hikka предложит их ввести:

```
Enter API ID: 1234567
Enter API Hash: 0123456789abcdef0123456789abcdef
```

Ключи сохраняются в `config.json` и больше запрашиваться не будут.

> **Альтернатива — переменные окружения:**
> ```bash
> # Linux/macOS
> export api_id=1234567
> export api_hash=0123456789abcdef0123456789abcdef
> python3 -m hikka
> ```
> ```bat
> :: Windows cmd
> set api_id=1234567
> set api_hash=0123456789abcdef0123456789abcdef
> python -m hikka
> ```

### Шаг 2. Ввод номера телефона

```
Enter phone: +79991234567
```

Введите номер в международном формате **с плюсом и кодом страны**.

### Шаг 3. Ввод кода подтверждения

На ваш аккаунт Telegram придёт код:

```
Enter code: 12345
```

Введите его. **Не сообщайте этот код никому.**

### Шаг 4. Завершение авторизации

После успешного входа вы увидите баннер запуска и сообщение:

```
🌘 Hikka 1.6.3 started!
```

Сессия сохраняется в файл `hikka-<номер>.session`. При следующих запусках повторный ввод не потребуется.

---

## 6. Авторизация через QR-код

Вместо ввода номера можно отсканировать QR-код с другого устройства, где уже выполнен вход в Telegram.

1. Запустите Hikka.
2. На вопрос `Use QR code? [y/N]:` введите `y`.
3. В терминале появится QR-код (ASCII).
4. Откройте Telegram на телефоне → **Настройки → Устройства → Подключить устройство**.
5. Наведите камеру на QR-код в терминале.
6. Подтвердите вход на телефоне.

> QR-логин работает только если сканировать с другого устройства. На том же устройстве, где запущен терминал, это не сработает.

---

## 7. Двухфакторная аутентификация (2FA)

Если на аккаунте включён облачный пароль (2FA), после ввода кода Hikka запросит:

```
Enter 2FA password (подсказка): ********
```

Введите ваш облачный пароль. Если подсказка есть, она будет показана в скобках.

---

## 8. Web-интерфейс настройки

На VPS/VDS (не Termux) Hikka по умолчанию запускает web-интерфейс для первичной настройки.

### Обычный запуск

```bash
python3 -m hikka
```

Web-интерфейс откроется на порту `8080`. Если вы подключены по SSH, Hikka создаст туннель и выведет ссылку вида:

```
http://localhost:8080
```

### Запуск с пробросом порта (VPS/VDS)

```bash
python3 -m hikka --proxy-pass
```

Hikka откроет SSH-туннель, чтобы вы могли открыть web-интерфейс локально.

### Отключение web-интерфейса

```bash
python3 -m hikka --no-web
```

Настройка полностью пройдёт в консоли.

### Указание своего порта

```bash
python3 -m hikka --port 9090
```

---

## 9. Базовое использование

После запуска Hikka работает как юзербот — команды отправляются прямо в любой чат (Saved Messages, личный диалог с собой и т.д.).

### Префикс команд

По умолчанию используется префикс `.` (точка). Например:

```
.ping
```

Изменить префикс:
```
.cfg prefix !
```

### Полезные команды

| Команда | Описание |
|---------|----------|
| `.ping` | Проверить, что юзербот работает (показывает пинг) |
| `.help` | Список всех загруженных модулей и команд |
| `.help <модуль>` | Подробная справка по конкретному модулю |
| `.hikka` | Информация о версии юзербота |
| `.restart` | Перезапустить юзербот |
| `.restart -sb` | Перезапуск в безопасном режиме (без сторонних модулей) |
| `.cfg <параметр> <значение>` | Изменить настройку |
| `.load <ссылка>` | Загрузить сторонний модуль |
| `.dl` | Список загруженных модулей |
| `.clear-db` | Очистить базу данных (⚠️ осторожно) |

### Пример

Отправьте в Saved Messages:
```
.ping
```
Hikka ответит сообщением с пингом — значит, всё работает.

---

## 10. Управление модулями

Hikka поддерживает загрузку сторонних модулей.

### Загрузить модуль

```
.load https://example.com/module.py
```

### Список модулей

```
.dl
```

### Репозиторий модулей

По умолчанию используется `https://github.com/anon97945/hikka-mods/raw/master`. Изменить:

```
.cfg repo https://ваш-репозиторий-модулей
```

Дополнительные репозитории (по умолчанию):

- `https://github.com/hikariatama/host/raw/master`
- `https://github.com/MoriSummerz/ftg-mods/raw/main`
- `https://gitlab.com/CakesTwix/friendly-userbot-modules/-/raw/master`
- `https://github.com/Den4ikSuperOstryyPer4ik/Astro-modules/raw/main`
- `https://github.com/idiotcoders/idiotmodules/raw/main`

Добавить свой репозиторий:

```
.addrepo https://github.com/ваш-репозиторий/raw/ветка
```

Удалить репозиторий:

```
.delrepo https://github.com/ваш-репозиторий/raw/ветка
```

### Безопасный режим

Если после установки модуля юзербот сломался:

```
.restart -sb
```

В безопасном режиме сторонние модули не загружаются, и вы можете удалить проблемный:

```
.unload <имя_модуля>
```

---

## 11. Обновление

### Через команду (рекомендуется)

```
.update
```

Hikka загрузит изменения из репозитория `https://github.com/troy9221/Hikka` (настраивается через `GIT_ORIGIN_URL`) и перезапустится.

### Через git вручную

```bash
cd Hikka
git pull
pip install -r requirements.txt
python3 -m hikka
```

### Изменение источника обновлений

```
.cfg GIT_ORIGIN_URL https://github.com/troy9221/Hikka
```

---

## 12. Решение проблем

### «ERROR: Could not open requirements file: [Errno 2] No such file or directory: 'requirements.txt'»

Команда `pip install -r requirements.txt` запущена не из директории репозитория. Сначала перейдите в папку с клонированным репозиторием:

```bash
cd Hikka
pip install -r requirements.txt
```

Если репозиторий ещё не клонирован — клонируйте его:

```bash
git clone https://github.com/troy9221/Hikka
cd Hikka
pip install -r requirements.txt
```

### «Microsoft Visual C++ 14.0 or greater is required» (Windows)

Пакет `aiohttp` (если pip решил собрать его из исходников) требует компиляции. Решения:
1. Используйте **Python 3.12** — для него есть готовые wheels `aiohttp` (версия 3.9.1+).
2. Либо установите [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) (компонент «Desktop development with C++»).

> `tgcrypto` исключён из обязательных зависимостей — он не имеет wheels для Windows.
> Hikka работает без него. На Linux: `pip install tgcrypto`.

### «You attempted to run Hikka on behalf of root user»

Hikka не разрешает запуск от root. Создайте отдельного пользователя:

```bash
sudo adduser hikka
sudo su - hikka
cd /path/to/Hikka
python3 -m hikka
```

Или запустите с флагом `--root` (не рекомендуется):

```bash
python3 -m hikka --root
```

### «Python was not found» (Windows)

Python не добавлен в PATH. Переустановите Python, отметив **«Add Python to PATH»**, либо используйте `py` launcher:

```bat
py -m hikka
```

### Сессия потеряна / нужно перелогиниться

Удалите файл сессии и запустите заново:

```bash
rm hikka-*.session
python3 -m hikka
```

### «Address already in use» / порт занят

Другой процесс Hikka уже запущен и занимает порт web-сервера. Найдите и завершите его:

```bash
# Linux — найти процесс, занимающий порт
fuser -k 49982/tcp
# или
lsof -t -i:49982 | xargs kill
```

```bat
:: Windows — найти процесс по порту
netstat -ano | findstr :49982
taskkill /PID <найденный_PID> /F
```

### FloodWait / временная блокировка

Telegram ограничивает частоту запросов. Подождите указанное время и повторите. Не спамьте команды.

### Юзербот не отвечает на команды

1. Проверьте, что процесс запущен: в терминале должно быть сообщение `Hikka started!`.
2. Проверьте префикс: `.ping` (точка).
3. Перезапустите в безопасном режиме: `.restart -sb`.
4. Проверьте логи в файле `hikka.log`.

### Очистка базы данных (полный сброс)

```
.clear-db
```

⚠️ Это удалит все настройки и данные модулей. Подтвердите действие.

---

## Полезные ссылки

- **Репозиторий:** https://github.com/troy9221/Hikka
- **Лицензия:** AGPLv3
- **Поддержка:** https://t.me/hikka_talks

---

## Краткая шпаргалка

```bash
# Установка (Linux)
git clone https://github.com/troy9221/Hikka && cd Hikka
pip install -r requirements.txt
python3 -m hikka

# Запуск
python3 -m hikka

# Запуск без web (консольная настройка)
python3 -m hikka --no-web

# Запуск с пробросом порта (VPS)
python3 -m hikka --proxy-pass

# Проверка работы (в любом чате Telegram)
.ping
```
