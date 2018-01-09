#!/usr/bin/python

from fpdf import FPDF
import sys,os,re

argCount = len(sys.argv)
if(argCount != 5):
	print "Usage: comicPDF.py [BOOK PATH] [RESULT PATH] [MODE] [TYPE]"
	sys.exit()

BOOKPATH = sys.argv[1].decode('utf8')
print BOOKPATH
RESULTPATH = sys.argv[2]
MODE = sys.argv[3]
TYPE = sys.argv[4]

# imagelist is the list with all image filenames

def sorted_aphanumeric(data):
	convert = lambda text: int(text) if text.isdigit() else text.lower()
	alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
	return sorted(data, key=alphanum_key)

def normalConvert():
	for dirname in os.listdir(BOOKPATH):
		if ".DS_Store" in dirname or ".zip" in dirname:
			continue 
		
		pdf = FPDF(MODE)
		newname = dirname.strip()
		os.rename(os.path.join(BOOKPATH,dirname), os.path.join(BOOKPATH,newname))
		for image in sorted_aphanumeric(os.listdir(os.path.join(BOOKPATH,newname))):
			if ".jpg" in image or ".png" in image or ".JPEG" in image:
				imagePath = BOOKPATH+"/"+dirname+"/"+image
				pdf.add_page()
				print imagePath
				pdf.image(imagePath,x=0, y=0, w=pdf.w, h=pdf.h)
		
		pdf.output(RESULTPATH+"/"+dirname+".pdf", "F")
		print RESULTPATH+"/"+dirname+".pdf"+" generated."

	print "Done"

def makeBookConvert():
	
	bookCount = 1
	idxCount = 0
	imageCount = 0
	bookDict = {}
	imageArr = []
	
	for dirname in os.listdir(BOOKPATH):
		if ".DS_Store" in dirname or ".zip" in dirname:
			continue 
			
		newname = dirname.strip()
		bookPath = os.path.join(BOOKPATH,newname)
		os.rename(os.path.join(BOOKPATH,dirname), bookPath)
		
		for image in sorted_aphanumeric(os.listdir(bookPath)):
			if ".jpg" in image or ".png" in image or ".JPEG" in image:
				imagePath = BOOKPATH+"/"+dirname+"/"+image
				imageCount = imageCount + 1
				imageArr.append(imagePath)
								
		idxCount = idxCount + 1
		
		if idxCount == 6:
			idxCount = 0
			bookName = BOOKPATH + " "+str(bookCount)
			bookDict[bookName] = imageArr
			imageArr = []
			bookCount = bookCount + 1
	
	for item in bookDict:
		pdf = FPDF(MODE)
		
		for image in bookDict[item]:
			pdf.add_page()
			pdf.image(image,x=0, y=0, w=pdf.w, h=pdf.h)
		
		#pdf.output(RESULTPATH+"/"+item+".pdf", "F")
		print RESULTPATH+"/"+item+".pdf"+" generated."
		
if TYPE == "1":
	makeBookConvert()
else:
	normalConvert()
	