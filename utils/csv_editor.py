import pandas as pd
import logging
from utils.sast_metadata import optimizable_columns

def filter_severity(severity, report, columns):
    filtered_report = pd.DataFrame(columns=columns)
    filtered_report1 = None
    filtered_report2 = None
    filtered_report3 = None
    filtered_report4 = None
    if "h" in severity:
        filtered_report1 = report[report["Result Severity"] == "High"]
    if "m" in severity:
        filtered_report2 = report[report["Result Severity"] == "Medium"]
    if "i" in severity:
        filtered_report3 = report[report["Result Severity"] == "Information"]
    if "l" in severity:
        filtered_report4 = report[report["Result Severity"] == "Low"]
    filtered_report = pd.concat([filtered_report, filtered_report1, filtered_report2, filtered_report3, filtered_report4])
    return filtered_report

def filter_status(status, report, columns):
    filtered_report = pd.DataFrame(columns=columns)
    filtered_report1 = None
    filtered_report2 = None
    filtered_report3 = None
    filtered_report4 = None
    filtered_report5 = None
    if "confirmed" in status:
        filtered_report1 = report[report["Result State"] == "Confirmed"]
    if "to verify" in status:
        filtered_report2 = report[report["Result State"] == "To Verify"]
    if "not exploitable" in status:
        filtered_report3 = report[report["Result State"] == "Not Exploitable"]
    if "urgent" in status:
        filtered_report4 = report[report["Result State"] == "Urgent"]
    if "proposed not exploitable" in status:
        filtered_report5 = report[report["Result State"] == "Proposed Not Exploitable"]
    filtered_report = pd.concat([filtered_report, filtered_report1, filtered_report2, filtered_report3, filtered_report4, filtered_report5])
    return filtered_report

def optimize_report(report):
    report = report.drop(columns=optimizable_columns)
    return report

def filter_report(severity, status, report_name, optimize):
    logging.info(f'[filter_report] Report filtering started...')
    report = pd.read_csv(f'{report_name}')
    report_name = report_name.split(".csv")[0]
    filtered_severity_report = filter_severity(severity, report, report.columns)
    filtered_severity_and_status_report = filter_status(status, filtered_severity_report, report.columns)
    if optimize == 'True':
        filtered_severity_and_status_report = optimize_report(filtered_severity_and_status_report)
    new_report_name = (f'{report_name}_{severity}_{status}.csv').replace(' ','_').replace(',','_')
    filtered_severity_and_status_report.to_csv(new_report_name, index=False)
    logging.info(f'[filter_report] Filtered report saved as {new_report_name}')