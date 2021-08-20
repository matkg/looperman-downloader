from credentials import email, password

"""
Data and Headers generated with
https://curl.trillworks.com/
"""

headers = {
    'authority': 'www.looperman.com',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'origin': 'https://www.looperman.com',
    'content-type': 'application/x-www-form-urlencoded',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-gpc': '1',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'referer': 'https://www.looperman.com/account/login',
    'accept-language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
    'cookie': 'loop_csrfc=45c8f731b4309e4ac20d5143badd39a8; loop_session=4f2711443b3aefe72e2029c79756a885f228eef6',
}

data = {
  'csrftoken': '45c8f731b4309e4ac20d5143badd39a8',
  'user_email': '',
  'upass': '',
  'user_remember_code': '1',
  'user_disclaimer': '1',
  'submit': 'submit'
}

def login(session):
  email.replace("@", "^%^40")
  data["user_email"] = email
  data["upass"] = password
  session.post('https://www.looperman.com/account/login', headers=headers, data=data)