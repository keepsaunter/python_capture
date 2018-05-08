# -*- coding: utf-8 -*-
from flask import Blueprint
from funs import jsonRes
import requests,re
tbcapture = Blueprint('tbcapture', __name__)
@tbcapture.route('/<int:goods_id>')
def index(goods_id):
	#抓取商品详情页
	# tb_page = requests.get('https://detail.tmall.com/item.htm?id='+str(goods_id))	#tm
	tb_page = requests.get('https://item.taobao.com/item.htm?id='+str(goods_id))
	page_data = tb_page.text
	res_reg = re.search(r'\"descUrl\":\"([^\"]*)\"', page_data)	#tm
	if not res_reg:
		res_reg = re.search(r'[{,]\s*descUrl *:[^\?]*\? *\'([^\']*)\'', page_data)	#tb
	detail_url = res_reg.group(1) if res_reg else ''	#获取详情数据地址
	if detail_url:
		detail_data = requests.get("http:"+detail_url)
		if detail_data.text:
			# res_detail = [x+'_760x760Q50s50.jpg_.webp' for x in re.findall(r'src=\"([^\"]*)\"', detail_data.text) if re.search(r'\.(jpg|png)$', x)]
			res_detail = [x for x in re.findall(r'src=\"([^\"]*)\"', detail_data.text) if re.search(r'\.(jpg|png)$', x)]
			# print(res_detail)
			return jsonRes(res_detail)
		else: return  jsonRes(404, 'goods detail is not exist')
	else: return  jsonRes(404, 'goods is not exist')