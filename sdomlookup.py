from requests import head
from requests import session

'''
  读取字典文件中的内容
'''
def get_dict_contents(filename):
  subdomain=[]
  with open(filename) as fp:
    for line in fp.readlines():
      line=line.strip()
      subdomain.append(line)
  return subdomain

def request_head(url,s):
  code=head(url).status_code
  if code==200:
    print(url+" [*]")

def main(url,filename):
  subdomain=get_dict_contents(filename)
  s=session()
  for sdom in subdomain:
    url="https://"+sdom+"."+url+"/"
    request_head(url,s)

if __name__=="__main__":
  main("baidu.com","./dict/common.txt")
