
import pdfplumber
import re
import string
 
filename = input("Enter a filename : ")
pdf=pdfplumber.open(filename)
heading = []
data = ''
span = []
for page in range(0,len(pdf.pages)):
    text = pdf.pages[page]
    txt = text.extract_text()
    content = '\n'.join(el.strip() for el in txt.split('\n') if el.strip())
    content = content.splitlines()
    #print(content)
    regex = re.compile('[@_!#$%^&*-<>?/,\|}{~]')
    for t in content:
      if t.count(' ')<=5 and  regex.search(t) == None and t[-1] != '.':
        extract = t.split(' ')[0:t.count(' ')+1]
        extract = ' '.join(extract)
        #print(extract)
        span.append(re.search(extract,txt).span())
        #print(span)
        heading.append(extract) 
    data += txt
    
#print(span)    
keyword = input('Enter a keyword : ')
pos = re.finditer(keyword,data)
#print(pos)

for p in pos:
    p = p.span()
    for s in span:
        after = s
        if s > p:
            #print('Break the loop')
            break
        before = s   
    #print(before)
    #print(after)
    para = data[before[0]:after[0]]
    print(para)