import re, requests, json
from docx import Document
from subprocess import call

# file handle fh
#fh = open('gitcommits_test.txt')
fh = call(["git","log","--pretty=format:'%cd %s'"])
p = open('p.txt')
p = p.readline()
url = 'https://jira.brandleadership.ch/rest/api/latest/issue/'
document = Document()
i = 0

while True:
    # read line
    line = fh.readline()
    # Search for Jira Issue
    number = re.search('[a-zA-Z]+-\d+',line)
    if number:
        target = url + number.group()
        response = requests.get(target, auth=('m-ammann', p)).json()
        
        #Add to Word
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
document.save('demo.docx')