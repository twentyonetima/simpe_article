import os
import requests
from bs4 import BeautifulSoup
from django.conf import settings

file_path = os.path.join(settings.BASE_DIR, 'index.txt')


def get_last_date():
    try:
        url = 'https://mirror.calculate-linux.org/release/'
        page = requests.get(url)
        page.raise_for_status()
        soup = BeautifulSoup(page.text, 'html.parser')
        links = soup.find_all('a')
        last_el = links[-1]
        last_href = last_el.get('href')[:-1]
        return last_href
    except requests.exceptions.RequestException as e:
        return "Error fetching webpage: " + str(e)
    except (ValueError, IndexError) as e:
        return "Error processing data: " + str(e)
    except Exception as e:
        return "An unexpected error occurred: " + str(e)


def read_date():
    with open(file_path, "r") as file:
        last_id = file.read().strip()
    return last_id


def get_page_content(url):
    page = requests.get(url)
    page.raise_for_status()
    return BeautifulSoup(page.text, 'html.parser')


def check_changing_date():
    file_date = read_date()
    server_date = get_last_date()
    if file_date == server_date:
        return server_date
    else:
        try:
            file_links = get_page_content('https://mirror.calculate-linux.org/release/{}/'.format(file_date)).find_all('a')
            server_links = get_page_content('https://mirror.calculate-linux.org/release/{}/'.format(server_date)).find_all('a')
            if len(server_links) < len(file_links):
                return file_date
            else:
                return server_date
        except requests.exceptions.RequestException as e:
            return "Error fetching webpage: " + str(e)


def rewrite_date():
    last_href = check_changing_date()
    with open(file_path, "r") as file:
        last_id = file.read().strip()
    print("Stored ID:", last_id)

    if not last_id or int(last_id) < int(last_href):
        with open(file_path, "w") as file:
            file.write(str(last_href))
        print("Updated ID in index.txt")
        return last_href
    else:
        print("No update needed.")
        return last_id


def get_new_links():
    date = rewrite_date()
    try:
        url = 'https://mirror.calculate-linux.org/release/' + date + '/'
        page = requests.get(url)
        page.raise_for_status()
        soup = BeautifulSoup(page.text, 'html.parser')
        links = soup.find_all('a')
        links = refactor_links(links, date)
        return links
    except requests.exceptions.RequestException as e:
        return "Error fetching webpage: " + str(e)
    except (ValueError, IndexError) as e:
        return "Error processing data: " + str(e)
    except Exception as e:
        return "An unexpected error occurred: " + str(e)


def dict_with_tag():
    lst = get_new_links()
    new_dict = dict()
    for i in range(0, len(lst)):
        if lst[i].get_text() == 'SHA256SUMS':
            new_dict['SHA256'] = lst[i].get('href')
        elif lst[i].get_text() == 'SHA512SUMS':
            new_dict['SHA512'] = lst[i].get('href')
        elif lst[i].get_text().endswith('.list'):
            text_list = lst[i].get_text().split('-')
            text_list[0] = text_list[0].upper()
            new_dict[text_list[0] + ':list'] = lst[i].get('href')
        elif lst[i].get_text().endswith('.iso'):
            text_iso = lst[i].get_text().split('-')
            text_iso[0] = text_iso[0].upper()
            href = lst[i].get('href')
            new_dict[text_iso[0] + ':iso'] = href
            size = get_file_size(href)
            new_dict[text_iso[0] + ':size'] = determine_size(size)
    new_dict['release'] = rewrite_date()
    return new_dict


def refactor_links(links, date):
    links = [i for i in links if i.get('href') not in ['../', 'README.txt', 'SHA256SUMS.asc', 'SHA512SUMS.asc']]
    base_url = 'https://mirror.calculate-linux.org/release/' + date + '/'
    for link in links:
        href = link.get('href')
        if href and not href.startswith('http'):
            link['href'] = base_url + href
    return links


def get_file_size(url):
    try:
        response = requests.head(url)
        if response.status_code == 200:
            content_length = response.headers.get('Content-Length')
            return int(content_length) if content_length else "Content-Length header not found"
        else:
            return "Failed to fetch file headers. Status code: {}".format(response.status_code)
    except Exception as e:
        return "An error occurred: {}".format(str(e))


def determine_size(size):
    units = ['bytes', 'KiB', 'MiB', 'GiB']
    for unit in units:
        if size < 1024 or unit == 'GiB':
            return "({} {})".format(round(size, 1), unit)
        size /= 1024
