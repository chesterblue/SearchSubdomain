# @Author: chesterblue

import os, click, log, queue
from cmdColor import printGreen, printRed
from requests import head, session
from tqdm import tqdm
from threading import Thread

'''global variate'''
logo = r"""         _                 _             _                
 ___  __| | ___  _ __ ___ | | ___   ___ | | ___   _ _ __  
/ __|/ _` |/ _ \| '_ ` _ \| |/ _ \ / _ \| |/ / | | | '_ \ 
\__ \ (_| | (_) | | | | | | | (_) | (_) |   <| |_| | |_) |
|___/\__,_|\___/|_| |_| |_|_|\___/ \___/|_|\_\\__,_| .__/ 
                                                   |_|      v1.0
"""
known_subdomain = []
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.7113.93 '
                  'Safari/537.36',
}


# 读取字典文件中的内容
def get_dict_contents(filename):
    subdomain = []
    with open(filename) as fp:
        for line in fp.readlines():
            line = line.strip()
            subdomain.append(line)
    return subdomain


# https协议
def request_head_s(url):
    code = 0
    try:
        code = head(url, headers=headers, timeout=3).status_code
    except KeyboardInterrupt:
        # exit()
        os._exit(0)
    except:
        # printRed(url)
        pass
    finally:
        return code


# http协议
def request_head(url):
    code = 0
    try:
        code = head(url, headers=headers, timeout=3).status_code
    except KeyboardInterrupt:
        # exit()
        os._exit(0)
    except:
        # printRed(url)
        pass
    finally:
        return code


# 输出存在此子域名的结果
def printRightResult(domain):
    print(domain, end=" ")
    printGreen("[*]\n")


# 输出不存在此子域名的结果
def printErrorResult(domain):
    print(domain, end=" ")
    printRed("[x]\n")


# 结果保存到文件
def write_into_file(filename):
    with open("./sites/" + filename, "a+") as fp:
        for subdomain in known_subdomain:
            fp.write(subdomain + "\n")


# 判断是否这个子域名是否存在
def isOK(code):
    if code == 200:
        return True
    else:
        return False

# 循环测试每个子站点
def connect_site(search_queue, domain):
    global known_subdomain
    while not search_queue.empty():
        sdom = search_queue.get(block=True, timeout=1)
        url_s = "https://%s.%s/" % (sdom, domain)
        url = "http://%s.%s/" % (sdom, domain)
        code = request_head_s(url_s)
        log.write(url_s)
        if isOK(code):
            known_subdomain.append(url_s)
            printRightResult(url_s)
        else:
            log.write(url)
            code = request_head(url)
            if isOK(code):
                known_subdomain.append(url)
                printRightResult(url)
            else:
                printErrorResult(sdom + "." + domain)
        search_queue.task_done()


# 初始化队列
def init_queue(search_queue, subdomain):
    for i in subdomain:
        search_queue.put(i)


# 多线程
def multi_queue_connect(domain, search_queue, thread_num, target_func):
    for i in range(thread_num):
        t = Thread(target=target_func, args=(search_queue, domain))
        t.start()

@click.command()
@click.option("-t", required="true", help="domain name of the target website")
@click.option("-d", default="./dict/test.txt", help="brute dictionary")
@click.option("-n", default=2, help="number of threads")
def main(t, d, n):
    print(logo)
    log.write("print logo")
    subdomain = get_dict_contents(d)
    log.write("get dictionary")
    search_queue = queue.Queue(len(subdomain))
    log.write("finish new queue")
    init_queue(search_queue, subdomain)
    log.write("Init queue")
    multi_queue_connect(t, search_queue, n, connect_site)
    log.write("finish connect")
    search_queue.join()
    write_into_file(t + ".txt")


if __name__ == "__main__":
    main()
