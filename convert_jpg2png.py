import os

# Convert .jpg to .png
print ("Converting .jps to .pngs ...")
os.system('mogrify -density 400 -background white -alpha remove -format png ./*.jpg[0]')

# Remove extra files
#os.system('rm *.json')
#os.system('rm *.jpg')
