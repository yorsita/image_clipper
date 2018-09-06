# -*- coding: utf-8 -*-
import re
import logging
import traceback

from django.views.generic.base import View
from django.http import HttpResponse

from apps.clipper import tools


logger = logging.getLogger('clipper.app')


class ClipperView(View):
    """
    图片裁剪
    """
    def get(self, request):
        """
        获取裁剪后的图片
        :param request:
        :return:
        """
        try:
            logger.info('Got a job, start processing...')
            path = request.get_full_path()
            logger.info('Getting image info...')
            image_info = tools.get_image_info(path)
            status = image_info.get('status')
            if status.get('code') == 1:
                image_url = image_info.get('url')
                image_height = image_info.get('height', None)
                image_weight = image_info.get('weight', None)
                logger.info('Getting image...')
                pri_image, content_type = tools.get_image(image_url)
                if pri_image:
                    logger.info('Clipping image...')
                    output_image = tools.clip_image(pri_image, {'height': image_height, 'weight': image_weight})
                    image_data = open(output_image, 'rb').read()
                    logger.info('Succeed output image!')
                    return HttpResponse(image_data, content_type=content_type)
                else:
                    logger.info('Image URL was wrong...')
                    message = '图片链接有误'
                    return HttpResponse(message)
            elif status.get('code') == 0:
                message = status.get('message')
                return HttpResponse(message)
        except Exception as e:
            logger.error(e)
            traceback.print_exc()
            return HttpResponse('您输入的参数有误，请检查后重新输入')
