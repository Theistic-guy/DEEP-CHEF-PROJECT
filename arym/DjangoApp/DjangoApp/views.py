from django.http import HttpResponse
from django.shortcuts import render
import base64
import imghdr
def home(request):
    return render(request,'home.html')

def analyze(request):
    uploaderName= request.POST.get('hiddenElement')
    if uploaderName == "":
        return HttpResponse("No image selected")
    else:
        if uploaderName in request.FILES:
            uploadedFile = request.FILES[uploaderName]
            binary_content = uploadedFile.read()
            params = {'toAlert':False}
            img_type = imghdr.what(None,h=binary_content)
            if img_type == None:
                return HttpResponse("Uploaded file is not recognized as an image")
            if img_type != 'jpeg':
                params['toAlert'] = True
            base64_encoded_data = base64.b64encode(binary_content).decode('ascii')
            dataURL = f'data:image/{img_type};base64,{base64_encoded_data}'
            params['dataURL'] = dataURL
            
            return render(request,'analyze.html',params)
        else:
            return HttpResponse("No image selected")