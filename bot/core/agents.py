import random
import re

existing_versions = {
    110: [
        '110.0.5481.154',
        '110.0.5481.153',
        '110.0.5481.65',
        '110.0.5481.64',
        '110.0.5481.63',
        '110.0.5481.61'
    ],
    111: [
        "111.0.5563.116",
        '111.0.5563.115',
        '111.0.5563.58',
        '111.0.5563.49'
    ],
    112: [
        '112.0.5615.136',
        '112.0.5615.136',
        '112.0.5615.101',
        '112.0.5615.100',
        '112.0.5615.48'
    ],
    113: [
        '113.0.5672.77',
        '113.0.5672.76'
    ],
    114: [
        '114.0.5735.60',
        '114.0.5735.53'
    ],
    115: [
        '115.0.5790.136'
    ],
    116: [
        '116.0.5845.172',
        '116.0.5845.164',
        '116.0.5845.163',
        '116.0.5845.114',
        '116.0.5845.92'
    ],
    117: [
        '117.0.5938.154',
        '117.0.5938.141',
        '117.0.5938.140',
        '117.0.5938.61',
        '117.0.5938.61',
        '117.0.5938.60'
    ],
    118: [
        '118.0.5993.112',
        '118.0.5993.111',
        '118.0.5993.80',
        '118.0.5993.65',
        '118.0.5993.48'
    ],
    119: [
        '119.0.6045.194',
        '119.0.6045.193',
        '119.0.6045.164',
        '119.0.6045.163',
        '119.0.6045.134',
        '119.0.6045.134',
        '119.0.6045.66',
        '119.0.6045.53'
    ],
    120: [
        '120.0.6099.230',
        '120.0.6099.210',
        '120.0.6099.194',
        '120.0.6099.193',
        '120.0.6099.145',
        '120.0.6099.144',
        '120.0.6099.144',
        '120.0.6099.116',
        '120.0.6099.116',
        '120.0.6099.115',
        '120.0.6099.44',
        '120.0.6099.43'
    ],
    121: [
        '121.0.6167.178',
        '121.0.6167.165',
        '121.0.6167.164',
        '121.0.6167.164',
        '121.0.6167.144',
        '121.0.6167.143',
        '121.0.6167.101'
    ],
    122: [
        '122.0.6261.119',
        '122.0.6261.106',
        '122.0.6261.105',
        '122.0.6261.91',
        '122.0.6261.90',
        '122.0.6261.64',
        '122.0.6261.43'
    ],
    123: [
        '123.0.6312.121',
        '123.0.6312.120',
        '123.0.6312.119',
        '123.0.6312.118',
        '123.0.6312.99',
        '123.0.6312.80',
        '123.0.6312.41',
        '123.0.6312.40'
    ],
    124: [
        '124.0.6367.179',
        '124.0.6367.172',
        '124.0.6367.171',
        '124.0.6367.114',
        '124.0.6367.113',
        '124.0.6367.83',
        '124.0.6367.82',
        '124.0.6367.54'
    ],
    125: [
        '125.0.6422.165',
        '125.0.6422.164',
        '125.0.6422.147',
        '125.0.6422.146',
        '125.0.6422.113',
        '125.0.6422.72',
        '125.0.6422.72',
        '125.0.6422.53',
        '125.0.6422.52'
    ],
    126: [
        '126.0.6478.122',
        '126.0.6478.72',
        '126.0.6478.71',
        '126.0.6478.50'
    ]
}

devices = [
    ('Samsung', 'SM-G980F', 'AVERAGE', 10),
    ('Samsung', 'SM-G973F', 'AVERAGE', 9),
    ('Samsung', 'SM-G973U', 'AVERAGE', 9),
    ('Samsung', 'SM-N986B', 'AVERAGE', 11),
    ('Samsung', 'SM-N981B', 'AVERAGE', 11),
    ('Samsung', 'SM-F916B', 'AVERAGE', 11),
    ('Samsung', 'SM-G998B', 'HIGH', 12),
    ('Samsung', 'SM-G991B', 'HIGH', 12),
    ('Samsung', 'SM-G996B', 'HIGH', 12),
    ('Samsung', 'SM-G990E', 'HIGH', 12),
    ('Samsung', 'SM-G990B', 'HIGH', 12),
    ('Samsung', 'SM-G990B2', 'HIGH', 12),
    ('Samsung', 'SM-G990U', 'HIGH', 12),
    ('Google', 'Pixel 5', 'AVERAGE', 11),
    ('Google', 'Pixel 5a', 'AVERAGE', 11),
    ('Google', 'Pixel 6', 'AVERAGE', 12),
    ('Google', 'Pixel 6 Pro', 'AVERAGE', 12),
    ('Google', 'Pixel 6 XL', 'AVERAGE', 12),
    ('Google', 'Pixel 6a', 'AVERAGE', 12),
    ('Google', 'Pixel 7', 'HIGH', 13),
    ('Google', 'Pixel 7a', 'AVERAGE', 13),
    ('Google', 'Pixel 7 Pro', 'HIGH', 13),
    ('Google', 'Pixel 8', 'HIGH', 14),
    ('Google', 'Pixel 8a', 'HIGH', 14),
    ('Google', 'Pixel 8 Pro', 'HIGH', 14),
    ('Google', 'Pixel 9', 'HIGH', 14),
    ('Google', 'Pixel 9 Pro', 'HIGH', 14),
    ('Google', 'Pixel 9 Pro XL', 'HIGH', 14),
    ('Xiaomi', 'Mi 10', 'AVERAGE', 10),
    ('Xiaomi', 'Mi 11', 'AVERAGE', 11),
    ('Xiaomi', 'Mi 12', 'HIGH', 12),
    ('Xiaomi', 'Redmi Note 10', 'HIGH', 11),
    ('Xiaomi', 'Redmi Note 10 Pro', 'HIGH', 11),
    ('Xiaomi', 'Redmi Note 11', 'HIGH', 12),
    ('Xiaomi', 'Redmi Note 11 Pro', 'HIGH', 12),
    ('Xiaomi', 'Redmi Note 12', 'HIGH', 13),
    ('Xiaomi', 'Redmi Note 12 Pro', 'HIGH', 13),
    ('Xiaomi', 'POCO M3 Pro', 'HIGH', 11),
    ('Xiaomi', 'POCO X5', 'HIGH', 12),
    ('Xiaomi', 'POCO X5 Pro', 'HIGH', 12),
    ('Xiaomi', 'POCO X6 Pro', 'HIGH', 13),
    ('Xiaomi', 'POCO F4', 'HIGH', 12),
    ('Xiaomi', 'POCO F4 GT', 'HIGH', 12),
    ('Xiaomi', 'POCO F3', 'HIGH', 11),
    ('OnePlus', 'NE2215', 'AVERAGE', 12),
    ('OnePlus', 'NE2210', 'AVERAGE', 12),
    ('OnePlus', 'IN2010', 'AVERAGE', 10),
    ('OnePlus', 'IN2023', 'AVERAGE', 11),
    ('OnePlus', 'LE2117', 'AVERAGE', 11),
    ('OnePlus', 'LE2123', 'AVERAGE', 11),
    ('OnePlus', 'CPH2423', 'AVERAGE', 12),
    ('Huawei', 'VOG-AL00', 'AVERAGE', 9),
    ('Huawei', 'ANA-AL00', 'AVERAGE', 10),
    ('Huawei', 'TAS-AL00', 'AVERAGE', 10),
    ('Huawei', 'OCE-AN10', 'AVERAGE', 11),
    ('Sony', 'J9150', 'AVERAGE', 9),
    ('Sony', 'J9210', 'AVERAGE', 10)
]

def generate_random_user_agent(device_type='android', browser_type='chrome'):
    firefox_versions = list(range(100, 127))  # Last 10 versions of Firefox

    if browser_type == 'chrome':
        major_version = random.choice(list(existing_versions.keys()))
        browser_version = random.choice(existing_versions[major_version])
    elif browser_type == 'firefox':
        browser_version = random.choice(firefox_versions)

    if device_type == 'android':
        android_versions = {
            '10': 29,
            '11': 30,
            '12': 31,
            '13': 33,
            '14': 34
        }

        manufacturer, model, performance_class, min_android_version = random.choice(devices)
        android_version = str(random.choice([v for v in android_versions.keys() if int(v) >= min_android_version]))
        sdk_version = android_versions[android_version]

        if browser_type == 'chrome':
            major_version = random.choice(list(existing_versions.keys()))
            browser_version = random.choice(existing_versions[major_version])
        elif browser_type == 'firefox':
            browser_version = random.choice(firefox_versions)

        telegram_version = "11.4.2"

        if browser_type == 'chrome':
            return (f"Mozilla/5.0 (Linux; Android {android_version}; {model}) AppleWebKit/537.36 "
                    f"(KHTML, like Gecko) Chrome/{browser_version} Mobile Safari/537.36 "
                    f"Telegram-Android/{telegram_version} ({manufacturer} {model}; Android {android_version}; "
                    f"SDK {sdk_version}; {performance_class})")
        elif browser_type == 'firefox':
            return (f"Mozilla/5.0 (Android {android_version}; Mobile; rv:{browser_version}.0) "
                    f"Gecko/{browser_version}.0 Firefox/{browser_version}.0 "
                    f"Telegram-Android/{telegram_version} ({manufacturer} {model}; Android {android_version}; "
                    f"SDK {sdk_version}; {performance_class})")

    elif device_type == 'ios':
        ios_versions = ['13.0', '14.0', '15.0', '16.0', '17.0', '18.0']
        ios_version = random.choice(ios_versions)
        if browser_type == 'chrome':
            return (f"Mozilla/5.0 (iPhone; CPU iPhone OS {ios_version.replace('.', '_')} like Mac OS X) "
                    f"AppleWebKit/537.36 (KHTML, like Gecko) CriOS/{browser_version} Mobile/15E148 Safari/604.1")
        elif browser_type == 'firefox':
            return (f"Mozilla/5.0 (iPhone; CPU iPhone OS {ios_version.replace('.', '_')} like Mac OS X) "
                    f"AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/{browser_version}.0 Mobile/15E148 Safari/605.1.15")

    elif device_type == 'windows':
        windows_versions = ['10.0', '11.0']
        windows_version = random.choice(windows_versions)
        if browser_type == 'chrome':
            return (f"Mozilla/5.0 (Windows NT {windows_version}; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                    f"Chrome/{browser_version} Safari/537.36")
        elif browser_type == 'firefox':
            return (f"Mozilla/5.0 (Windows NT {windows_version}; Win64; x64; rv:{browser_version}.0) "
                    f"Gecko/{browser_version}.0 Firefox/{browser_version}.0")

    elif device_type == 'ubuntu':
        if browser_type == 'chrome':
            return (f"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) AppleWebKit/537.36 (KHTML, like Gecko) "
                    f"Chrome/{browser_version} Safari/537.36")
        elif browser_type == 'firefox':
            return (f"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:{browser_version}.0) Gecko/{browser_version}.0 "
                    f"Firefox/{browser_version}.0")

    return None

def get_sec_ch_ua(user_agent: str) -> str:
    browser_version = re.search(r'Chrome/(\d+)', user_agent).group(1)
    return f'"Android WebView";v="{browser_version}", "Chromium";v="{browser_version}", "Not_A Brand";v="24"'