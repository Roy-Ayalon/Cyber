import socket
import requests
from urllib.parse import urlparse

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
}

def get_ip_address(url):
    try:
        ip = socket.gethostbyname(url)
        IP = ip
        return IP
    except:
        pass


def remove_http_https_and_after_coil(url):
    """ Get a url and remove the http/https and everything after the .co.il"""
    parsed = urlparse(url)
    schemeless_url = parsed.netloc + parsed.path
    coil_index = schemeless_url.find('.co.il')
    if coil_index != -1:
        schemeless_url = schemeless_url[:coil_index + len('.co.il')]

    return schemeless_url


def create_dictionary(new_text, url, date, Notifier, OS, ip_of_server):
    lines = new_text.split('\n')
    dictionary = {}
    dictionary = {'url': url}
    for line in lines:
        dictionary['date'] = date
        dictionary['Notifier'] = Notifier
        dictionary['OS'] = OS
        if line.startswith('person:'):
            dictionary['person'] = line.split(':', 1)[1].strip()
        elif line.startswith('phone:'):
            dictionary['phone'] = line.split(':', 1)[1].strip()
        elif line.startswith('e-mail:'):
            dictionary['email'] = (line.split(':', 1)[1].strip()).replace(' AT ', '@')
    dictionary['ip_of_server'] = ip_of_server
    return dictionary


def get_whois_info(url):
    response = requests.get(f'https://who.is/whois/{url}', headers=headers, verify=False)
    if response.status_code == 200:
        return response.text
    else:
        return None


def get_text_between_phrases(text, start_phrase, end_phrase):
    start_index = text.find(start_phrase)
    end_index = text.find(end_phrase)
    if start_index != -1 and end_index != -1:
        return text[start_index:end_index + len(end_phrase)]
    else:
        return None


def get_contact(new_list):
    data = []
    for list in new_list:
        try:
            url = list[2]
            whois_info = get_whois_info(url)
            new_text = get_text_between_phrases(whois_info, "person:", "registrar info:")
            ip_of_server = get_ip_address(url)
            dictionary = create_dictionary(new_text, url, list[0], list[1], list[3], ip_of_server)
            if new_text is not None:
                data.append(dictionary)  # Add the dictionary to the list
                print(dictionary)
            else:
                pass
        except:
            pass

    return data

def create_owner_dictionary(url):
    dictionary = {'url' : url}
    clean_url = remove_http_https_and_after_coil(url)
    who_is_info = get_whois_info(clean_url)
    ip = get_ip_address(url)
    who_is_info = get_text_between_phrases(who_is_info, "person:", "registrar info:")
    lines = who_is_info.split("\n")
    for line in lines:
        if line.startswith('person:'):
            dictionary['person'] = line.split(':', 1)[1].strip()
        elif line.startswith('phone:'):
            dictionary['phone'] = line.split(':', 1)[1].strip()
        elif line.startswith('e-mail:'):
            dictionary['email'] = (line.split(':', 1)[1].strip()).replace(' AT ', '@')
    dictionary['ip_of_server'] = ip
    return dictionary
