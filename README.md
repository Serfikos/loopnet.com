[English](#english) | [Русский](#russian)

<a name="english"></a>
# LoopNet Scraper Project

This project is a high-performance web scraping application built with Python and Django. It is designed to extract commercial real estate listings and detailed broker information from `LoopNet.com`. Unlike traditional Selenium-based scrapers, this project utilizes `curl_cffi` to impersonate real browser TLS fingerprints, making it faster and more stealthy against bot protections.

## Features

*   **Listings Scraping:** Collects commercial real estate listings including titles, URLs, and agency names.
*   **Broker Scraping:** Extracts detailed broker profiles including names, phone numbers, emails, bios, awards, specialties, and transaction history.
*   **Smart Detection:** Can parse broker details directly from listing pages or follow links to dedicated broker profile pages.
*   **Database Integration:** Uses Django ORM with PostgreSQL to store structured data (`Listing` and `Broker` models).
*   **High Performance:** Uses `curl_cffi` for fast HTTP requests with browser impersonation (`chrome110`), avoiding the overhead of a full browser instance.
*   **Workflow Management:** Tracks the status of listings (`New`, `Done`, `Broker Info Done`, `Error`) to manage the scraping pipeline efficiently.

## Tech Stack

*   **Python 3.8+**
*   **Django** (ORM & Admin Interface)
*   **curl_cffi** (HTTP Client with TLS fingerprinting)
*   **BeautifulSoup4** (HTML Parsing)
*   **PostgreSQL** (Database)

## Prerequisites

1.  Python 3.8 or higher.
2.  PostgreSQL installed and running.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd <repository_folder>
    ```

2.  **Set up a Virtual Environment:**
    ```bash
    python -m venv venv
    
    # Windows
    venv\Scripts\activate
    
    # Mac/Linux
    source venv/bin/activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install django psycopg2-binary curl_cffi beautifulsoup4
    ```

4.  **Database Configuration:**
    Open `loopnet_project/settings.py` and configure the `DATABASES` dictionary.
    
    Default configuration:
    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'loopnet_db',
            'USER': 'loopnet_user', # Update with your postgres user
            'PASSWORD': '111',      # Update with your password
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
    ```
    *Ensure you create the database (e.g., `loopnet_db`) in PostgreSQL before proceeding.*

5.  **Apply Migrations:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

## Usage

The scraping process is divided into two main stages.

### 1. Scrape Listings
Run the script to iterate through LoopNet search pages and collect listing URLs.
*(Assuming the file is named `scrape_listings.py` based on the provided code)*
```bash
python scrape_listings.py
```
*   This script iterates through search results.
*   It saves listings to the database with status `Done`.
*   It stops automatically when no more listings are found.

### 2. Scrape Broker Details
Run the script to process collected listings and extract broker information.
*(Assuming the file is named `scrape_brokers.py` based on the provided code)*
```bash
python scrape_brokers.py
```
*   This script looks for listings with status `Done`.
*   It visits each listing URL to find broker contacts.
*   If a broker profile link is found, it visits that profile to scrape deep details (Bio, Awards, Education).
*   If no profile link is found, it attempts to parse contact info directly from the listing page.
*   Upon success, updates listing status to `Broker Info Done`.

## Project Structure

*   `manage.py`: Django's command-line utility.
*   `loopnet_project/`: Project settings.
*   `parser_app/`: Django app containing models (`Listing`, `Broker`) and Admin config.
*   `scrape_listings.py`: Script to harvest listing URLs.
*   `scrape_brokers.py`: Script to enrich listings with broker data.
*   `load_django.py`: Utility to initialize Django context for standalone scripts.

---

<a name="russian"></a>
# Проект парсера LoopNet

Это высокопроизводительное приложение для веб-скрапинга, созданное на Python и Django. Проект предназначен для извлечения объявлений о коммерческой недвижимости и детальной информации о брокерах с сайта `LoopNet.com`. В отличие от традиционных парсеров на базе Selenium, этот проект использует `curl_cffi` для имитации TLS-отпечатков реального браузера, что делает его более быстрым и незаметным для защиты от ботов.

## Возможности

*   **Парсинг объявлений:** Сбор объявлений о коммерческой недвижимости, включая заголовки, URL-адреса и названия агентств.
*   **Парсинг брокеров:** Извлечение детальных профилей брокеров, включая имена, телефоны, email, биографии, награды, специализации и историю сделок.
*   **Умное обнаружение:** Умеет парсить данные брокера напрямую со страницы объявления или переходить по ссылкам на специализированные страницы профилей.
*   **Интеграция с базой данных:** Использование Django ORM с PostgreSQL для хранения структурированных данных (модели `Listing` и `Broker`).
*   **Высокая производительность:** Использует `curl_cffi` для быстрых HTTP-запросов с имитацией браузера (`chrome110`), избегая накладных расходов на запуск полноценного браузера.
*   **Управление процессом:** Отслеживает статус объявлений (`New`, `Done`, `Broker Info Done`, `Error`) для эффективного управления конвейером сбора данных.

## Технологический стек

*   **Python 3.8+**
*   **Django** (ORM и админ-панель)
*   **curl_cffi** (HTTP-клиент с поддержкой TLS-имперсонации)
*   **BeautifulSoup4** (Парсинг HTML)
*   **PostgreSQL** (База данных)

## Предварительные требования

1.  Установлен Python 3.8 или выше.
2.  Установлен и запущен PostgreSQL.

## Установка

1.  **Клонирование репозитория:**
    ```bash
    git clone <repository_url>
    cd <repository_folder>
    ```

2.  **Создание виртуального окружения:**
    ```bash
    python -m venv venv
    
    # Windows
    venv\Scripts\activate
    
    # Mac/Linux
    source venv/bin/activate
    ```

3.  **Установка зависимостей:**
    ```bash
    pip install django psycopg2-binary curl_cffi beautifulsoup4
    ```

4.  **Настройка базы данных:**
    Откройте `loopnet_project/settings.py` и настройте словарь `DATABASES`.
    
    Конфигурация по умолчанию:
    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'loopnet_db',
            'USER': 'loopnet_user', # Укажите вашего пользователя postgres
            'PASSWORD': '111',      # Укажите ваш пароль
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
    ```
    *Перед продолжением убедитесь, что база данных (например, `loopnet_db`) создана в PostgreSQL.*

5.  **Применение миграций:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

## Использование

Процесс парсинга разделен на два основных этапа.

### 1. Сбор объявлений (Listings)
Запустите скрипт для обхода страниц поиска LoopNet и сбора URL-адресов объявлений.
*(Предполагается, что файл называется `scrape_listings.py` на основе предоставленного кода)*
```bash
python scrape_listings.py
```
*   Скрипт перебирает результаты поиска.
*   Сохраняет объявления в базу данных со статусом `Done`.
*   Автоматически останавливается, когда объявления заканчиваются.

### 2. Сбор данных о брокерах
Запустите скрипт для обработки собранных объявлений и извлечения информации о брокерах.
*(Предполагается, что файл называется `scrape_brokers.py` на основе предоставленного кода)*
```bash
python scrape_brokers.py
```
*   Скрипт ищет объявления со статусом `Done`.
*   Посещает каждый URL объявления для поиска контактов брокера.
*   Если найдена ссылка на профиль брокера, переходит по ней для сбора глубоких данных (Биография, Награды, Образование).
*   Если ссылка на профиль не найдена, пытается извлечь контактную информацию непосредственно со страницы объявления.
*   При успехе обновляет статус объявления на `Broker Info Done`.

## Структура проекта

*   `manage.py`: Утилита командной строки Django.
*   `loopnet_project/`: Настройки проекта.
*   `parser_app/`: Приложение Django, содержащее модели (`Listing`, `Broker`) и настройки админки.
*   `scrape_listings.py`: Скрипт для сбора URL-адресов объявлений.
*   `scrape_brokers.py`: Скрипт для обогащения объявлений данными о брокерах.
*   `load_django.py`: Утилита для инициализации контекста Django для автономных скриптов.
