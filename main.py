# @Author: chesterblue
# @File Name:main.py

from Sdl.sdlcore import *
import tools.log as log

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