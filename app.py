from flask import Flask, request, render_template, send_file, redirect, url_for, flash
import PureCloudPlatformClientV2
from PureCloudPlatformClientV2.rest import ApiException
from PureCloudPlatformClientV2 import ApiClient, Configuration
import requests
import pandas as pd
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.secret_key = 'key_para_flask'

def get_access_token_organizacion_1():
    url = 'url_token_genesys'
    response = requests.post(url)
    response_data = response.json()
    return response_data['token']

def get_access_token_organizacion_2():
    url = 'url_token_genesys'
    response = requests.post(url)
    response_data = response.json()
    return response_data['token']

def create_api_client(access_token, host):
    config = Configuration()
    config.host = host
    config.access_token = access_token
    api_client = ApiClient()
    api_client.configuration = config
    return api_client

def get_queue_name(api_instance, queue_id):
    try:
        queue = api_instance.get_routing_queue(queue_id)
        return queue.name
    except ApiException as e:
        print(f"Exception when calling RoutingApi->get_routing_queue for queue {queue_id}: {e}\n")
        return None

def fetch_wrapup_codes(api_instance, queue_id, queue_name):
    page_number = 1
    page_size = 25
    wrapup_codes_data = []
    has_wrapups = False

    try:
        while True:
            api_response = api_instance.get_routing_queue_wrapupcodes(queue_id, page_size=page_size, page_number=page_number)
            
            if api_response.entities:
                has_wrapups = True
                for wrapup_code in api_response.entities:
                    wrapup_codes_data.append({
                        'Queue ID': queue_id, 
                        'Queue Name': queue_name,
                        'Wrap-up Code ID': wrapup_code.id, 
                        'Wrap-up Code Name': wrapup_code.name
                    })
    
            if api_response.page_count <= page_number:
                break
            
            page_number += 1

        if not has_wrapups:
            wrapup_codes_data.append({
                'Queue ID': queue_id,
                'Queue Name': queue_name,
                'Wrap-up Code ID': 'N/A', 
                'Wrap-up Code Name': 'No wrap-ups'
            })

    except ApiException as e:
        print(f"Exception when calling RoutingApi->get_routing_queue_wrapupcodes for queue {queue_id}: {e}\n")
    
    return wrapup_codes_data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_wrapups', methods=['POST'])
def get_wrapups():
    organization = request.form['organization'].strip().lower()
    file = request.files['file']
    
    if file and file.filename.endswith('.xlsx'):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        
        df = pd.read_excel(file_path)
        if 'id_queues' not in df.columns:
            flash('El archivo no tiene el encabezado correcto. Asegúrese de que la columna se llame "id_queues" (Descarga el ejemplo)')
            return redirect(url_for('index'))
        
        queue_ids = df['id_queues'].tolist()
        if len(queue_ids) > 25:
            flash('El archivo contiene más de 25 IDs de queues. Solo se pueden procesar un máximo de 25 queues.')
            return redirect(url_for('index'))
    else:
        flash('Archivo no válido. Por favor, cargue un archivo Excel con la columna "id_queues".')
        return redirect(url_for('index'))

    if organization == 'organizacion_1':
        access_token = get_access_token_organizacion_1()
        api_client = create_api_client(access_token, 'host_token_region_genesys')
    elif organization == 'organizacion_2':
        access_token = get_access_token_organizacion_2()
        api_client = create_api_client(access_token, 'host_token_region_genesys')
    else:
        flash('Organización no válida. Por favor, elija "organizacion_1" o "organizacion_2".')
        return redirect(url_for('index'))

    api_instance = PureCloudPlatformClientV2.RoutingApi(api_client)
    wrapup_codes_data = []

    for queue_id in queue_ids:
        queue_id = str(queue_id).strip()
        queue_name = get_queue_name(api_instance, queue_id)
        wrapup_codes_data.extend(fetch_wrapup_codes(api_instance, queue_id, queue_name))

    wrapup_codes_df = pd.DataFrame(wrapup_codes_data)
    output_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'wrapup_codes.xlsx')
    wrapup_codes_df.to_excel(output_file_path, index=False)

    table_html = wrapup_codes_df.to_html(classes='table table-striped', index=False)
    
    return render_template('download.html', filename='wrapup_codes.xlsx', table_html=table_html)

@app.route('/download/<filename>')
def download(filename):
    return render_template('download.html', filename=filename)

@app.route('/download_file/<filename>')
def download_file(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), as_attachment=True)

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
