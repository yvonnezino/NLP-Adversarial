from django.shortcuts import render
from django.http import HttpResponse
from django import forms

class NewForm(forms.Form):
    inputText = forms.CharField(widget=forms.Textarea, label='')

def index(request):
    
    if request.method == "POST":
        # Take in the data the user submitted and save it as form
        givenText = NewForm(request.POST)
        textInputted=True
        return render(request, "AdversarialTool/index.html", {
        "form":NewForm(), "textInputted":textInputted, "givenText":givenText
    })
    else:
        return render(request, "AdversarialTool/index.html", {
            "form":NewForm(), "textInputted":False, "givenText":""
        })
