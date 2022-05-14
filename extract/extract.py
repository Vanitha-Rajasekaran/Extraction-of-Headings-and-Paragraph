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
    
def search(keyword_pos,span,text,dicts,totalpages,filename):
    flag = before = after = 0
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
            p = dicts[after]["page"]
            if totalpages-p == 0:
              content += '\n Found on Page : '+str(p)+'\n'+text[after[0]:]
            else:
              content += '\n Found on Pages : '+str(p)+' - '+str(totalpages)+'\n'+text[after[0]:]
            #tableextraction(p,totalpages,filename)
        else:
            p1 = dicts[before]["page"]
            p2= dicts[after]["page"]
            if p2-p1 > 0 :
              content += '\n Found on Pages : '+str(p1)+' - '+str(p2)+'\n'+text[before[0]:after[0]]
            else:
              content += '\n Found on Pages : '+str(p1)+'\n'+text[before[0]:after[0]]
            #tableextraction(p1,p2,filename)
        flag = after
    return content

def page_finder(dicts,span):
  for pages in range(0,len(pdf.pages)):
        page = pdf.pages[pages]
        text = page.extract_text()
        for i in range(len(span)):
          d = dicts[span[i]]["head"]
          if d in text:
            dicts[span[i]]["page"] = pages+1
  return dicts 
  
def tableextraction(p1,p2,filename):
  tables =camelot.read_pdf(filename,flavor="lattice",pages='all')
  if tables.n > 0:
    for i in range(0,tables.n):
      temp = tables[i].shape
      if temp[1] == 1:
        continue
      else:
        header = tables[i].df.iloc[0]
        new_df = pd.DataFrame(tables[i].df.values[1:],columns=header)
        #new_df = new_df.replace('\n',' ', regex=True)
        print(new_df)
        
#main
dicts = {}
filename = input("Enter a filename : ")
pdf = pdfplumber.open(filename)
totalpages=len(pdf.pages)
text = text_extraction(pdf)
heading = heading_extraction(text)
span = span_of_heading(heading,text)
for i in range(len(span)):
  j = span[i]
  dicts[j] = {}
  head = heading[i]
  dicts[j]["head"] = head
dicts = page_finder(dicts,span)
keyword_pos = keyword(text)
content = search(keyword_pos,span,text,dicts,totalpages,filename)
print(content)
