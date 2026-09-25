from django.shortcuts import render, redirect
from .forms import ProductModelForm
from .models import Product
from django.template.loader import render_to_string, get_template
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from io import BytesIO
from xhtml2pdf import pisa
from django.http import HttpResponse
from django.utils.html import strip_tags
from django.core.mail import send_mail

# Create your views here.


def home(request):
    data = Product.objects.all()
    return render(request, 'home.html', {'data': data})


def add(request):
    if request.method == 'POST':
        form = ProductModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProductModelForm()
    return render(request, 'add.html', {'form': form})


def email(request, id):
    product = Product.objects.get(pk=id)

    subject = f"New Product Added {product.name}"
    from_email = "user123@gmail.com"
    recipient_list = ["your_mailtrap_inbox@mailtrap.io"]
    html_message = render_to_string('email.html', {'product': product})
    plain_message = strip_tags(html_message)
    send_mail(subject, plain_message, from_email,
              recipient_list, html_message=html_message)
    return redirect('home')


def pdf(request, id):
    product = get_object_or_404(Product, pk=id)

    template = get_template('pdf.html')
    html = template.render({'product': product})

    buffer = BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=buffer)

    if pisa_status.err:
        return HttpResponse('PDF creation error!')
    else:
        response = HttpResponse(
            buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="{}.pdf"'.format(
            product.name)
        return response
