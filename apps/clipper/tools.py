# -*- coding: utf-8 -*-
import re
import time
import logging
import traceback

import requests
from PIL import Image


logger = logging.getLogger('clipper.app')


def get_image_info(full_path):
    """
    获取图片的目标尺寸和图片链接
    :param full_path: str: 完整的请求链接
    :return: dict: {
        'url': url,  # 图片链接
        'size': size,  # 要求尺寸
        'status': status  # 状态
    }
    """
    try:
        status = dict()
        info = dict()
        size_pat = re.compile(r'(h_\d*,w_\d*)')
        url_pat = re.compile(
            r'(?:https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|](?:\.jpg|\.png)')
        size = size_pat.findall(full_path)
        if not size:
            status['code'] = 0
            status['message'] = '缺少裁剪尺寸参数或参数填写格式有误，参数格式为h_{裁剪目标高度},w_{裁剪目标宽度}，例如h_300,w_300'
            info['status'] = status
            return info
        else:
            size = size[0]
            height, weight = size.split(',')
            if height:
                height = int(re.compile(r'h_(\d*)').findall(height)[0])
                info['height'] = height
            if weight:
                weight = int(re.compile(r'w_(\d*)').findall(weight)[0])
                info['weight'] = weight
            status['code'] = 1
        url = url_pat.findall(full_path)
        if not url:
            status['code'] = 0
            status['message'] = '缺少图片url参数'
        else:
            url = url[0]
            status['code'] = 1
            info['url'] = url
            info['status'] = status
        return info
    except Exception as e:
        logger.error(e)
        traceback.print_exc()
        info = {
            'status':{
                'code': 0,
                'message': '您输入的参数有误，请检查后重新输入'
            }
        }
        return info



def get_image(url):
    """
    获取原始图片
    :param url: str: 图片url
    :return: str: 裁剪后的图片路径
    """
    try:
        response = requests.get(url)
        content_type = response.headers.get('Content-Type', "")
        is_image = re.compile(r'(image/.*)').findall(content_type)
        if is_image:
            image_type = is_image[0].split('/')[1]
            stamp = int(round(time.time()*1000))
            image_filename = 'static/image_{stamp}.{type}'.format(stamp=stamp, type=image_type)
            with open(image_filename, 'wb') as file:
                file.write(response.content)
            return image_filename, content_type
        else:
            return 0
    except Exception as e:
        logging.error(e)
        traceback.print_exc()
        return 0


def clip_image(image_filename, size):
    """
    按照要求尺寸对图片进行裁剪
    :param image_filename: 图片相对路径
    :param size: dict: {
        "height": int
        "weight": int
    }
    :return: 裁剪后的图片路径
    """
    try:
        pri_image = Image.open(image_filename)
        pri_image_size = pri_image.size
        weight = size.get("weight") if size.get("weight") else pri_image_size[0]
        height = size.get("height") if size.get("height") else pri_image_size[1]
        pri_image.resize((weight, height), Image.ANTIALIAS).save(image_filename)
        return image_filename
    except Exception as e:
        logging.error(e)
        traceback.print_exc()
        return image_filename