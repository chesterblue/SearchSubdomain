import os
from requests import head
from requests import session
'''global variate'''
known_subdomain=[]

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

'''
  https协议
'''
def request_head_s(url):
  code=0
  try:
    code=head(url,timeout=3).status_code
  except KeyboardInterrupt:
    os._exit(0)
  except:
    pass
  else:
    return code

'''
  http协议
'''
def request_head(url):
  code=0
  try:
    code=head(url,timeout=3).status_code
  except KeyboardInterrupt:
    os._exit(0)
  except:
    pass
  finally:
    return code

'''
  结果保存到文件
'''
def write_into_file(filename):
  with open(filename,"a+") as fp:
    for subdomain in known_subdomain:
      fp.write(subdomain+"\n")

'''
  循环测试URL
'''
def loop_connect_site(domain,subdomain):
  global known_subdomain
  for sdom in subdomain:
    url_s="https://%s.%s/"%(sdom,domain)
    url="http://%s.%s/"%(sdom,domain)
    print(url_s+"......")
    code=request_head_s(url_s)
    if code==200:
      print(url_s+"[*]")
      known_subdomain.append(url_s)
    else:
      print(url+"......")
      code=request_head(url)
      if code==200:
        print(url+"[*]")
        known_subdomain.append(url)

def main(domain,filename):
  subdomain=get_dict_contents(filename)
  loop_connect_site(domain,subdomain)
  write_into_file(domain+".txt")

if __name__=="__main__":
  main("douyu.com","./dict/common.txt")
