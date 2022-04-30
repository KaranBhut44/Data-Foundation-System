from django.http import HttpResponse
from operator import truediv
from django.http import FileResponse, HttpResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Approved_req, Dataset_info, Pending_req, Rejected_req, user_details

user_data = []
admin_result = []
own_datasets =[]
datasets_info = dict()
username = ""
current_dataset = ""

class MyStruct():
    def __init__(self, field1, field2, field3):
        self.field1 = field1
        self.field2 = field2
        self.field3 = field3

class AdminData():
    def __init__(self, field1, field2,field3,field4):
        self.dname = field1
        self.date = field2
        self.access = field3
        self.UA = field4

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
        datasets_info[item.dname] = [item.author,item.date_time,item.link,item.access_type,item.need_UA,item.UA]

    pending,approved,rejected = [],[],[]

    for item in datasets_info_list:
        if item.access_type == "public":
            approved.append([item.dname,"Approved"])
    
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
    return render(request, "home.html", {'datasets': user_data, 'UA': ""})

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
    global datasets_info
    access_type = datasets_info[user_data[id].field1][4]
    UA_description = datasets_info[user_data[id].field1][5]
    if(access_type == "yes"):
        return render(req, "home.html", {'datasets': user_data ,'UA':UA_description,'Id':id})
    return redirect(send_req,id)

def send_req(req,id):
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
            own_datasets.append(AdminData(dataset.dname,dataset.date_time,dataset.access_type,dataset.need_UA))

def adminPanel(req):
    global username
    load_admin_info(username)
    global own_datasets
    return render(req,"admin.html",{"requests":own_datasets})

def acceptReq(req,id):
    id -= 1
    global current_dataset
    global consumers

    newRow = Approved_req(dname=current_dataset, cname=consumers[id])
    newRow.save()
    oldRow = Pending_req.objects.get(dname=current_dataset, cname=consumers[id])
    oldRow.delete()
    return redirect(adminPanel)

def rejectReq(req,id):
    id -= 1
    global current_dataset
    global consumers
    
    newRow = Rejected_req(dname=current_dataset, cname=consumers[id])
    newRow.save()
    oldRow = Pending_req.objects.get(dname=current_dataset, cname=consumers[id])
    oldRow.delete()
    return redirect(adminPanel)


def viewConsumers(requ,id):
    id -= 1
    global own_datasets
    global consumers
    global current_dataset

    current_dataset = own_datasets[id].dname
    allAccepted = Approved_req.objects.all()

    consumers = [] 
    for req in allAccepted:
        if req.dname == current_dataset:
            consumers.append(req.cname)

    return render(requ,"consumers.html",{"consumers":consumers})

def performChanges(req):
    access = req.POST['access']
    UA_needed = req.POST['need']
    UA = req.POST['UA']

    global current_dataset

    newRow = Dataset_info.objects.get(dname=current_dataset)
    newRow.access_type = access
    newRow.need_UA = UA_needed
    newRow.UA = UA
    newRow.save()
    load_admin_info(username)
    return redirect(adminPanel)

def modify(req,id):
    id -= 1
    global current_dataset
    global own_datasets
    current_dataset = own_datasets[id].dname
    

    return render(req,"admin.html",{"modified":"yes","current_dataset":current_dataset,"requests":own_datasets})

def viewRequests(requ,id):
    id -= 1
    global own_datasets
    global consumers
    global current_dataset

    current_dataset = own_datasets[id].dname
    print("current dataset", current_dataset)

    allpending = Pending_req.objects.all()

    consumers = [] 
    for req in allpending:
        if req.dname == current_dataset:
            consumers.append(req.cname)

    return render(requ,"requestList.html",{"consumers":consumers})

def revokeAccess(req,id):
    id -= 1
    global consumers
    global current_dataset

    newRow = Rejected_req(dname=current_dataset, cname=consumers[id])
    newRow.save()
    oldRow = Approved_req.objects.get(dname = admin_result[id].dname, cname=consumers[id])
    oldRow.delete()

def consumer_has_access(req,dname,cname):
    req_list = Approved_req.objects.all()
    for req in req_list:
        if(req.dname == dname and req.cname == cname):
            return HttpResponse("yes")
    return HttpResponse("no")