import streamlit as st
import matplotlib.pyplot as plt
from fpdf import FPDF
import base64
from matplotlib.pyplot import fill
import numpy as np
from tempfile import NamedTemporaryFile

from xarray import align

def create_download_link(val, filename):
    b64 = base64.b64encode(val)  # val looks like b'...'
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}.pdf">Download file</a>' 

#framework style
#pdf_w=210
#pdf_h=297 

#def lines(pdf):
    #pdf.set_fill_color(255, 255, 255) # color for outer rectangle
    #pdf.rect(5.0, 5.0, 200.0,287.0,'DF')
    #pdf.set_fill_color(255, 255, 255) # color for inner rectangle
    #pdf.rect(8.0, 8.0, 194.0,282.0,'FD')
#Tittle
def tittle(pdf):
	pdf.set_font('Arial', 'B', 16)
	pdf.cell(200, 10, txt = "Google Maps Dashboard", ln = 1, align = 'C')
#Logo
def logo(pdf):
	pdf.image(name = 'logo1.png', x = 65, y = 19, w = 90, h = 50, link = 'http://localhost:8501/media/f27f03a91f9ea879ce3fac82f75f94d9cc4b318f6b0338dac6b93970.png')

#i = 2
#business_name = 'Chili\'s'
#types = ['Restaurant', 'Food', 'Place of Interest']
#Business name
business_name = 'Chilli\'s' 
def business(pdf, business_name):
	pdf.set_font('Arial', 'B', 18)
	pdf.text(x = 100, y = 70, txt = business_name)
#Business type
types = ['Restaurant', 'Food', 'Place of Interest']
def business_types(pdf, item, y):
	pdf.set_font('Arial', '', 14)
	#pdf.set_text_color(102, 102, 255)
	pdf.text(x = 10, y = y, txt = item)
#Address
address = 'C. 60 local 124, Zona Indiustrial'
def business_address(pdf, address):
	pdf.set_font('Arial', '', 14)
	pdf.text(x = 33, y = 125, txt = address)
#business
def column_my_business(pdf):
	pdf.set_font('Arial', 'B', 14)
	pdf.text(x = 30, y= 140, txt = 'My business')
	pdf.text(x = 150, y = 140, txt = 'Others')
#rating
my_rating = '4.2'
other_rating = '4.0'
def business_rating(pdf, my_rating, other_rating):
	pdf.set_font('Arial', '', 12)
	pdf.text(x = 52, y= 150, txt = my_rating)
	pdf.text(x = 183, y = 150, txt = other_rating)
#price level
my_price_level = '4.0'
other_price_level = '3.0'
def pricing_level(pdf, my_price_level, other_price_level):
	pdf.set_font('Arial', '', 12)
	pdf.text(x = 61, y = 160, txt = my_price_level)
	pdf.text(x = 192, y = 160, txt = other_price_level)
#comments
my_comment_number = '150'
other_comment_number = '120'
def comment_number(pdf, my_comment_number, other_comment_number):
	pdf.set_font('Arial', '', 12)
	pdf.text(x = 61, y = 170, txt = my_price_level)
	pdf.text(x = 186, y = 170, txt = other_price_level)







   

class PDF(FPDF): 

	pdf = FPDF()#pdf object
	pdf = FPDF(orientation='L')
	pdf = FPDF(unit='mm') #unit of measurement
	pdf = FPDF(format='A4') #page format. A4 is the default value of the format, you don't have to specify it.
	pdf = FPDF(orientation='P', unit='mm', format='A4')

	

	pdf.add_page()
	#lines(pdf)
	tittle(pdf) 
	logo(pdf)
	business(pdf, business_name)
	#pdf.set_text_color(220, 50, 50)
	pdf.text(x = 10, y = 80, txt = 'Types:')
	y = 90
	for item in types:
		business_types(pdf, item, y)
		y += 10
	pdf.set_font('Arial', 'B', 14)
	pdf.text(x = 10, y = 125, txt = 'Address: ')
	business_address(pdf, address)
	column_my_business(pdf)
	pdf.set_font('Arial', 'B', 12)
	pdf.text(x = 30, y = 150, txt = 'My rating:')
	pdf.set_font('Arial', 'B', 12)
	pdf.text(x = 150, y = 150, txt = 'Average rating:')
	business_rating(pdf, my_rating, other_rating)
	pdf.set_font('Arial', 'B', 12)
	pdf.text(x = 30, y = 160, txt = 'My price level:')
	pdf.set_font('Arial', 'B', 12)
	pdf.text(x = 150, y = 160, txt = 'Average price level:')
	pricing_level(pdf, my_price_level, other_price_level)
	pdf.set_font('Arial', 'B', 12)
	pdf.text(x = 30, y = 170, txt = 'My comments:')
	pdf.set_font('Arial', 'B', 12)
	pdf.text(x = 150, y = 170, txt = 'Other comments:')
	comment_number(pdf, my_comment_number, other_price_level)
	html = create_download_link(pdf.output(dest="S").encode("latin-1"), "testfile")
	st.markdown(html, unsafe_allow_html=True)
	pdf.output('test.pdf','F')









	

	


	












