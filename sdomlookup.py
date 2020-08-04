# @Author: chesterblue

import os,click
from cmdColor import printGreen
from requests import head,session
from tqdm import tqdm

'''global variate'''
logo=r"""         _                 _             _                
 ___  __| | ___  _ __ ___ | | ___   ___ | | ___   _ _ __  
/ __|/ _` |/ _ \| '_ ` _ \| |/ _ \ / _ \| |/ / | | | '_ \ 
\__ \ (_| | (_) | | | | | | | (_) | (_) |   <| |_| | |_) |
|___/\__,_|\___/|_| |_| |_|_|\___/ \___/|_|\_\\__,_| .__/ 
                                                   |_|      v1.0
"""
known_subdomain=[]


 # 读取字典文件中的内容
def get_dict_contents(filename):
  subdomain=[]
  with open(filename) as fp:
    for line in fp.readlines():
      line=line.strip()
      subdomain.append(line)
  return subdomain

# https协议
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

# http协议
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

# 结果保存到文件
def write_into_file(filename):
  with open(filename,"a+") as fp:
    for subdomain in known_subdomain:
      fp.write(subdomain+"\n")

#判断是否这个子域名是否存在
def isOK(code,url):
  if code == 200:
    return True
  else:
    return False

# 循环测试URL
def loop_connect_site(domain,subdomain):
  global known_subdomain
  for sdom in tqdm(subdomain,ascii=True):
    url_s="https://%s.%s/"%(sdom,domain)
    url="http://%s.%s/"%(sdom,domain)
    code=request_head_s(url_s)
    if isOK(code,url_s):
      known_subdomain.append(url_s)
    else:
      code=request_head(url)
      if isOK(code,url):
        known_subdomain.append(url)

#输出结果
def PrintResult():
  global known_subdomain
  for domain in known_subdomain:
    print(domain,end=" ")
    printGreen("[*]\n")

@click.command()
@click.option("-t",required="true",help="domain name of the target website")
@click.option("-d",default="./dict/common.txt",help="brute dictionary")
def main(t,d):
  print(logo)
  subdomain=get_dict_contents(d)
  loop_connect_site(t,subdomain)
  PrintResult()
  write_into_file(t+".txt")

if __name__=="__main__":
  main()
