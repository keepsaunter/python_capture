# -*- coding: utf-8 -*-
def jsonRes(st='suc', msg='', data={}):
	import json
	res = {}
	#设置返回码
	status_codes = { 'suc': 200, 'err': 999 }
	#处理参数
	if not (type(st) == str or type(st) == int): data, st = (st, 'suc')
	if type(st) == int:
		res['st'] = st
	elif st in status_codes:
		res['st'] = status_codes[st]
	else: st, msg = ('suc', st)
	if not (type(msg) == str or type(msg) == int): data, msg = (msg, '')
	
	if msg: res['msg'] = msg
	if data: res['data'] = data
	return json.dumps(res)