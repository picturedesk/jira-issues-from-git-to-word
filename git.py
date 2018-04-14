import re, requests, json, sys
from docx import Document
from subprocess import call

# Settings
u = ''
p = open('p.txt')
p = p.readline()
host = ''
location = sys.argv

# file handle fh
#fh = open('gitcommits_test.txt')
input = call(["git","log",location,"--pretty=format:'%cd %s'"])
endpoint = '/rest/api/latest/issue/'
url = host + endpoint
document = Document()
i = 0

while True:
    # Read line
    line = input.readline()
    # Parse for Jira Issue
    number = re.search('[a-zA-Z]+-\d+',line)
    if number:
        target = url + number.group()
        response = requests.get(target, auth=(u,p)).json()
        
        #Add to Word pages
        document.add_heading(response["fields"]["summary"], 0)
        document.add_heading('Datum', level=1)
        document.add_paragraph(response["fields"]["created"])
        document.add_heading("Jira Nummer", level=1)
        document.add_paragraph(number.group())
        document.add_heading('Beschreibung', level=1)
        document.add_paragraph(response["fields"]["description"])
        document.add_page_break()
    
    i += i

    if i == 5:
        break
    # check if line is not empty
    if not line:
        break
fh.close()

# Save Word with Jira Issues
document.save('output.docx')