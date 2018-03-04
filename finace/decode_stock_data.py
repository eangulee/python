# -*- coding: utf-8 -*-
import re  
import datetime  
import json
import sys

def decodePE(filePath,targetFilePath):
	pe_10 = []
	pe_15 = []
	pe_20 = []
	pe_all = []
	# Reading data back
	with open(filePath, 'r',encoding='utf-8') as f:
		for line in f:
			text = line.replace('\'','\"')
			data = json.JSONDecoder().decode(text)
			# print(data)
			try:
				pe = float(data['市盈率MRQ'])
				if(pe > 0 and pe <= 10):
					data['pe'] = pe
					pe_10.append(data)
					pe_all.append(data)
				elif(pe > 10 and pe <= 15):
					data['pe'] = pe
					pe_15.append(data)
					pe_all.append(data)
				elif(pe > 15 and pe <= 20):
					data['pe'] = pe
					pe_20.append(data)
					pe_all.append(data)
			except:
				pass
	# sort by aesc
	pe_10 = sorted(pe_10,key=lambda pe: pe['市盈率MRQ'], reverse=False)
	pe_15 = sorted(pe_15,key=lambda pe: pe['市盈率MRQ'], reverse=False)
	pe_20 = sorted(pe_20,key=lambda pe: pe['市盈率MRQ'], reverse=False)

	pe_all = sorted(pe_all,key=lambda pb:pb['市净率'], reverse=False)

	'''
	with open(targetFilePath,'a',encoding='utf-8') as f:
		print('10倍pe总计：{0}只:'.format(len(pe_10)))
		f.write('10倍pe总计：{0}只:'.format(len(pe_10)) + '\n')
		for d in pe_10:
			print(d)
			f.write(str(d)+ '\n')
		print('15倍pe总计：{0}只:'.format(len(pe_15)))
		f.write('15倍pe总计：{0}只:'.format(len(pe_15)) + '\n')
		for d in pe_15:
			print(d)
			f.write(str(d)+ '\n')
		print('20倍pe总计：{0}只:'.format(len(pe_20)))
		f.write('20倍pe总计：{0}只:'.format(len(pe_20)) + '\n')
		for d in pe_20:
			print(d)
			f.write(str(d)+ '\n')
			print('20倍pe总计：{0}只:'.format(len(pe_20)))
		f.write('市净率排序:' + '\n')
		for d in pe_all:
			print(d)
			f.write(str(d)+ '\n')
	'''
	with open(targetFilePath,'a',encoding='utf-8') as f:
		print('10倍pe总计：{0}只:'.format(len(pe_10)))
		f.write('10倍pe总计：{0}只:'.format(len(pe_10)) + '\n')
		for i in range(len(pe_10)):
			d = pe_10[i]
			text = str(i+1)+'.'+d['股票名称']+' '+str(d['pe'])+'(pe) '+d['市净率']+'(pb)'
			print(text)
			f.write(text+ '\n')
		print('15倍pe总计：{0}只:'.format(len(pe_15)))
		f.write('15倍pe总计：{0}只:'.format(len(pe_15)) + '\n')
		for i in range(len(pe_15)):
			d = pe_15[i]
			text = str(i+1)+'.'+d['股票名称']+' '+str(d['pe'])+'(pe) '+d['市净率']+'(pb)'
			print(text)
			f.write(text+ '\n')
		print('20倍pe总计：{0}只:'.format(len(pe_20)))
		f.write('20倍pe总计：{0}只:'.format(len(pe_20)) + '\n')
		for i in range(len(pe_20)):
			d = pe_20[i]
			text = str(i+1)+'.'+d['股票名称']+' '+str(d['pe'])+'(pe) '+d['市净率']+'(pb)'
			print(text)
			f.write(text+ '\n')
		f.write('市净率排序:' + '\n')
		for i in range(len(pe_all)):
			d = pe_all[i]
			text = str(i+1)+'.'+d['股票名称']+' '+str(d['pe'])+'(pe) '+d['市净率']+'(pb)'
			print(text)
			f.write(text+ '\n')
def decodePB():
	pass

def aesc_sorted(x,y):
	if(x['pe'] < y['pe']):
		return -1
	if(x['pe'] > y['pe']):
		return 1
	return 0

def main():
	print('start')
    # 数据保存路径
	time = re.sub(r'[^0-9]','_',str(datetime.datetime.now()))
	intput_file = 'data/stock_info_2018_03_04_01_05_36_174000.txt'
	output_file = 'data/stock_pe_list_{0}.txt'.format(time)
	print(output_file)
	decodePE(intput_file,output_file)
	print('over')
    
if __name__ == '__main__':
	main()  