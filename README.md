# CMX SAST REPORT RETRIEVER
This tool downloads SAST reports from Checkmarx SAST application using REST API.

Required REST API documentation can be found here: https://checkmarx.stoplight.io/docs/checkmarx-sast-api-reference-guide/bc4f6e4c46e89-retrieve-the-report
Or here: https://corporativeCMxSastDomain.net/cxrestapi/help/swagger/ui/index#!/GENERAL/Reports_PostByreportRequest

## PREREQUISITES
- Before running this tool in the underlying OS two environment variables must be configured: **CMX_USERNAME** and **CMX_PASSWORD**.\
They will be used for **access token** retrieval.
- Configure project names\
Set the scope of SAST projects available for report retrieval by adding **CMx project name** and its **CMx id** in **./utils/sast_metadata.py** in **class Projects(Enum)**.\
Both project name and project ID are taken from CMx SAST UI, project Id can be found in URL of project's web page.
- Configure base_url\
Define **base_url** as the address of your CMx SAST server in **./utils/config.py**.
- Install dependencies\
`pip3 install -r requirements.txt`
- Optional step: extend **optimizable_columns**
By default only a few columns are removed from output report during optimization. This can be configured in **./utils/sast_metadata.py**.

## ARGUMENTS
Arguments must be configured using equal sign without spaces, e.g. **p=ProjectName** or **st="To Verify,Confirmed"**
- If no arguments submitted, defaults will be used:\
reports will be retrieved for **all projects** that are specified in `sast_metadata.py`\
**no version** will be added to the report name\
report will be in **CSV** format\
report will be filtered having only **HM** severity (HIGH & MEDIUM) and only **Confirmed** status and will be **optimized**
- Available arguments:\
**p** - name of project in Checkmarx SAST\
**v** - version of your product, used only in naming output reports\
**t** - desired type of output report (PDF, RTF, CSV, XML)\
**sv** - only for CSV reports. Filter for severity. Specified values will be presented in report, this argument is expected to be a set of first letters for High, Medium, Information, Low, e.g. sv=hm\
**st** - only for CSV reports. Filter for status (result state). Specified values will be presented in report, list here desired statuses from Confirmed, To Verify, Not Exploitable, Urgent, Proposed Not Exploitable, e.g. st="Not exploitable"\
**opt** - only for CSV reports, optimization toggle. If enabled deletes all columns that are listed in optimizable_columns in `./utils/sast_metadata.py`, True or False is expected

## EXAMPLE
Example run:
```
python3 ./cmx_sast_reports_retriever.py p=Project v=1.0 t=PDF
python3 ./cmx_sast_reports_retriever.py t=CSV p=Project v=1.0 sv=HMLI st="Not exploitable, To verify" opt=True
```

## OUTPUT
When CSV type is chosen for each project two reports will be generated - original and filtered one. \
Filtered report is marked with applied filters.\
Output report will be placed in reports folder of this tool:
```
./reports/Project_5.5_sast.pdf
./reports/Project_5.5_sast.csv
./reports/Project_5.5_sast_hm_confirmed.csv
```
