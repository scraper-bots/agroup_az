# -*- coding: utf-8 -*-
"""
Aptekonline.az Pharmacy Scraper
Scrapes all pharmacy data from https://aptekonline.az/pharmacies
"""

import sys
import io
import requests
import urllib3
import re
import csv
import json
import time
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configuration
BASE_URL = "https://aptekonline.az"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
}
TIMEOUT = 30
MAX_WORKERS = 5
DELAY_BETWEEN_REQUESTS = 0.5


def get_session():
    """Create a requests session."""
    session = requests.Session()
    session.headers.update(HEADERS)
    return session


def get_pharmacy_ids(session):
    """Extract all pharmacy IDs and basic info from the main pharmacies page."""
    url = f"{BASE_URL}/pharmacies"

    print(f"Fetching pharmacy list from {url}...")
    response = session.get(url, timeout=TIMEOUT, verify=False)
    response.encoding = 'utf-8'

    if response.status_code != 200:
        raise Exception(f"Failed to fetch pharmacy list: {response.status_code}")

    # Find JSON array with pharmacy data embedded in the page
    json_match = re.search(r'\[{"id":\d+,"thumbImg"[^\]]+\]', response.text)

    if not json_match:
        raise Exception("Could not find pharmacy data in page")

    pharmacies_basic = json.loads(json_match.group(0))
    print(f"Found {len(pharmacies_basic)} pharmacies")

    return pharmacies_basic


def scrape_pharmacy_page(session, pharmacy_id):
    """Scrape ALL available information from an individual pharmacy page."""
    url = f"{BASE_URL}/pharmacies/{pharmacy_id}"

    try:
        response = session.get(url, timeout=TIMEOUT, verify=False)
        response.encoding = 'utf-8'

        if response.status_code != 200:
            return {'id': pharmacy_id, 'error': f"HTTP {response.status_code}"}

        text = response.text
        soup = BeautifulSoup(text, 'lxml')

        data = {'id': pharmacy_id}

        # 1. Extract pharmacy name from title
        title = soup.find('title')
        if title:
            title_text = title.text.strip()
            name_match = re.match(r'(.+?)\s*Aptekonline', title_text)
            data['name'] = name_match.group(1).strip() if name_match else title_text.split('Aptekonline')[0].strip()

        # 2. Extract meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        data['description'] = meta_desc.get('content', '').strip() if meta_desc else ''

        # 3. Extract region from card-header
        card_header = soup.find('div', class_='card-header')
        data['region'] = card_header.get_text(strip=True) if card_header else ''

        # 4. Extract address from contact-aptek (fa-map-marker)
        contact_div = soup.find('div', class_='contact-aptek')
        if contact_div:
            # Address - look for fa-map-marker icon
            address_p = contact_div.find('i', class_='fa-map-marker')
            if address_p and address_p.parent:
                data['address'] = address_p.parent.get_text(strip=True)
            else:
                # Fallback: first p tag
                first_p = contact_div.find('p')
                data['address'] = first_p.get_text(strip=True) if first_p else ''

            # Phone from contact-aptek (fa-phone)
            phone_i = contact_div.find('i', class_='fa-phone')
            if phone_i and phone_i.parent:
                data['contact_phone'] = phone_i.parent.get_text(strip=True)
            else:
                data['contact_phone'] = ''

            # Check for Optika text in page
            optika_i = contact_div.find('i', class_='fa-eye')
            data['has_optika_service'] = '1' if optika_i else '0'
        else:
            data['address'] = ''
            data['contact_phone'] = ''
            data['has_optika_service'] = '0'

        # 5. Extract coordinates from initMapPharmacies function
        map_coords = re.search(
            r'initMapPharmacies[^{]+{[^}]*lat:\s*\(?([0-9.]+)\)?[^}]*lng:\s*\(?([0-9.]+)\)?',
            text, re.DOTALL
        )
        if map_coords:
            data['latitude'] = map_coords.group(1)
            data['longitude'] = map_coords.group(2)
        else:
            data['latitude'] = ''
            data['longitude'] = ''

        # 6. Extract pharmacy image URL
        aptek_div = soup.find('div', class_='aptek-pinto')
        if aptek_div:
            img = aptek_div.find('img', class_='img-fluid')
            data['image_url'] = img.get('src', '') if img else ''
        else:
            data['image_url'] = ''

        # 7. Extract all phone numbers from tel: links
        tel_links = soup.find_all('a', href=re.compile(r'^tel:'))
        phones = list(set([a.get('href', '').replace('tel:', '') for a in tel_links]))
        data['all_phones'] = '; '.join(phones) if phones else ''

        # 8. Extract insurance partners
        insurance_section = soup.find('section', class_='partniyor')
        if insurance_section:
            insurance_imgs = insurance_section.find_all('img', title=True)
            insurances = [img.get('title', '') for img in insurance_imgs if img.get('title')]
            data['insurance_partners'] = '; '.join(insurances) if insurances else ''
        else:
            data['insurance_partners'] = ''

        # 9. Extract gallery images
        gallery_div = soup.find('div', class_='tab-gallery')
        if gallery_div:
            gallery_imgs = gallery_div.find_all('img', src=True)
            gallery_urls = [img.get('src', '') for img in gallery_imgs if img.get('src')]
            data['gallery_images'] = '; '.join(gallery_urls) if gallery_urls else ''
            data['gallery_count'] = str(len(gallery_urls))
        else:
            data['gallery_images'] = ''
            data['gallery_count'] = '0'

        # 10. Generate Google Maps URL
        if data['latitude'] and data['longitude']:
            data['google_maps_url'] = f"https://www.google.com/maps?q={data['latitude']},{data['longitude']}"
        else:
            data['google_maps_url'] = ''

        data['page_url'] = url

        return data

    except Exception as e:
        return {'id': pharmacy_id, 'error': str(e)}


def scrape_all_pharmacies(pharmacy_list, max_workers=MAX_WORKERS):
    """Scrape all pharmacy pages with concurrent requests."""
    session = get_session()
    results = []
    errors = []

    total = len(pharmacy_list)
    print(f"\nScraping {total} pharmacy pages...")

    # Create lookup for basic info from main page
    basic_info = {p['id']: p for p in pharmacy_list}

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_id = {
            executor.submit(scrape_pharmacy_page, session, p['id']): p['id']
            for p in pharmacy_list
        }

        completed = 0
        for future in as_completed(future_to_id):
            completed += 1
            pharmacy_id = future_to_id[future]

            try:
                result = future.result()

                if 'error' in result:
                    errors.append(result)
                    print(f"  [{completed}/{total}] Error scraping pharmacy {pharmacy_id}: {result['error']}")
                else:
                    # Merge with basic info from main page
                    basic = basic_info.get(pharmacy_id, {})
                    result['thumb_image'] = basic.get('thumbImg', '')
                    result['pharmacy_name_main'] = basic.get('pharmacyName', '')
                    result['pharmacy_tel'] = basic.get('pharmacyTel', '')
                    result['pharmacy_mob'] = basic.get('pharmacyMob', '')
                    result['is_duty_24h'] = str(basic.get('isduty', ''))
                    result['has_optika'] = str(basic.get('optika', ''))

                    results.append(result)
                    print(f"  [{completed}/{total}] Scraped: {result.get('name', 'Unknown')[:40]}")

            except Exception as e:
                errors.append({'id': pharmacy_id, 'error': str(e)})
                print(f"  [{completed}/{total}] Exception for pharmacy {pharmacy_id}: {e}")

            time.sleep(DELAY_BETWEEN_REQUESTS)

    return results, errors


def save_to_csv(data, filename='aptekonline.csv'):
    """Save scraped data to CSV file."""
    if not data:
        print("No data to save!")
        return

    # Define column order - ALL columns
    columns = [
        'id',
        'name',
        'pharmacy_name_main',
        'description',
        'region',
        'address',
        'latitude',
        'longitude',
        'contact_phone',
        'pharmacy_tel',
        'pharmacy_mob',
        'all_phones',
        'is_duty_24h',
        'has_optika',
        'has_optika_service',
        'insurance_partners',
        'image_url',
        'thumb_image',
        'gallery_images',
        'gallery_count',
        'google_maps_url',
        'page_url'
    ]

    with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=columns, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(data)

    print(f"\nSaved {len(data)} pharmacies to {filename}")


def main():
    """Main function to run the scraper."""
    print("=" * 60)
    print("Aptekonline.az Pharmacy Scraper - Full Data Extraction")
    print("=" * 60)

    session = get_session()

    # Step 1: Get all pharmacy IDs
    pharmacy_list = get_pharmacy_ids(session)

    # Step 2: Scrape each pharmacy page
    results, errors = scrape_all_pharmacies(pharmacy_list)

    # Step 3: Save results
    save_to_csv(results, 'aptekonline.csv')

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total pharmacies found: {len(pharmacy_list)}")
    print(f"Successfully scraped: {len(results)}")
    print(f"Errors: {len(errors)}")

    if errors:
        print("\nPharmacies with errors:")
        for err in errors[:10]:
            print(f"  - ID {err['id']}: {err.get('error', 'Unknown error')}")
        if len(errors) > 10:
            print(f"  ... and {len(errors) - 10} more")

    # Statistics
    if results:
        with_coords = sum(1 for r in results if r.get('latitude'))
        with_address = sum(1 for r in results if r.get('address'))
        on_duty = sum(1 for r in results if r.get('is_duty_24h') == '1')
        with_optika = sum(1 for r in results if r.get('has_optika') == '1')
        with_insurance = sum(1 for r in results if r.get('insurance_partners'))
        with_gallery = sum(1 for r in results if int(r.get('gallery_count', 0)) > 0)

        print(f"\nStatistics:")
        print(f"  - With coordinates: {with_coords} ({100*with_coords/len(results):.1f}%)")
        print(f"  - With address: {with_address} ({100*with_address/len(results):.1f}%)")
        print(f"  - On duty (24h): {on_duty} ({100*on_duty/len(results):.1f}%)")
        print(f"  - With optika: {with_optika} ({100*with_optika/len(results):.1f}%)")
        print(f"  - With insurance info: {with_insurance} ({100*with_insurance/len(results):.1f}%)")
        print(f"  - With gallery images: {with_gallery} ({100*with_gallery/len(results):.1f}%)")

    print("\nData columns extracted:")
    print("  - id, name, pharmacy_name_main, description")
    print("  - region, address, latitude, longitude")
    print("  - contact_phone, pharmacy_tel, pharmacy_mob, all_phones")
    print("  - is_duty_24h, has_optika, has_optika_service")
    print("  - insurance_partners")
    print("  - image_url, thumb_image, gallery_images, gallery_count")
    print("  - google_maps_url, page_url")


if __name__ == "__main__":
    main()
