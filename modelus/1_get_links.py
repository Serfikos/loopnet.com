from load_django import *
from parser_app.models import Listing
from curl_cffi import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

BASE_URL = "https://www.loopnet.com/search/commercial-real-estate/for-sale/"
# LISTINGS_LIMIT = 100 # --- Лимит убран для полного сбора

def run_scraper():
    print("Начинаем полный сбор данных с LoopNet. Цель: ВСЕ доступные объявления.")
    
    session = requests.Session(impersonate="chrome110", verify=False)
    
    newly_added_count = 0
    page = 1

    # --- Цикл изменен на while True, он будет прерван, когда закончатся объявления ---
    while True:
        params = {
            'sk': '42a92858e0dde51e147630da224d069b',
            'bb': 'ymjozigmnXwgo2hizttpB',
            'page': page
        }
        
        print(f"Обрабатываем страницу {page}...")
        
        try:
            response = session.get(BASE_URL, params=params, timeout=40)
            
            if response.status_code != 200:
                print(f"Сайт вернул статус {response.status_code}. Остановка.")
                break
            
            soup = BeautifulSoup(response.text, 'html.parser')
            placards = soup.find_all('article', class_='placard')

            # --- Это условие остановит цикл, когда страницы закончатся ---
            if not placards:
                print("Больше объявлений не найдено на странице. Завершаем работу.")
                break

            for placard in placards:
                # Название и URL объявления
                title_tag = placard.find('a', class_='placard-title')
                if not title_tag:
                    header_h4 = placard.find('h4')
                    title_tag = header_h4.find('a') if header_h4 else None

                if not (title_tag and title_tag.has_attr('href')):
                    continue
                
                title = title_tag.text.strip()
                listing_url = urljoin(BASE_URL, title_tag['href'])

                # Агентство
                agency_name = "Название не найдено"
                agency_url = None
                agency_link_tag = placard.find('a', class_='listing-company')
                if agency_link_tag and agency_link_tag.has_attr('href'):
                    agency_url = agency_link_tag['href']
                contacts_list = placard.find('ul', class_='contacts')
                if contacts_list:
                    company_li = contacts_list.find('li', title=True, class_=lambda c: c != 'tenx-logo' if c else True)
                    if company_li and company_li.get('title'):
                        agency_name = company_li['title'].strip()
                    else:
                        contact_logo_li = contacts_list.find('li', class_='contact-logo')
                        if contact_logo_li:
                            img_tag = contact_logo_li.find('img', alt=True)
                            if img_tag and img_tag.get('alt'):
                                agency_name = img_tag['alt'].strip()
                if agency_name == "Название не найдено" and agency_link_tag:
                    if agency_link_tag.has_attr('title') and agency_link_tag['title']:
                        agency_name = agency_link_tag['title'].strip()
                    elif agency_link_tag.find('img') and agency_link_tag.find('img').get('alt'):
                        agency_name = agency_link_tag.find('img')['alt'].strip()

                #Сохраняем или обновляем в базе данных
                obj, created = Listing.objects.update_or_create(
                    url=listing_url,
                    defaults={
                        'title': title,
                        'agency_name': agency_name,
                        'agency_url': agency_url,
                        'status': 'Done'  
                    }
                )
                
                if created:
                    newly_added_count += 1
                    # --- Обновлен текст вывода, т.к. нет общего лимита ---
                    print(f"Добавлено (новых за сессию: {newly_added_count}): {title} | Агентство: {agency_name}")
            
            page += 1
            time.sleep(2)

        except Exception as e:
            print(f"Сбой на странице {page}: {e}")
            print("Прерываем сбор.")
            break
            
    print(f"\nСбор завершен. Всего добавлено новых записей в этой сессии: {newly_added_count}")

if __name__ == "__main__":
    run_scraper()