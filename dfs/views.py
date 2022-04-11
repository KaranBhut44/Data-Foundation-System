from http.client import HTTPResponse
from django.http import FileResponse, HttpResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Approved_req, Dataset_info, Pending_req, Rejected_req, user_details

# dataset1link = "https://docs.google.com/spreadsheets/d/1c4TeZFFueJHsedVSSyIKA2-tHSMut6jE/edit?usp=sharing&ouid=103453030291973279123&rtpof=true&sd=true"
# dataset1link = "https://docs.google.com/spreadsheets/d/1l_mVbz3LiFocOTNvVrUWFXTl_YjEYntIJCTRLRkm2U8/edit?usp=sharing"
# dataset2link = "https://docs.google.com/spreadsheets/d/12uEkgD-hdvibspl6_S7BLimq-LiElwmV/edit?usp=sharing&ouid=103453030291973279123&rtpof=true&sd=true"
# dataset3link = "https://docs.google.com/spreadsheets/d/1M8Vhi5_NFpeXwM1QyC8c40J9tz4vuWSy/edit?usp=sharing&ouid=103453030291973279123&rtpof=true&sd=true"
# dataset4link = "https://docs.google.com/spreadsheets/d/1aYIbMnWsDMnMYJ-c-gbTl9EFtCotRt6A/edit?usp=sharing&ouid=103453030291973279123&rtpof=true&sd=true"
# datasets_links = [dataset1link,dataset2link,dataset3link,dataset4link]

user_data = []
admin_result = []
own_datasets =[]
datasets_info = dict()
username = ""

class MyStruct():
    def __init__(self, field1, field2, field3):
        self.field1 = field1
        self.field2 = field2
        self.field3 = field3

class AdminData():
    def __init__(self, field1, field2):
        self.dname = field1
        self.cname = field2

def validate(req):
    name = req.POST['name']
    password = req.POST['password']
    flag = True
    
    try:
        oldRow = user_details.objects.get(name = name,password=password)
    except:
        errorMessage = "Wrong Credentials"
        return render(req, 'login.html', {'error': errorMessage})
    
    global username
    username = name
    return redirect(home)

def validateRegistration(req):
    name = req.POST['name']
    password = req.POST['password']
    cpassword = req.POST['cpassword']

    if(password != cpassword):
        errorMessage = "Password and Confirm password don't match"
        return render(req, 'registration.html', {'error': errorMessage})
    newRow = user_details(name=name, password=password)
    newRow.save()
    global username

    username = name
    return home(req)


def registration(req):
    return render(req, 'registration.html')

def login(req):
    return render(req, 'login.html')

def logout(req):
    global username
    username=""
    return redirect(login)

def add_date_time(lst):
    global datasets_info
    global username
    updated_list = []

    for item in lst:
        updated_list.append([item[0],datasets_info[item[0]][1],item[1]])

    final_list = []
    for item in updated_list:
        mystruct = MyStruct(item[0],item[1],item[2])
        final_list.append(mystruct)
    
    requests = [x[0] for x in lst]
    for item in datasets_info.keys():
        if item not in requests:
            if(datasets_info[item][0] != username):
                mystruct = MyStruct(item,datasets_info[item][1],"Not requested")
                final_list.append(mystruct)
    return final_list

def load_data():
    global datasets_info
    global user_data
    user_data = []
    datasets_info.clear()
    allpending = Pending_req.objects.all()
    allrejected = Rejected_req.objects.all()
    allapproved = Approved_req.objects.all()
    datasets_info_list = Dataset_info.objects.all()

    for item in datasets_info_list:
        datasets_info[item.dname] = [item.author,item.date_time,item.link]

    pending,approved,rejected = [],[],[]

    for req in allpending:
        if req.cname == username:
            pending.append([req.dname,"Pending"])

    for req in allapproved:
        if req.cname == username:
            approved.append([req.dname,"Approved"])

    for req in allrejected:
        if req.cname == username:
            rejected.append([req.dname,"Rejected"])
    
    relevant_list = approved
    relevant_list.extend(pending)
    relevant_list.extend(rejected)
    user_data = add_date_time(relevant_list)

def home(request):
    global username
    if(username == ""):
        return redirect(login)
    load_data()
    global user_data
    return render(request, "home.html", {'datasets': user_data})

def download(req,id):
    id -= 1
    global datasets_info
    datasetName = user_data[id].field1
    datasetPath = datasets_info[datasetName][2]
    return redirect(datasetPath)

def cancelReq(req,id):
    id -= 1
    global username
    global user_data
    oldRow = Pending_req.objects.get(dname = user_data[id].field1, cname=username)
    oldRow.delete()
    return redirect(home)

def requestDataset(req,id):
    id -= 1
    global username
    global user_data
    newRow = Pending_req(dname=user_data[id].field1, cname=username)
    newRow.save()
    return redirect(home)

def load_admin_info(admin):
    all_datasets = Dataset_info.objects.all()
    global own_datasets
    own_datasets = []
    for dataset in all_datasets:
        if(dataset.author == admin):
            own_datasets.append(dataset.dname)

    allpending = Pending_req.objects.all()
    global admin_result
    admin_result = []
    for req in allpending:
        if req.dname in own_datasets:
            obj1 = AdminData(req.dname,req.cname)
            admin_result.append(obj1)

def adminPanel(req):
    global username
    load_admin_info(username)
    return render(req,"admin.html",{"requests":admin_result})

def acceptReq(req,id):
    id -= 1
    newRow = Approved_req(dname=admin_result[id].dname, cname=admin_result[id].cname)
    newRow.save()
    oldRow = Pending_req.objects.get(dname = admin_result[id].dname)
    oldRow.delete()
    return redirect(adminPanel)

def rejectReq(req,id):
    id -= 1
    newRow = Rejected_req(dname=admin_result[id].dname, cname=admin_result[id].cname)
    newRow.save()
    oldRow = Pending_req.objects.get(dname = admin_result[id].dname)
    oldRow.delete()
    return redirect(adminPanel)