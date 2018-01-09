#!/usr/bin/python

from fpdf import FPDF
import sys,os

argCount = len(sys.argv)
if(argCount != 3):
	print "Usage: comicPDF.py [BOOK PATH] [RESULT PATH]"
	sys.exit()

BOOKPATH = sys.argv[1].decode('utf8')
print BOOKPATH
RESULTPATH = sys.argv[2]

# imagelist is the list with all image filenames

for dirname in os.listdir(BOOKPATH):
	if ".DS_Store" in dirname or ".zip" in dirname:
		continue 
	
	pdf = FPDF('L')
	newname = dirname.strip()
	os.rename(os.path.join(BOOKPATH,dirname), os.path.join(BOOKPATH,newname))
	for image in os.listdir(os.path.join(BOOKPATH,newname)):
		if ".jpg" in image or ".png" in image or ".JPEG" in image:
			imagePath = BOOKPATH+"/"+dirname+"/"+image
			pdf.add_page()
			pdf.image(imagePath,x=0, y=0, w=pdf.w, h=pdf.h)
	
	pdf.output(RESULTPATH+"/"+dirname+".pdf", "F")
	print RESULTPATH+"/"+dirname+".pdf"+" generated."

print "Done"
#for image in imagelist:
#	pdf.add_page()
#	pdf.image(image,x,y,w,h)
#pdf.output("yourfile.pdf", "F")