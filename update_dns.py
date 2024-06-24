import os
import time
import requests
import logging

API_TOKEN = os.getenv('API_TOKEN')
ZONE = os.getenv('ZONE')
SUBDOMAIN = os.getenv('SUBDOMAIN', '')
PROXIED = os.getenv('PROXIED', 'false').lower() == 'true'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

headers = {
    'Authorization': f'Bearer {API_TOKEN}',
    'Content-Type': 'application/json'
}

def get_external_ip():
    response = requests.get('https://api.ipify.org?format=json')
    response.raise_for_status()
    return response.json()['ip']

def get_zone_id():
    url = f'https://api.cloudflare.com/client/v4/zones?name={ZONE}'
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()['result'][0]['id']

def get_dns_record(zone_id):
    name = f'{SUBDOMAIN}.{ZONE}' if SUBDOMAIN else ZONE
    url = f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records?type=A&name={name}'
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    records = response.json()['result']
    if records:
        return records[0]['id'], records[0]['content']
    return None, None

def update_dns_record(zone_id, record_id, ip):
    name = f'{SUBDOMAIN}.{ZONE}' if SUBDOMAIN else ZONE
    url = f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}'
    data = {
        'type': 'A',
        'name': name,
        'content': ip,
        'ttl': 300,
        'proxied': PROXIED
    }
    response = requests.put(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()

def create_dns_record(zone_id, ip):
    name = f'{SUBDOMAIN}.{ZONE}' if SUBDOMAIN else ZONE
    url = f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records'
    data = {
        'type': 'A',
        'name': name,
        'content': ip,
        'ttl': 300,
        'proxied': PROXIED
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()

def main():
    zone_id = get_zone_id()

    while True:
        try:
            current_ip = get_external_ip()
            record_id, dns_ip = get_dns_record(zone_id)
            
            name = f'{SUBDOMAIN}.{ZONE}' if SUBDOMAIN else ZONE
            if not record_id:
                create_dns_record(zone_id, current_ip)
                logger.info(f"Created new A record for {name} with IP {current_ip}")
            elif current_ip != dns_ip:
                update_dns_record(zone_id, record_id, current_ip)
                logger.info(f"Updated A record for {name} to new IP {current_ip}")
            else:
                logger.debug(f"No IP change detected. Current IP is still {current_ip}")
        except Exception as e:
            logger.error(f"An error occurred: {e}")
        time.sleep(300)  # Wait for 5 minutes

if __name__ == '__main__':
    main()