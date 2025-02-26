import os

base_url = "https://corporativeCMxSastDomain.net/cxrestapi/"

token_endpoint = base_url + "auth/identity/connect/token"
get_latest_scan = base_url + "help/sast/scans?projectId={project_id}&last=1&scanStatus=Finished"
register_report_endpoint = base_url + "reports/sastScan"
report_status_endpoint = base_url + "reports/sastScan/{id}/status"
get_report_endpoint = base_url + "reports/sastScan/{id}"

username = os.getenv('CMX_USERNAME')
password = os.getenv('CMX_PASSWORD')

body_token =  {
    "username":username,
    "password":password,
    "grant_type":"password",
    "scope":"sast_rest_api",
    "client_id":"resource_owner_client",
    "client_secret":"014DF517-39D1-4453-B7B3-9930C563627C"
    }

headers_common =  {
    "Content-Type": "application/json;v=1.0",
    "Accept": "application/json;v=1.0",
    "Authorization": "Bearer {TOKEN}"
    }

current_dir = os.getcwd()
if not os.path.exists(f'{current_dir}/reports/'):
      os.makedirs(f'{current_dir}/reports/')
reports_path = f'{current_dir}/reports'
      