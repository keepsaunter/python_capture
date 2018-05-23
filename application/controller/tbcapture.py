# -*- coding: utf-8 -*-
from flask import Blueprint, request
from funs import jsonRes
import requests, re, json
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
			return jsonRes(res_detail)
		else: return jsonRes(404, 'goods detail is not exist')
	else: return jsonRes(404, 'goods is not exist')

@tbcapture.route('/commentTotal/<int:goods_id>')
def commentTotal(goods_id):
	get_data = requests.get('https://rate.taobao.com/detailCommon.htm?auctionNumId='+str(goods_id))
	try:
		comment_data = json.loads(get_data.text[3:-1])
	except:
		comment_data = ''
	if comment_data:
		return jsonRes(comment_data.get('data',''))
	else:
		return jsonRes(404, 'goods comment_data is not exist')

@tbcapture.route('/comments/<int:goods_id>')
def comments(goods_id):
	req_data = request.args
	t_page = req_data.get('page', '1')
	t_page_size = req_data.get('page_size', '20')
	t_rateType = req_data.get('rateType', '')
	t_attribute = req_data.get('attribute', '')
	req_str = str(goods_id)+'&currentPageNum='+t_page+'&pageSize='+t_page_size
	if t_rateType:
		req_str += '&rateType='+t_rateType
	if t_attribute:
		req_str += '&attribute='+t_attribute
	get_data = requests.get('https://rate.taobao.com/feedRateList.htm?auctionNumId='+req_str)
	try:
		comment_data = json.loads(get_data.text[3:-2])
	except:
		comment_data = ''
	if comment_data:
		if 'search' in comment_data:
			comment_data.pop('search')
		return jsonRes(comment_data)
	else:
		return jsonRes(404, 'goods comment_data is not exist')