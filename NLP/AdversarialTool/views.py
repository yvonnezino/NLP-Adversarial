from django.shortcuts import render
import numpy as np
from django.http import HttpResponse
from django import forms
from AdversarialTool.ml_test import predict 

class NewForm(forms.Form):
    inputText = forms.CharField(widget=forms.Textarea, label='')

def index(request):
    
    if request.method == "POST":
        # Take in the data the user submitted and save it as form
        givenText = request.POST.get("inputText")
        textInputted=True
        a_list = givenText.split()
        map_object = map(int, a_list)
        list_of_integers = list(map_object)

        classifiedText=predict(np.array(list_of_integers))
        print(classifiedText)
        return render(request, "AdversarialTool/index.html", {
        "form":NewForm(), "textInputted":textInputted, "givenText":classifiedText, "classification":classifiedText
    })
    else:
        return render(request, "AdversarialTool/index.html", {
            "form":NewForm(), "textInputted":False, "givenText":""
        })
