# @Author: chesterblue
# @File Name:main.py

from Sdl.sdlcore import *
import click, queue
import tools.log as log
from Se import baidu, bing, google
from Dns import threadcrowd, virusTotal
import configparser
import tools.deduplicate as deduplicate

"""
global variable
"""
config = configparser.ConfigParser()
config.read("./conf/default.ini")
default_dict = "./dict/" + config['cmd']['dictName']
default_thread_num = int(config['cmd']['threadNum'])
proxies = config['proxies']
virus_api_key = config['ApiKey']['virusapikey']


def brute(domain, dict_name, thread_num):
    """
    爆破功能
    """
    subdomain = get_dict_contents(dict_name)
    log.write("get dictionary")
    search_queue = queue.Queue(len(subdomain))
    log.write("finish new queue")
    init_queue(search_queue, subdomain)
    log.write("Init queue")
    multi_queue_connect(domain, search_queue, thread_num, connect_site)
    log.write("finish connect")
    search_queue.join()
    write_into_file(domain + ".txt")


def start_search_engine(se, domain):
    """
    搜索引擎爬虫功能
    """
    # e.g:search_engine = ['baidu','google']
    search_engine = se.strip().split(',')
    se_subdomains = []
    for client in search_engine:
        if client == 'baidu':
            Baidu = baidu.Client(domain)
            se_subdomains.extend(Baidu.run())
        elif client == 'google':
            Google = google.Client(domain, proxies=proxies)
            se_subdomains.extend(Google.run())
        elif client == 'bing':
            Bing = bing.Client(domain)
            se_subdomains.extend(Bing.run())
    return se_subdomains


def dns_resolution(domain):
    """
    dns解析API
    """
    dns_subdomains = []
    # VirusTotal DNS resolution
    VirusTotal = virusTotal.Client(domain, virus_api_key)
    dns_subdomains.extend(VirusTotal.run())
    # threadcrowd DNS resolution
    ThreadCrowd = threadcrowd.Client(domain, proxies)
    dns_subdomains.extend(ThreadCrowd.run())
    return dns_subdomains


def data_processing(web_subdomains):
    web_subdomains = deduplicate.remove_duplicate_data(web_subdomains)
    print("------------------------web spider or dns resolution:-----------------------------")
    for subdomain in web_subdomains:
        print(subdomain)

def write_subdomains_to_file(filename: str, subdomains: list):
    with open("./sites/"+filename, "a+") as fp:
        fp.write("------------------------web spider or dns resolution:--------------------------\n")
        for subdomain in subdomains:
            fp.write(subdomain+'\n')


@click.command()
@click.option("-t", required="true", help="domain name of the target website")
@click.option("-d", default=default_dict, help="brute dictionary")
@click.option("-n", default=default_thread_num, help="number of threads")
@click.option("--bt", is_flag=True, help="use bruting subdomain")
@click.option("--se", help="select use search engine[support google,baidu and bing now]. e.g., --se google,baidu")
@click.option("--dns", is_flag=True, help="use dns resolution")
def main(t, d, n, bt, se, dns):
    domain = t
    print(logo)
    log.write("print logo")
    web_subdomains = []
    if bt:
        dict_name = d
        thread_num = n
        brute(domain, dict_name, thread_num)
    # 如果使用se参数，执行爬虫功能
    if se:
        web_subdomains.extend(start_search_engine(se, domain))
    # 如果使用dns参数，执行dns解析功能
    if dns:
        web_subdomains.extend(dns_resolution(domain))
    if se or dns:
        data_processing(web_subdomains)
        write_subdomains_to_file(domain+'.txt', web_subdomains)


if __name__ == "__main__":
    main()
