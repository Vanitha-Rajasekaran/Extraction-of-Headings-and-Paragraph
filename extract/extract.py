import pdfplumber
import re
 
def text_extraction(pdf):
    text=''
    heading = []
    for pages in range(0,len(pdf.pages)):
        page = pdf.pages[pages]
        text += page.extract_text()
    return text
    
def heading_extraction(text):
    heading = []
    content = '\n'.join(el.strip() for el in text.split('\n') if el.strip())
    content = content.splitlines()
    regex = re.compile('[@_!#$?;''%^;,*()<>\[\]?/=\,“”"|}{~●•]')
    for t in content:
        if t.count(' ')<6 and  regex.search(t) == None and t[-1] != '.' and t[-1].isdigit() == False:
            heading.append(t)
    return heading
    
def span_of_heading(heading,text):
    span = []
    for h in heading:
        span.append(re.search(h,text).span())
    return span

def keyword(text):
    keyword = input('Enter a keyword : ')
    keyword_pos = re.finditer(keyword,text)
    return keyword_pos
    
def search(keyword_pos,span,text):
    flag = 0
    content = ''
    for p in keyword_pos:
        p = p.span()
        for s in span:
            after = s
            if s > p:
                break
            before = s  
        if flag == after:
            continue
        if before == after:
            content += '\n'+text[after[0]:]
        else:
            content += '\n'+text[before[0]:after[0]]
        flag = after
    return content
    
#main
filename = input("Enter a filename : ")
pdf = pdfplumber.open(filename)
text = text_extraction(pdf)
heading = heading_extraction(text)
span = span_of_heading(heading,text)
keyword_pos = keyword(text)
content = search(keyword_pos,span,text)
print(content)
