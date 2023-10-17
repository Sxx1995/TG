from ruamel import yaml

from service.provider.TextImgProvider import TextImgProvider
from service.provider.BackgroundImgProvider import BackgroundImgProvider
from service.provider.TextProvider import TextProvider
from service.provider.SmoothAreaProvider import SmoothAreaProvider
from service.provider.LayoutProvider import LayoutProvider
from utils import log
from multiprocessing import Pool
import traceback
import os

basedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..')
conf: dict
text_img_provider: TextImgProvider
background_img_provider: BackgroundImgProvider
text_provider: TextProvider
smooth_area_provider: SmoothAreaProvider
layout_provider: LayoutProvider


def load_from_config():
    global text_img_provider
    global background_img_provider
    global text_provider
    global smooth_area_provider
    global layout_provider

    text_img_provider = TextImgProvider(**conf['provider']['text_img'])
    background_img_provider = BackgroundImgProvider(conf['provider']['bg_img'])
    text_provider = TextProvider(conf['provider']['text'])
    smooth_area_provider = SmoothAreaProvider(**conf['provider']['smooth_area'])
    layout_provider = LayoutProvider(**conf['provider']['layout'])


def init_config():
    log.info("load config")
    global conf
    with open(os.path.join(basedir, "config.yml"), 'r') as f:
        conf = yaml.load(f.read(), Loader=yaml.Loader)
        text2add = conf['provider']['bbox']
        load_from_config()
        return text2add


def init():
    return init_config()


def run(text, bbox):
  from service.base import gen_all_pic
  gen_all_pic(text, bbox)



def start():
    text2add = init()
    process_count = conf['base']['process_count']
    print('Parent process {pid}.'.format(pid=os.getpid()))
    print('process count : {process_count}'.format(process_count=process_count))

    #p = Pool(process_count)
    #for i in range(process_count):
    #    p.apply_async(run, ([x.values() for x in text2add], ))
    run([list(x.keys())[0]for x in text2add], [x[list(x.keys())[0]] for x in text2add])
    print('Waiting for all subprocesses done...')
    p.close()
    p.join()
    print('All subprocesses done.')


if __name__ == '__main__':
    init_config()
    print(conf)
