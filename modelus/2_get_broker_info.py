import time
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from curl_cffi import requests

from load_django import *
from parser_app.models import Listing, Broker

BASE_URL = "https://www.loopnet.com"

def get_text_or_none(tag, separator='\n'):
    if not tag:
        return None
    text = ' '.join(tag.stripped_strings)
    return text

def find_section_text(soup, heading_text):
    heading_tag = soup.find('div', class_='bd-heading', string=lambda t: t and heading_text.lower() in t.lower())
    if heading_tag:
        content_div = heading_tag.find_next_sibling('div')
        if content_div:
            return get_text_or_none(content_div, separator='\n')
    card_heading = soup.find(lambda tag: tag.name in ['h3', 'div'] and heading_text.lower() in tag.text.lower())
    if card_heading:
        card = card_heading.find_parent(class_='lnc-card')
        if card:
             return get_text_or_none(card.select_one('.bd-body, .bd-expanding-about, .bd-affiliations'))

    return None

def parse_broker_page(soup, broker_url):
    main_profile = soup.select_one('.bd-profile-main')
    if not main_profile:
        return None

    name = get_text_or_none(main_profile.select_one('h1.bd-content-highlight'))
    if not name:
        return None

    title_company_str = get_text_or_none(main_profile.select_one('h2.bd-content-title'))
    title, company_name = None, None
    if title_company_str:
        parts = [p.strip() for p in title_company_str.split(',')]
        title = parts[0]
        if len(parts) > 1:
            company_name = ', '.join(parts[1:])

    address = get_text_or_none(main_profile.select_one('div.bd-content-location'))
    
    phone, mobile = None, None
    phone_container = main_profile.select_one('.bd-contact .bd-header-modules-desktop')
    if phone_container:
        phone_tags = phone_container.select('p.bd-header-modules-desktop-all-phones')
        for p_tag in phone_tags:
            strong_tag = p_tag.find('strong')
            if strong_tag:
                label = strong_tag.text.strip().lower()
                value = get_text_or_none(p_tag, separator=' ').replace(strong_tag.text, '').strip()
                if 'phone' in label:
                    phone = value
                elif 'mobile' in label:
                    mobile = value

    bio = get_text_or_none(main_profile.select_one('#bdBio'))
    
    specialties, property_types, markets = None, None, None
    skill_items = main_profile.select('.bd-skill-item')
    for item in skill_items:
        title_tag = item.select_one('.bd-skill-title')
        content_tag = item.select_one('.bd-skill-content')
        if title_tag and content_tag:
            skill_title = get_text_or_none(title_tag).lower()
            skill_content = get_text_or_none(content_tag, separator=', ')
            if 'specialties' in skill_title:
                specialties = skill_content
            elif 'property types' in skill_title:
                property_types = skill_content
            elif 'markets' in skill_title:
                markets = skill_content

    education = find_section_text(main_profile, 'Education')
    affiliations_list = main_profile.select('#bdAffiliations ul li')
    affiliations = '\n'.join([get_text_or_none(li) for li in affiliations_list]) if affiliations_list else find_section_text(main_profile, 'Affiliations')
    awards = find_section_text(main_profile, 'Awards')

    broker_data = {
        'profile_url': broker_url, 'name': name, 'title': title, 'company_name': company_name,
        'address': address, 'phone': phone, 'mobile': mobile, 'bio': bio,
        'specialties': specialties, 'property_types': property_types, 'markets': markets,
        'education': education, 'affiliations': affiliations, 'awards': awards,
    }
    return broker_data


def parse_broker_from_listing_page(soup, listing_url):
    contact_box = soup.select_one('div.container-contact-form, div.contact-box')
    if not contact_box:
        return None

    name_tag = contact_box.select_one('li.contact:first-of-type .contact-name')
    name = get_text_or_none(name_tag)
    
    if not name:
        return None

    phone_tag = contact_box.select_one('.cta-phone-number, .broker-bio__info__phone .broker-phone')
    phone = get_text_or_none(phone_tag)
    if phone and 'Call' in phone:
        phone = phone.replace('Call', '').strip()

    company_tag = contact_box.select_one('li.contact-logo img, .broker-bio__title-wrap__logo img')
    company_name = company_tag['alt'].strip() if company_tag and company_tag.has_attr('alt') else None
    
    broker_pseudo_url = f"{listing_url}#broker={name.replace(' ', '_')}"
    
    return {
        'profile_url': broker_pseudo_url, 'name': name, 'phone': phone, 'company_name': company_name,
        'title': None, 'address': None, 'mobile': None, 'bio': None, 'specialties': None,
        'property_types': None, 'markets': None, 'education': None, 'affiliations': None, 'awards': None,
    }

def run():
    print("Этап 2: Сбор информации о брокерах.")
    
    listings_to_process = Listing.objects.filter(status='Done')
    
    if not listings_to_process.exists():
        print("Нет новых объявлений для сбора информации о брокерах (статус 'Done').")
        return

    print(f"Найдено {listings_to_process.count()} объявлений для обработки.")

    session = requests.Session(impersonate="chrome110", verify=False)
    
    processed_count = 0
    for listing in listings_to_process:
        print(f"\n[Listing] Обрабатываем: {listing.url}")
        broker_data = None
        broker_profile_url = None

        try:
            listing_response = session.get(listing.url, timeout=40)
            listing_response.raise_for_status()
            listing_soup = BeautifulSoup(listing_response.text, 'html.parser')

            selectors = [
                'section.broker-bio__wrap .broker-bio:first-of-type a.avatar-container',
                'ul#contact-form-contacts li:first-of-type a',
            ]
            first_broker_tag = None
            for selector in selectors:
                first_broker_tag = listing_soup.select_one(selector)
                if first_broker_tag and first_broker_tag.has_attr('href') and '/commercial-real-estate-brokers/profile/' in first_broker_tag['href']:
                    break
                else:
                    first_broker_tag = None

            if first_broker_tag:
                broker_profile_url = urljoin(BASE_URL, first_broker_tag['href'])
                print(f"Найден URL профиля брокера: {broker_profile_url}")

                broker_response = session.get(broker_profile_url, timeout=40)
                broker_response.raise_for_status()
                broker_soup = BeautifulSoup(broker_response.text, 'html.parser')
                broker_data = parse_broker_page(broker_soup, broker_profile_url)
            else:
                print("Ссылка на профиль не найдена, пытаемся извлечь данные со страницы.")
                broker_data = parse_broker_from_listing_page(listing_soup, listing.url)
                if broker_data:
                    broker_profile_url = broker_data['profile_url']

            if not broker_data or not broker_profile_url:
                print("Не удалось извлечь данные о брокере. Пропускаем.")
                listing.status = 'Error'
                listing.save()
                continue
            
            broker, created = Broker.objects.update_or_create(
                profile_url=broker_profile_url,
                defaults={k: v for k, v in broker_data.items() if k != 'profile_url' and v is not None}
            )
            
            listing.broker = broker
            listing.status = 'Broker Info Done'
            listing.save()
            
            processed_count += 1
            print(f"Сохранена информация для брокера: {broker.name}")

            time.sleep(2)

        except Exception as e:
            print(f" Ошибка при обработке {listing.url}: {e}")
            listing.status = 'Error'
            listing.save()
            
    print(f"\nСбор информации о брокерах завершен. Обработано записей: {processed_count}")

if __name__ == "__main__":
    run()