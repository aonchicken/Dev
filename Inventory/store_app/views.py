''''from django.shortcuts import render

# Create your views here.
'''


from __future__ import absolute_import, print_function, unicode_literals
import os
#
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.http import HttpResponse
#!python
# log/views.py
from django.shortcuts import render, render_to_response, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import Product, Staff, Document, Customer, Goods,Question,Choice
from .forms import ProductForm

# html2pdf

# from .utils import render_to_pdf ##created in step 4
#from .utils import render_to_pdf2
from django.views.generic import View
from django.template.loader import get_template, render_to_string
# html2pdf

from django.conf import settings

from django.contrib.auth import get_user_model
from django.utils.timezone import now
from django.views.generic import DetailView


from django.template import Context, loader

from os.path import basename, splitext

from django.test import override_settings
from django.views.generic import TemplateView
import pdfkit

from django.core.mail import EmailMessage, send_mail
from django.contrib import messages


# Create your views here.
# this login required decorator is to not allow to any
# view without authenticating

from django.template.response import TemplateResponse
# ----------------------------------------------

from .utils import (content_disposition_filename, render_pdf_from_template)
# --------------------_excel_function_------------------------------------------  
from django.http import HttpResponseBadRequest
from django import forms
from django.template import RequestContext
import django_excel as excel
from ._compact import JsonResponse

data = [
    [1, 2, 3],
    [4, 5, 6]
]


class UploadFileForm(forms.Form):
    file = forms.FileField()


# Create your views here.
def upload(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            filehandle = request.FILES['file']
            return excel.make_response(filehandle.get_sheet(), "csv",
                                       file_name="download")
    else:
        form = UploadFileForm()
    return render(
        request,
        'upload_form.html',
        {
            'form': form,
            'title': 'Excel file upload and download example',
            'header': ('Please choose any excel file ' +
                       'from your cloned repository:')
        })


def download(request, file_type):
    sheet = excel.pe.Sheet(data)
    return excel.make_response(sheet, file_type)


def download_as_attachment(request, file_type, file_name):
    return excel.make_response_from_array(
        data, file_type, file_name=file_name)


def export_data(request, atype):
    if atype == "sheet":
        return excel.make_response_from_a_table(
            Question, 'xls', file_name="sheet")
    elif atype == "book":
        return excel.make_response_from_tables(
            [Question, Choice], 'xls', file_name="book")
    elif atype == "custom":
        question = Question.objects.get(slug='ide')
        query_sets = Choice.objects.filter(question=question)
        column_names = ['choice_text', 'id', 'votes']
        return excel.make_response_from_query_sets(
            query_sets,
            column_names,
            'xls',
            file_name="custom"
        )
    else:
        return HttpResponseBadRequest(
            "Bad request. please put one of these " +
            "in your url suffix: sheet, book or custom")


def import_data(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST,
                              request.FILES)

        def choice_func(row):
            q = Question.objects.filter(slug=row[0])[0]
            row[0] = q
            return row
        if form.is_valid():
            request.FILES['file'].save_book_to_database(
                models=[Question, Choice],
                initializers=[None, choice_func],
                mapdicts=[
                    ['question_text', 'pub_date', 'slug'],
                    ['question', 'choice_text', 'votes']]
            )
            return redirect('handson_view')
        else:
            return HttpResponseBadRequest()
    else:
        form = UploadFileForm()
    return render(
        request,
        'upload_form.html',
        {
            'form': form,
            'title': 'Import excel data into database example',
            'header': 'Please upload sample-data.xls:'
        })


def import_sheet(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST,
                              request.FILES)
        if form.is_valid():
            request.FILES['file'].save_to_database(
                name_columns_by_row=2,
                model=Question,
                mapdict=['question_text', 'pub_date', 'slug'])
            return HttpResponse("OK")
        else:
            return HttpResponseBadRequest()
    else:
        form = UploadFileForm()
    return render(
        request,
        'upload_form.html',
        {'form': form})


def exchange(request, file_type):
    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():
        filehandle = request.FILES['file']
        return excel.make_response(filehandle.get_sheet(), file_type)
    else:
        return HttpResponseBadRequest()


def parse(request, data_struct_type):
    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():
        filehandle = request.FILES['file']
        if data_struct_type == "array":
            return JsonResponse({"result": filehandle.get_array()})
        elif data_struct_type == "dict":
            return JsonResponse(filehandle.get_dict())
        elif data_struct_type == "records":
            return JsonResponse({"result": filehandle.get_records()})
        elif data_struct_type == "book":
            return JsonResponse(filehandle.get_book().to_dict())
        elif data_struct_type == "book_dict":
            return JsonResponse(filehandle.get_book_dict())
        else:
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()


def handson_table(request):
    return excel.make_response_from_tables(
        [Question, Choice], 'handsontable.html')


def embed_handson_table(request):
    """
    Renders two table in a handsontable
    """
    content = excel.pe.save_book_as(
        models=[Question, Choice],
        dest_file_type='handsontable.html',
        dest_embed=True)
    content.seek(0)
    return render(
        request,
        'custom-handson-table.html',
        {
            'handsontable_content': content.read()
        })


def embed_handson_table_from_a_single_table(request):
    """
    Renders one table in a handsontable
    """
    content = excel.pe.save_as(
        model=Question,
        dest_file_type='handsontable.html',
        dest_embed=True)
    content.seek(0)
    return render(
        request,
        'custom-handson-table.html',
        {
            'handsontable_content': content.read()
        })


def survey_result(request):
    question = Question.objects.get(slug='ide')
    query_sets = Choice.objects.filter(question=question)
    column_names = ['choice_text', 'votes']

    # Obtain a pyexcel sheet from the query sets
    sheet = excel.pe.get_sheet(query_sets=query_sets,
                               column_names=column_names)
    sheet.name_columns_by_row(0)
    sheet.column.format('votes', int)

    # Transform the sheet into an svg chart
    svg = excel.pe.save_as(
        array=[sheet.column['choice_text'], sheet.column['votes']],
        dest_file_type='svg',
        dest_chart_type='pie',
        dest_title=question.question_text,
        dest_width=600,
        dest_height=400
    )

    return render(
        request,
        'survey_result.html',
        dict(svg=svg.read())
    )


def import_sheet_using_isave_to_database(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST,
                              request.FILES)
        if form.is_valid():
            request.FILES['file'].isave_to_database(
                model=Question,
                mapdict=['question_text', 'pub_date', 'slug'])
            return HttpResponse("OK")
        else:
            return HttpResponseBadRequest()
    else:
        form = UploadFileForm()
    return render(
        request,
        'upload_form.html',
        {'form': form})


def import_data_using_isave_book_as(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST,
                              request.FILES)

        def choice_func(row):
            q = Question.objects.filter(slug=row[0])[0]
            row[0] = q
            return row
        if form.is_valid():
            request.FILES['file'].isave_book_to_database(
                models=[Question, Choice],
                initializers=[None, choice_func],
                mapdicts=[
                    ['question_text', 'pub_date', 'slug'],
                    ['question', 'choice_text', 'votes']]
            )
            return redirect('handson_view')
        else:
            return HttpResponseBadRequest()
    else:
        form = UploadFileForm()
    return render(
        request,
        'upload_form.html',
        {
            'form': form,
            'title': 'Import excel data into database example',
            'header': 'Please upload sample-data.xls:'
        })


def import_without_bulk_save(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST,
                              request.FILES)

        def choice_func(row):
            q = Question.objects.filter(slug=row[0])[0]
            row[0] = q
            return row
        if form.is_valid():
            request.FILES['file'].save_book_to_database(
                models=[Question, Choice],
                initializers=[None, choice_func],
                mapdicts=[
                    ['question_text', 'pub_date', 'slug'],
                    ['question', 'choice_text', 'votes']],
                bulk_save=False
            )
            return redirect('handson_view')
        else:
            return HttpResponseBadRequest()
    else:
        form = UploadFileForm()
    return render(
        request,
        'upload_form.html',
        {
            'form': form,
            'title': 'Import excel data into database example',
            'header': 'Please upload sample-data.xls:'
        })

#  -----------------------------------------------------------------------------------


@login_required
def home(request):
    products = Product.objects.filter(status=True)
    return render(request, 'home.html', {"products": products})


@login_required
def detail(request, id):
    product = Product.objects.get(id=id)
    return render(request, 'detial.html', {"product": product})


@login_required
def addnew(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        print(dir(form))
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProductForm()
    return render(request, 'new.html', {'form': form})


@login_required
def edit(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProductForm(instance=product)
    return render(request, 'edit.html', {'form': form})


@login_required
def document(request):
    product = Product.objects.get(id=1)
    return render(request, 'document.html', {"product": product})


# html2pdf

context = {
    'date': '24 พฤษภาคม 2561',
    'customer_tel': '0859078578',
    'customer_address': 'Bankok',
    'no': 1,
    'contract_no': 'สอ.2/2561',
    'customer_name': 'สมมติ ขึ้นมา',
    'detail_pd': 'Router 892w ',
    'staff_name': 'รัฐกานต์ บันที',
    'count_pd': 1,
    'key_pd': '-',
    'serial_pd': 84003446789236,
    'ref': '-',
    'note': '1กล่อง',
    'range': range(1, 15+1),
}


@login_required
def doc_pdf(request):
    product = Product.objects.get(id=1)

    return render(request, 'doc_pdf.html', context)


@login_required
def view_pdf(request):
    product = Product.objects.get(id=1)
    return render(request, 'hello.html', {"product": product})


'''

def product_search(request):
    products = Product.objects.filter(name__contains = request.GET['product_search'])
    return render(request,'index.html',{"products" : products})
'''


class PDFView(TemplateView):
    #: Set to change the filename of the PDF.
    filename = None

    #: Set to default the PDF display to inline.
    inline = False

    #: Set pdfkit options dict.
    pdfkit_options = None

    def get(self, request, *args, **kwargs):
        """
        Return a HTTPResponse either of a PDF file or HTML.

        :rtype: HttpResponse
        """
        if 'html' in request.GET:
            # Output HTML
            content = self.render_html(*args, **kwargs)
            return HttpResponse(content)

        else:
            # Output PDF
            content = self.render_pdf(*args, **kwargs)

            response = HttpResponse(content, content_type='application/pdf')

            if (not self.inline or 'download' in request.GET) and 'inline' not in request.GET:
                response['Content-Disposition'] = 'attachment; filename=%s' % self.get_filename()

            response['Content-Length'] = len(content)

            return response

    def render_pdf(self, *args, **kwargs):
        """
        Render the PDF and returns as bytes.

        :rtype: bytes
        """
        html = self.render_html(*args, **kwargs)

        options = self.get_pdfkit_options()
        if 'debug' in self.request.GET and settings.DEBUG:
            options['debug-javascript'] = 1

        kwargs = {}
        wkhtmltopdf_bin = os.environ.get('WKHTMLTOPDF_BIN')
        if wkhtmltopdf_bin:
            kwargs['configuration'] = pdfkit.configuration(
                wkhtmltopdf=wkhtmltopdf_bin)

        pdf = pdfkit.from_string(html, False, options, **kwargs)

        return pdf

    def get_pdfkit_options(self):
        """
        Returns ``self.pdfkit_options`` if set otherwise a default dict of options to supply to pdfkit.

        :rtype: dict
        """
        if self.pdfkit_options is not None:
            return self.pdfkit_options

        return {
            'page-size': 'A4',
            'encoding': 'UTF-8',
        }

    def get_filename(self):
        """
        Return ``self.filename`` if set otherwise return the template basename with a ``.pdf`` extension.

        :rtype: str
        """
        if self.filename is None:
            name = splitext(basename(self.template_name))[0]
            return '{}.pdf'.format(name)

        return self.filename

    def render_html(self, *args, **kwargs):
        """
        Renders the template.

        :rtype: str
        """
        static_url = '%s://%s%s' % (self.request.scheme,
                                    self.request.get_host(), settings.STATIC_URL)
        media_url = '%s://%s%s' % (self.request.scheme,
                                   self.request.get_host(), settings.MEDIA_URL)

        with override_settings(STATIC_URL=static_url, MEDIA_URL=media_url):
            template = loader.get_template(self.template_name)
            #context = self.get_context_data(*args, **kwargs)

            html = template.render(context)
            return html


class PDFResponse(HttpResponse):
    """HttpResponse that sets the headers for PDF output."""

    def __init__(self, content, status=200, content_type=None,
                 filename=None, show_content_in_browser=None, *args, **kwargs):

        if content_type is None:
            content_type = 'application/pdf'

        super(PDFResponse, self).__init__(content=content,
                                          status=status,
                                          content_type=content_type)
        self.set_filename(filename, show_content_in_browser)

    def set_filename(self, filename, show_content_in_browser):
        self.filename = filename
        if filename:
            fileheader = 'attachment; filename={0}'
            if show_content_in_browser:
                fileheader = 'inline; filename={0}'

            filename = content_disposition_filename(filename)
            header_content = fileheader.format(filename)
            self['Content-Disposition'] = header_content
        else:
            del self['Content-Disposition']


class PDFTemplateResponse(TemplateResponse, PDFResponse):
    """Renders a Template into a PDF using wkhtmltopdf"""

    def __init__(self, request, template, context=None,
                 status=None, content_type=None, current_app=None,
                 filename=None, show_content_in_browser=None,
                 header_template=None, footer_template=None,
                 cmd_options=None, *args, **kwargs):
        cover_template = kwargs.pop('cover_template', None)

        super(PDFTemplateResponse, self).__init__(request=request,
                                                  template=template,
                                                  context=context,
                                                  status=status,
                                                  content_type=content_type,
                                                  *args, **kwargs)
        self.set_filename(filename, show_content_in_browser)

        self.header_template = header_template
        self.footer_template = footer_template
        self.cover_template = cover_template
        if cmd_options is None:
            cmd_options = {}
        self.cmd_options = cmd_options

    @property
    def rendered_content(self):
        """Returns the freshly rendered content for the template and context
        described by the PDFResponse.

        This *does not* set the final content of the response. To set the
        response content, you must either call render(), or set the
        content explicitly using the value of this property.
        """
        cmd_options = self.cmd_options.copy()
        return render_pdf_from_template(
            self.resolve_template(self.template_name),
            self.resolve_template(self.header_template),
            self.resolve_template(self.footer_template),
            context=self.resolve_context(self.context_data),
            request=self._request,
            cmd_options=cmd_options,
            cover_template=self.resolve_template(self.cover_template)

        )


class PDFTemplateView(TemplateView):
    """Class-based view for HTML templates rendered to PDF."""

    # Filename for downloaded PDF. If None, the response is inline.
    filename = 'rendered_pdf.pdf'

    # Send file as attachement. If True render content in the browser.
    show_content_in_browser = True

    # Filenames for the content, header, and footer templates.
    template_name = None
    header_template = None
    footer_template = None
    cover_template = None

    # TemplateResponse classes for PDF and HTML
    response_class = PDFTemplateResponse
    html_response_class = TemplateResponse

    # Command-line options to pass to wkhtmltopdf
    cmd_options = {

        # 'orientation': 'portrait',
        # 'collate': True,
        # 'quiet': None,
    }

    def __init__(self, *args, **kwargs):
        super(PDFTemplateView, self).__init__(*args, **kwargs)

        # Copy self.cmd_options to prevent clobbering the class-level object.
        self.cmd_options = self.cmd_options.copy()

    def get(self, request, *args, **kwargs):
        response_class = self.response_class
        try:
            if request.GET.get('as', '') == 'html':
                # Use the html_response_class if HTML was requested.
                self.response_class = self.html_response_class
            return super(PDFTemplateView, self).get(request,
                                                    *args, **kwargs)
        finally:
            # Remove self.response_class
            self.response_class = response_class

    def get_filename(self):
        return self.filename

    def get_cmd_options(self):
        return self.cmd_options


        

    def render_to_response(self, context, **response_kwargs):
        """
        Returns a PDF response with a template rendered with the given context.
        """
        filename = response_kwargs.pop('filename', None)
        cmd_options = response_kwargs.pop('cmd_options', None)
        rt = 'Router 892w'
        d = '0000000000000000000000000000000000000000000000000001' \
           # '0000000000000000000000000000000000000000000000000002' \
           # '0000000000000000000000000000000000000000000000000003' \
           # '0000000000000000000000000000000000000000000000000004' 

        # d = '1234567890123456789012345678901234567890123456789012' \
        #     '1234567890123456789012345678901234567890123456789012' \
        #     '1234567890123456789012345678901234567890123456789012' \
        #     '1234567890123456789012345678901234567890123456789012' \
        #     '1234567890123456789012345678901234567890123456789012' \
        #     '1234567890123456789012345678901234567890123456789012'
        d = 'ในปัจจุบันที่การธุรกิจออนไลน์กำลังขยายตัว ทำให้เว็บไซต์อีคอมเมิร์ซ  ร้านค้าออนไลน์ และโซเชียลเน็ตเวิร์กต่างมีจำนวนผู้ขายเพิ่มขึ้นอย่างมาก การที่มีผู้ขายในตลาดเพิ่มมากขึ้นนั้นดีต่อผู้ซื้อเพราะผู้ซื้อสามารถเปรียบเทียบและเลือกซื้อสินค้าจากผู้ขายที่มีคุณภาพได้ตามต้องการ แต่การตัดสินใจเลือกซื้อสินค้าในร้านใดร้านหนึ่งย่อมต้องมีเงื่อนไขประกอบการเลือกซื้อมากขึ้น'    
            #  0000000000000000000000000000000000000000000000000000
        d = 'ในปัจจุบันที่การธุรกิจออนไลน์กำลังขยายตัว ทำให้เว็บไซต์อีคอมเมิร์ซ  ร้านค้าออนไลน์ และโซเชียลเน็ตเวิร์กต่างมีจำนวนผู้ขายเพิ่มขึ้นอย่างมาก'  
        # 
        #   
        # -----------------------------------------------------------    
        # n = 52
        # r = [d[i:i + n] for i in range(0, len(d), n)]
        def vowel_indices(s):
            res = []
            index = 0

            for vowel in s:
                index += 1

                if vowel.lower() in '่๋็้ี๊ัํึื์ิฺุู':
                    res.append(index)

            return res

        def count_n(s):
            res = []
            index = 0
            for n in s:
                index += 1
                res.append(index)
            return res

        a=count_n(d)
        b=vowel_indices(d)

        n_vowel = []
        ind = 0
        vowel = 0
        for i in a:
            if i in b :
                ind = ind
                vowel += 1

            else:
                ind += 1
                n_vowel.append(i)




        n=[]
        for i in range(1,1+len(n_vowel)//52) :
             n.append(n_vowel[52*i-1])


        r = []
        i=0
        for j in n :
            r.append(d[i:j])
            i = j
    # -----------------------------------------------------------    
        ele = 50
        n_line = len(r)
        tot_line = n_line * ele
        line1page = 18

        footEle = line1page//n_line
        foot = ele//3
        ar = []
        for i in range(1, foot + 1):
            ar.append(i * footEle)



        context = {
            'date': '24 พฤษภาคม 2561',
            'customer_tel': '0859078578',
            'customer_address': 'Bankok',
            'no': 1,
            'contract_no': 'สอ.2/2561',
            'customer_name': 'สมมติ ขึ้นมา',
                    'detail_pd': r,
                    'staff_name': 'รัฐกานต์ บันที',
                    'count_pd': 1,
                    'key_pd': '-',
                    'serial_pd': 84003446789236,
                    'ref': '-',
                    'note': '1กล่อง',
                    'range': range(1, 50+1),
                    'nb': ar,#[18, 36, 54, 72, 90],
                }

        for i in range(len(r)):
            context[i] = r[i]

        if issubclass(self.response_class, PDFTemplateResponse):
            if filename is None:
                filename = self.get_filename()

            if cmd_options is None:
                cmd_options = self.get_cmd_options()

            return super(PDFTemplateView, self).render_to_response(
                context=context, filename=filename,
                show_content_in_browser=self.show_content_in_browser,
                header_template=self.header_template,
                footer_template=self.footer_template,
                cmd_options=cmd_options,
                cover_template=self.cover_template,
                **response_kwargs
            )
        else:
            return super(PDFTemplateView, self).render_to_response(
                context=context,
                **response_kwargs
            )


def display(request):
    return render_to_response('table.html', {'obj': Product.objects.all()})


#   def home(request):
#     products = Product.objects.filter(status=True)
#     return render(request,'home.html',{"products" : products})


def mail(request):
   # if request.method == "POST":
    send_mail('Subject here', 'Here is the message.', 'from@example.com', [
              'aonchicken@gmail.com'], fail_silently=False)
    messages.success(request, "Thank you. Email is Sent")
    return render(request, 'document.html', {})
