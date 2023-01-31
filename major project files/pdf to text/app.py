#import re
#from pdfminer.high_level import extract_pages, extract_text
#text = extract_text("JTs-World.pdf")
#print(text)

#import fitz
#import PIL.Image
#import io
#pdf=fitz.open("JTs-World.pdf")
#counter=1
#for i in range(len(pdf)):
#    page=pdf[i]
#    images=page.get_images()
#    for image in images:
#        base_img=pdf.extract_image(image[0])
#        image_data=base_img['image']
#        img=PIL.Image.open(io.BytesIO(image_data))
#        extension= base_img['ext']
#        img.save(open(f"image{counter}.{extension}", "wb"))
#        counter += 1


import tabula
tables=tabula.read_pdf("Kumbhar Rutuja_Resume.pdf", pages="all")
print(tables)
