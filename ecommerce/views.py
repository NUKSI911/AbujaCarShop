from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,get_user_model
from .forms import ContactForm


def home_page(request):
	# return HttpResponse("<h1>Hello world</h1>")
	context={
	 'title':'ABUJA CAR SHOP',
	 "content":"Welcome tothe official Website"
	 	}
	if request.user.is_authenticated():
		context["premium_content"]="YEAHHHHHH"
	return render(request,'home_page.html',context)


def about_page(request):
    context = {
        "title":"About Page",
        "content":" Welcome to the about page."
    }
    return render(request, "home_page.html", context)


def service_page(request):
	# return HttpResponse("<h1>Hello world</h1>")

	return render(request,'service_page.html',{})

def contact_page(request):
        contact_form = ContactForm(request.POST or None)
        context ={
            "title":"Contact",
            "content":" Welcome to the contact page.",
            "form": contact_form,
        }
        if contact_form.is_valid():
            print(contact_form.cleaned_data)
            if request.is_ajax():
                return JsonResponse({"message": "Thank you for your submission"})
        if contact_form.errors:
            errors = contact_form.errors.as_json()
            if request.is_ajax():
                return HttpResponse(errors, status=400, content_type='application/json')
        return render(request,'contact/view.html',context)
