import requests as r 
from bs4 import BeautifulSoup as bs
import os
import re
import pdfkit
import argparse


path_wfk = "Paste the Path to wkhtmltopdf executabele file here"
config = pdfkit.configuration(wkhtmltopdf=path_wfk)


# returns the title of documentation/guide 
def folder_name(str):
	sub = str.split(' ')[0]
	begin = len(str.split(' ')[0])
	end = None
	try:
		end = str.index(sub,begin,len(str))
	except:
		pass
	if(end):
		return str[0:end]
	elif(len(str) < 10):	
		return str[0:len(str)]
	else:
		return str[0:10]
	

# creates a folder for each documentation/guide
def make_dir(root_directory,url):		
	topic = url.split('/')[-1].replace(' ','_')
	if(os.path.exists(os.path.join(root_directory,topic))):
		download_directory = os.path.join(root_directory,topic)
		return download_directory
	else:
		download_directory = os.path.join(root_directory,topic)
		os.mkdir(download_directory)
		return download_directory
		

def generate_pdf(download_directory,url):
	resp = r.get(url).text
	soup = bs(resp,'html.parser')

	lists = soup.find('div',{'class':'sidebar-body'}).find('ol')


	for li in lists:
		ols = li.find('ol')
		if(ols is None):
			filename = str(li.text)
			filename =  re.sub(r'[^a-zA-Z0-9\s]+', '', filename)
			filename = filename.replace(" ","_")
			print(filename)
			try:
				url = li.find('a').get('href')
			except:
				print("No url found for this list")
				continue
			
			
			if(os.path.exists(os.path.join(download_directory,filename+".pdf"))):
				print("Duplicate file")
				continue
			path = os.path.join(download_directory,filename+".pdf")
			print(root+url)
			print(path)
			try:
				pdfkit.from_url(root+url,path,configuration=config)
				print("Success")
				continue
			except:
				print("an error occured for", filename)
				continue
		
		#ols = li.find('ol')
		if(ols is not None and (li.find('summary') != -1)):
			name= folder_name(str(li.find('summary').text))
			name =  re.sub(r'[^a-zA-Z0-9\s]+', '', name)
			name = name.replace(" ","_")
			if(name not in folders):
				cwd = os.path.join(download_directory,name)
				if(not os.path.exists(cwd)):
					os.mkdir(cwd)
			else:
				cwd = os.path.join(download_directory,name)
			print(name)
			print(cwd)
			print()
			count = 1
			for i in ols.find_all('li'):
				filename = str(i.text)
				filename =  re.sub(r'[^a-zA-Z0-9\s]+', '', filename)
				filename = filename.replace(" ","_")
				print(filename)
				url = i.find('a').get('href')
				if(os.path.exists(os.path.join(cwd,str(count)+"--"+filename+".pdf"))):
					print("Duplicate file")
					count+=1
					continue
				path = os.path.join(cwd,str(count)+"--"+filename+".pdf")
				print(root+url)
				print(path)
				try:
					pdfkit.from_url(root+url,path,configuration=config)
				except:
					print("an error occured for", filename)
				count+=1
				print("success")


		
root = 'https://developer.mozilla.org'
dir = os.getcwd()

parser = argparse.ArgumentParser()
parser.add_argument("--url", type=str, help="an url to documentation/guide")
args = parser.parse_args()
url= args.url


download_dir = make_dir(os.path.join(dir,"downloads"),url)

folders = os.listdir(download_dir)

generate_pdf(download_dir,url)
	


print()
			
print("Finished")


			


