import requests
from utils.config import token_endpoint, get_latest_scan, register_report_endpoint, report_status_endpoint, get_report_endpoint, body_token, headers_common, reports_path
import logging
from utils.sast_metadata import Projects
import time
import json

logging.basicConfig(level=logging.INFO)

def get_sast_access_token():
    try:
        access_token = None
        logging.info("[access_token] Starting new token retrieval...")
        response = requests.post(token_endpoint, data=body_token)
        if response is not None:
            status_code = response.status_code
            content = response.content
            if "access_token" in str(content):
                access_token = response.json()["access_token"]
        if status_code >= 300: 
            logging.info(f'[access_token] Failed. Status_code: {status_code}, msg: {content}')
        return access_token 
    except Exception as e:
        logging.error(f'[access_token] Failed. Error: {e}')

def get_scanId(project_name, access_token):
    try:
        headers = (str(headers_common)).replace("{TOKEN}",str(access_token)).replace("'","\"")
        headers = json.loads(headers)
        project_id = Projects[project_name].value
        url = get_latest_scan.replace("{project_id}",str(project_id))
        logging.info(f'[get_scanId] Getting latest scanId for project {project_name}...')
        scanId = None
        response = requests.get(url, headers=headers)
        if response is not None:
            status_code = response.status_code
            content = response.content
        else:
            logging.error('[get_scanId] Request to CMx REST API has failed. Response is None')
        if status_code >= 300: 
            logging.info(f'[get_scanId] Failed. Status_code: {status_code}, msg: {content}')
        last_scan_metadata = json.loads(response.text)[0]
        scanId = last_scan_metadata["id"]
        return scanId
    except Exception as e:
        logging.error(f'[get_scanId] Failed. Error: {e}')

def register_report(scanId, access_token, report_type):
    try:
        headers = (str(headers_common)).replace("{TOKEN}",str(access_token)).replace("'","\"")
        headers = json.loads(headers)
        reportId = None
        logging.info("[register_report] Registering new report request...")
        payload = {
            "reportType": report_type,
            "scanId": scanId
            }
        response = requests.post(register_report_endpoint, data=str(payload), headers=headers)
        if response is not None:
            status_code = response.status_code
            content = response.content
            if "reportId" in str(content):
                reportId = response.json()["reportId"]
        else:
            logging.error('[register_report] Request to CMx REST API has failed. Response is None')
        if status_code >= 300:
            logging.info(f'[register_report] Failed. Status_code: {status_code},  msg: {content}')
        return reportId
    except Exception as e:
        logging.error(f'[register_report] Failed. Error: {e}')

def report_status_check(reportId, access_token):
    try:
        headers = (str(headers_common)).replace("{TOKEN}",str(access_token)).replace("'","\"")
        headers = json.loads(headers)
        url = report_status_endpoint.replace("{id}",str(reportId))
        is_created = False
        time_counter = 0
        logging.info(f'[report_status_check] Checking status for reportId {reportId}...')
        while True:
            status_id = None
            response = requests.get(url, headers=headers)
            if response is not None:
                status_code = response.status_code
                content = response.content
                if "status" in str(content):
                    status_id = response.json()["status"]["id"]
            else:
                logging.error('[report_status_check] Request to CMx REST API has failed. Response is None')
                break
            if status_code >= 300:
                logging.info(f'[report_status_check] Failed. Status_code: {status_code}, msg: {content}')
                break
            if status_id:                    
                if status_id == 0 or status_id == 3:
                    logging.info(f'[report_status_check] Error. Requested report marked either Deleted or Failed')
                    break
                if status_id == 1:
                    time.sleep(5)
                    time_counter = time_counter + 5
                    logging.info(f'[report_status_check] Still preparing the report, time spent: {time_counter} seconds.')
                if status_id == 2:
                    is_created = True
                    break
        return is_created          
    except Exception as e:
        logging.error(f'[report_status_check] Failed. Error: {e}')

def get_report(reportId, access_token, project_name, product_version, report_type):
    try: 
        headers = (str(headers_common)).replace("{TOKEN}",str(access_token)).replace("'","\"")
        headers = json.loads(headers)
        url = get_report_endpoint.replace("{id}",str(reportId))
        logging.info("[get_report] Extracting the report...")
        response = requests.get(url, headers=headers)
        if response is not None:
            status_code = response.status_code
            content = response.content
        else:
            logging.error('[get_report] Request to CMx REST API has failed. Response is None')
        if status_code >= 300: 
            logging.info(f'[get_report] Failed. Status_code: {status_code}, msg: {content}')
        if product_version == "": 
            name = f'{reports_path}/{project_name}_{product_version}sast.{report_type.lower()}'
        else:
            name = f'{reports_path}/{project_name}_{product_version}_sast.{report_type.lower()}'
        name.replace(' ','_').replace(',','_')
        with open(name, 'wb') as f:
            f.write(response.content)
        logging.info(f'[get_report] Report saved as {name}')
        return name
    except Exception as e:
        logging.error(f'[get_report] Failed. Error: {e}')

