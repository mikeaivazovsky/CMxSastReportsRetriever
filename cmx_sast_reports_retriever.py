import sys
import logging
from utils.sast_rest_helper import get_sast_access_token, get_scanId, register_report, report_status_check, get_report
from utils.sast_metadata import Projects
from utils.csv_editor import filter_report

# for this to work first env vars must be configured in OS
# 1 - get an access token https://docs.checkmarx.com/en/34965-278101-using-the-cxsast--rest--api--v8-6-0-and-up-.html#UUID-81760a8b-9b69-6b2f-b630-9b0dd2fbb399_id_UsingtheCxSASTRESTAPIv860andup-Authentication
# 2 - register report request https://checkmarx.stoplight.io/docs/checkmarx-sast-api-reference-guide/aee0e6c7c6a9e-register-a-new-scan-report 
# 3 - looping report status requests until report is created https://checkmarx.stoplight.io/docs/checkmarx-sast-api-reference-guide/8c98d41476bec-retrieve-report-status 
# 4 - and finally get the report https://checkmarx.stoplight.io/docs/checkmarx-sast-api-reference-guide/bc4f6e4c46e89-retrieve-the-report

def args_parsing(args_list):
    arguments = {}
    if len(args_list) > 1:
        for argument in args_list:
            if '=' not in argument:
                continue
            else:
                arguments[argument.split("=")[0]] = argument.split("=")[1]
    
    project_name = None
    product_version = ""
    report_type = "CSV"
    severity = "hm"
    status = "confirmed"
    projects_list = [x.name for x in Projects]
    optimize = True
    for arg in arguments.keys():
        if arg == "p" and arguments[arg].lower() == "all":
            continue
        elif arg == "p":
            project_name = arguments[arg]
            projects_list = [project_name]
        elif arg == "v":
            product_version = arguments[arg]
        elif arg == "t":
            report_type = arguments[arg]
        elif arg == "sv":
            severity = (arguments[arg]).lower()
        elif arg == "st":
            status = arguments[arg].lower()
        elif arg == "opt":
            optimize = arguments[arg]
    
    return project_name, product_version, report_type, severity, status, projects_list, optimize

def main():
    try:
        # for test
        # sys.argv = ["./cmx_sast_reports_retriever.py", "t=CSV", "p=All", "v=0.0",  "sv=HMLI", "st=Not exploitable, To verify", "opt=True"]
        # sys.argv = ["./cmx_sast_reports_retriever.py"]
        project_name, product_version, report_type, severity, status, projects_list, optimize = args_parsing(sys.argv)

        access_token = get_sast_access_token()

        for project_name in projects_list:
            scanId = get_scanId(project_name, access_token)
            print(f'ScanId is: {scanId}')

            reportId = register_report(scanId, access_token, report_type)
            print(f'ReportId is: {reportId}')

            is_created = report_status_check(reportId, access_token)
            print(f'Report is created: {is_created}')

            report_name = get_report(reportId, access_token, project_name, product_version, report_type)

            if report_type == "CSV":
                filter_report(severity, status, report_name, optimize)

    except Exception as e:
        logging.error(f'[sast_report_retrieval] Failed. Error: {e}')

main()