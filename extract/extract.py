import pdfplumber
import re
import string
 
filename = input("Enter a filename : ")
pdf=pdfplumber.open(filename)
data = ''
span = []
heading = []
for page in range(0,len(pdf.pages)):
    text = pdf.pages[page]
    txt = text.extract_text()
    content = '\n'.join(el.strip() for el in txt.split('\n') if el.strip())
    content = content.splitlines()
    regex = re.compile('[@_!#$%^&;,*()<>?/\,|}{~●]')
    for t in content:
      if t.count(' ')<6 and  regex.search(t) == None and t[-1] != '.' and t[-1].isdigit() == False:
        print(t)
        heading.append(t)
    data += txt
for h in heading :
 span.append(re.search(h,data).span())
keyword = input('Enter a keyword : ')
keyword_pos = re.finditer(keyword,data)
#print(keyword_pos)
eof = re.search('\Z',data)
eof = eof.span()
for p in keyword_pos:
    p = p.span()
    for s in span:
        after = s
        if s > p:
            break
        before = s   
    #print(before)
    #print(after)
    if before == after:
      para = data[after[0]:eof[0]]
    else:
      para = data[before[0]:after[0]]
    print(para)
