from django.shortcuts import render

def testView(request):
    return render(request, 'main/test.html')
