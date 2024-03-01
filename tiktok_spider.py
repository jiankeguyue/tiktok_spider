#! usr/bin/env python
#  writer: yueji0j1anke

import requests
import datetime
import colorama
import pandas as pd
import os
import threading
import config
import log
import json

# ids = ['7317205561290886450','7323148494234045731','7296051796198411546','7205552823567532852']
ids = ['7205521489125215488','7317205561290886450']

def title():
    print("                                        ")
    print(colorama.Fore.BLUE + "|    | \ _ / | \\ ___ /(/  \\_ __ _| |")
    print(colorama.Fore.BLUE + "|____|__\_/__|  \\ __/( /__\\ _    | |")
    print(colorama.Fore.BLUE + "|    |__/ \__|   \\ /(  /  \\      | |   ")
    print(colorama.Fore.BLUE + "|    | /   \ |    |(___/_ \\  spider_TikTOk_|\\_\\")
    print(colorama.Fore.YELLOW + "                                 writer: yuejinjianke")
    print('\n')
    print('\n')


def get_data(id,file_path,log_recorder):
    url_list = []
    nickname_list = []
    gender_list = []
    place_list = []
    user_id_list = []
    comment_time_list = []
    content_list = []
    content_level_list = []
    likes_num = []
    page = 0

    url = 'https://www.douyin.com/aweme/v1/web/comment/list/'
    headers = {
        'cookie': config.cookie,
        'referer': 'https://www.douyin.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 SLBrowser/9.0.3.1311 SLBChan/10',
    }

    while True:
    # 请求参数
       params = {
           "device_platform": "webapp",
           "aid": 6383,
           "channel": "channel_pc_web",
           "aweme_id": id,
           "cursor": page * 20,
           "count": 20,
           "item_type": 0,
           "insert_ids": "",
           "whale_cut_token": "",
           "cut_version": 1,
           "rcFT": "",
           "pc_client_type": 1,
           "version_code": 170400,
           "version_name": "17.4.0",
           "cookie_enabled": True,
           "screen_width": 1235,
           "screen_height": 823,
           "browser_language": "zh-CN",
           "browser_platform": "Win32",
           "browser_name": "Chrome",
           "browser_version": "109.0.0.0",
           "browser_online": True,
           "engine_name": "Blink",
           "engine_version": "109.0.0.0",
           "os_name": "Windows",
           "os_version": "10",
           "cpu_core_num": 16,
           "device_memory": 8,
           "platform": "PC",
           "downlink": 7.2,
           "effective_type": "4g",
           "round_trip_time": 150,
           "webid": "7208902085361960506",
           "msToken": "VjT914ox94y25sviLBEH1agIm_VfbCOKYwvc3jZjUgGoKdR7NdPAMefyNWXH7d29zI9HpiMG6eo2DK4tRM32Zg3fZByGIDn412Mg3cpF6FqSWhcdsZTvvtJmU8E1GGIF",
           "X-Bogus": "DFSzswVuGvUANndftbv0TBt/pLwG"
       }
       try:
            response = requests.get(url=url,params=params,headers=headers)

       except Exception as e:
            print(colorama.Fore.RED + '[error] 爬取页面 {} 时出现故障： {}'.format(id,e))
            log_recorder.logger.error('[error] 爬取页面 {} 时出现故障： {}'.format(id,e))
            break
       try:
          json_data = response.json()
       except Exception as e:
           print(colorama.Fore.RED + '[error] 对应api数据为空,无法爬取')
           log_recorder.logger.error('[error] {} 子评论 {} 对应api数据为空,无法爬取'.format(id,cid))
           break

       comments = json_data['comments']
       if comments is not None:
           print(colorama.Fore.GREEN + '[info] 正在爬取一级评论页面 {} 第 {} 页'.format(id, page))
       else:
           data_save(url_list, nickname_list, place_list, user_id_list, comment_time_list, content_list,content_level_list, likes_num, file_path)
           print(colorama.Fore.GREEN + '[info] 没有更多页了')
           print(colorama.Fore.GREEN + '[info] id为 {} 的页面爬取完毕'.format(id))
           log_recorder.logger.info('[info] id为 {} 的页面爬取完毕'.format(id))
           break

       print(colorama.Fore.GREEN + '[info] 正在爬取一级评论页面 {} 第 {} 页'.format(id, page))
       for comment in comments:
            # 爬取一级评论
            list_append1(url_list, nickname_list, place_list, user_id_list, comment_time_list, content_list,content_level_list, likes_num, comment)

            # 二级评论逻辑
            if int(comment['reply_comment_total']):
               cid = comment['cid']
               print(colorama.Fore.BLUE + '[info] id 为 {} 的评论拥有子评论 {} 条'.format(comment['cid'], comment['reply_comment_total']))
               print(colorama.Fore.BLUE + '[info] id 为 {} 的评论即将展开子评论爬取'.format(comment['cid']))
               get_child_data(id, cid, url_list, nickname_list, place_list, user_id_list, comment_time_list, content_list,content_level_list, likes_num)

    # 判断父级评论是否爬取完成
       if int(json_data['has_more']):
           page += 1
           if page >= 250:
               data_save(url_list, nickname_list, place_list, user_id_list, comment_time_list, content_list,content_level_list, likes_num, file_path)
               break
           print(colorama.Fore.GREEN + '[info] 正在爬取一级评论页面 {} 第 {} 页'.format(id, page))
           continue
       else:
           data_save(url_list, nickname_list, place_list, user_id_list, comment_time_list, content_list,content_level_list, likes_num, file_path)
           print(colorama.Fore.GREEN + '[info] 没有更多页了')
           print(colorama.Fore.GREEN + '[info] id为 {} 的页面爬取完毕'.format(id))
           log_recorder.logger.info('[info] id为 {} 的页面爬取完毕'.format(id))
           break






def get_child_data(id,cid,url_list,nickname_list,place_list,user_id_list,comment_time_list,content_list,content_level_list,likes_num):
    child_page = 0
    url = 'https://www.douyin.com/aweme/v1/web/comment/list/reply/'
    headers = {
        'cookie': config.cookie,
        'referer': 'https://www.douyin.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 SLBrowser/9.0.3.1311 SLBChan/10',
    }
    while True:
        params = {
            "device_platform": "webapp",
            "aid": 6383,
            "channel": "channel_pc_web",
            "item_id": id,
            "comment_id": cid,
            "cut_version": 1,
            "cursor": child_page * 20,
            "count": 20,
            "item_type": 0,
            "pc_client_type": 1,
            "version_code": 170400,
            "version_name": "17.4.0",
            "cookie_enabled": True,
            "screen_width": 1235,
            "screen_height": 823,
            "browser_language": "zh-CN",
            "browser_platform": "Win32",
            "browser_name": "Chrome",
            "browser_version": "109.0.0.0",
            "browser_online": True,
            "engine_name": "Blink",
            "engine_version": "109.0.0.0",
            "os_name": "Windows",
            "os_version": 10,
            "cpu_core_num": 16,
            "device_memory": 8,
            "platform": "PC",
            "downlink": 10,
            "effective_type": "4g",
            "round_trip_time": 50,
            "webid": "7208902085361960506",
            "msToken": "1A4z-84Nbe47dZ1eCesmWqlVfCHeXwP3Cgt20m5bUt5bJXF66921Ty4M9Q_zckms44BPIVkm9dI0_0ZTxDZYowjMIk88seRYW-OO1UZZKpuohRpMa6pRwICKXC9XIq8=",
            "X-Bogus": "DFSzswVLkkUANnzrtbI6/-t/pL3t"
        }
        try:
            response = requests.get(url=url, params=params, headers=headers)

        except Exception as e:
            print(colorama.Fore.RED + '[error] 爬取 {} 子评论 {} 时出现故障： {}'.format(id,cid,e))
            break

        try:
            json_data = response.json()
        except Exception as e:
            print(colorama.Fore.RED + '[error] 对应api数据为空,无法爬取')
            log_recorder.logger.error('[error] {} 子评论 {} 对应api数据为空,无法爬取'.format(id, cid))
            break

        comments = json_data['comments']
        if comments is not None:
            print(colorama.Fore.GREEN + '[info] 正在爬取子评论 {} 第 {} 页'.format(cid, child_page))
            for comment in comments:
                # 爬取二级评论
                list_append2(url_list, nickname_list, place_list, user_id_list, comment_time_list, content_list,
                             content_level_list, likes_num, comment)
            if int(json_data['has_more']):
                child_page += 1
                print(colorama.Fore.GREEN + '[info] 正在爬取子评论 {} 第 {} 页'.format(cid, child_page))
                continue
            else:
                print(colorama.Fore.GREEN + '[info] 子评论没有更多页了')
                print(colorama.Fore.BLUE + '[info] id 为 {} 的评论子评论 爬取完毕，总共爬取 {} 条'.format(
                    comment['cid'], comment['comment_reply_total']))
                log_recorder.logger.info(
                    '[info] id 为 {} 的评论子评论 爬取完毕，总共爬取 {} 条'.format(comment['cid'],
                                                                                  comment['comment_reply_total']))
                break
        else:
            print(colorama.Fore.GREEN + '[info] 子评论没有更多页了')
            break



def list_append1(url_list,nickname_list,place_list,user_id_list,comment_time_list,content_list,content_level_list,likes_num,comment):
    url_list.append("https://www.douyin.com/video/"+comment['aweme_id'])
    nickname_list.append(comment['user']['nickname'])
    user_id_list.append(comment['user']['uid'])
    place_list.append(comment['ip_label'])
    content_list.append(comment['text'])
    comment_time_list.append(datetime.datetime.fromtimestamp(int(comment['create_time'])).strftime("%Y-%m-%d %H:%M:%S"))
    content_level_list.append("一级评论")
    likes_num.append(comment['digg_count'])

def list_append2(url_list,nickname_list,place_list,user_id_list,comment_time_list,content_list,content_level_list,likes_num,comment):
    url_list.append("https://www.douyin.com/video/"+comment['aweme_id'])
    nickname_list.append(comment['user']['nickname'])
    user_id_list.append(comment['user']['uid'])
    place_list.append(comment['ip_label'])
    content_list.append(comment['text'])
    comment_time_list.append(datetime.datetime.fromtimestamp(int(comment['create_time'])).strftime("%Y-%m-%d %H:%M:%S"))
    content_level_list.append("二级评论")
    likes_num.append(comment['digg_count'])


def data_save(url_list,nickname_list,place_list,user_id_list,comment_time_list,content_list,content_level_list,likes_num,file_path):
    df = pd.DataFrame(
        {
            '评论链接': url_list,
            '评论者昵称': nickname_list,
            '评论者id': user_id_list,
            '地区': place_list,
            '评论内容': content_list,
            '评论时间': comment_time_list,
            '评论等级': content_level_list,
            '点赞数量': likes_num
        }
    )
    if os.path.exists(file_path):
        header = False
    else:
        header = True
    df.to_csv(file_path, mode="a+", header=header, index=False, encoding='utf_8_sig')


def multi_thread(ids,log_recorder):
    threads = []
    for id in ids:
        threads.append(
            threading.Thread(target=get_data,args=(id,f"{id}.csv",log_recorder))
        )

    for task in threads:
        task.start()

    for task in threads:
        task.join()


if __name__ == '__main__':
    title()
    print(colorama.Fore.GREEN + '[info] 开始爬取')
    log_recorder = log.Log_Recorder()
    log_recorder.logger.info('[info] 开始爬取')
    multi_thread(ids,log_recorder)