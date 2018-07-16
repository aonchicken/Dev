#!python
# log/urls.py
from django.conf.urls import url

from .import views
#2pdf
#from store_app.views import GeneratePdf
#from django_pdfkit import PDFView

#log in 
from django.contrib.auth.decorators import login_required

#from easy_pdf.views import PDFTemplateView
#from .views import PDF_View
from django.template import Context, loader
#from .views import PDFTemplateView

#from .models import Product

#from wkhtmltopdf.views import PDFTemplateView
#from django_pdfkit.views import PDFView


#product = Product.objects.get(id=1)
'''context = {
    'amount': 39.99,
    'customer_name': 'Cooper Mann',
    'order_id': 'เอกสารใบส่งมอบสินค้า',
    'name': 'TTTTT',#product.device_name,
}'''
#context = Context({'amount': 39.99,})


context = {
                'date' : '24 พฤษภาคม 2561',
                'customer_tel' : '0859078578',
                'customer_address' : 'Bankok',
                'no': 1,
                'contract_no': 'สอ.2/2561',
                'customer_name': 'สมมติ ขึ้นมา',
                'detail_pd': 'Router 892w ',
                'staff_name': 'รัฐกานต์ บันที',
                'count_pd' : 1,
                'key_pd': '-',
                'serial_pd' : 84003446789236,
                'ref' : '-',
                'note' : '1กล่อง',
                'range': range(1,15+1),
            }  

# We are adding a URL called /home
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^product/(?P<id>[0-9]+)/', views.detail, name='detail'),#localhost:8000/product/10/
    url(r'^addnew/', views.addnew, name="addnew"),
    url(r'^edit/(?P<id>[0-9]+)/', views.edit, name="edit"),
    url(r'^document/', views.document, name="document"),
    url(r'^doc_pdf/', views.doc_pdf, name="doc_pdf"),
    url(r'^my-pdf/', views.doc_pdf, name="my-pdf"),
    url(r'^display/', views.display, name="display"),
    #url(r'^pdf/', PDFTemplateView.as_view(filename='doc_pdf.pdf',template_name='doc_pdf.html'),name='pdf'),4
   
    url(r'^pdf/$', views.PDFTemplateView.as_view(  cmd_options = {
        'page-size': 'A4',
        'margin-top': 80,
        'margin-bottom': 90,
        #'footer-right': 'Page [page] of [toPage]',
        
        #'margin-right' => 5,
        #'margin-left' => 5,
     
        #'orientation' => 'Landscape',
        #'footer-center' => 'Page [page] of [toPage]',
        #'footer-font-size' => 8,
        #'footer-left' => 'Confidential'

    },template_name='content.html',header_template='header.html',footer_template='footer.html',show_content_in_browser = True), name='pdf'),
    url(r'^mail/', views.mail,name="mail"),
    #url(r'^pdf/$', PDFTemplateView.as_view(template_name='content.html',show_content_in_browser = True), name='pdf'),
  

   
    url(r'^pdf-inline/', views.PDFView.as_view(inline=True, template_name='doc_pdf.html'), name='pdf-inline'),
    #url(r'^pdf-filename/', PDFView.as_view(filename='foo.pdf', template_name='doc_pdf.html'), name='pdf-filename'),
    url(r'^upload2csv/', views.upload, name='uplink'),
    url(r'^import/', views.import_data, name="import"),
    url(r'^handson_view/', views.handson_table, name="handson_view"),
    
]
