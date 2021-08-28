import json
import re

from django.shortcuts import redirect, render
from django.http import HttpResponse, response
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.utils.safestring import mark_safe

from util import mongoClient


@login_required(login_url='/login')  # redirect when user is not logged in
def index(request):
    all_data = mongoClient.find_(request.user.id)['to_do_list']
    if len(all_data) == 0:
        all_data = None
    else:
        pass
    return render(request, 'index.html', {'data_context':all_data})

@login_required(login_url='/login')  # redirect when user is not logged in
@csrf_exempt
def new_to_do_list(request): # here we will add new car to the db
    redi = 'index'
    if request.method == 'POST':
        if 'submit-record' in request.POST:
            dataName = request.POST['dataName']
            dataList = request.POST['dataList']
            if len(dataName) == 0:
                messages.error(request, "You can't leave name blank")
                return redirect(redi)
            else:
                mongoClient.add_to_do(request.user.id, dataName, dataList)
                messages.success(request, mark_safe(f"New data '<strong>{dataName}</strong>' has been added"))
                return redirect(redi)
        else:
            payload = json.loads(request.body)
            dataName = payload['dataName']
            dataList = payload['dataList']
            try:
                response  = json.dumps([{'SUCCESS' : f'New record "{dataName}" has been added'}])
                return HttpResponse(response, content_type = 'text/json')
            except:
                response = json.dumps([{'ERROR':'Something went wrong :( please try again'}])
                return HttpResponse(response, content_type = 'text/json')
    else:
        return HttpResponse('Try to POST me!')

@login_required(login_url='/login')  # redirect when user is not logged in
@csrf_exempt
def del_data(request): # here we will add new car to the db
    redi = redirect('index')
    if request.method == 'POST':
        if 'del-single-item' in request.POST: # this for delete single record 
            data_id = request.POST['del-single-item']
            data_name = mongoClient.find_data(request.user.id, data_id, 'to_do_list')['to_do_list']
            for data_details in data_name:
                pass
            mongoClient.remove_data(request.user.id, data_id, 'to_do_list')
            messages.success(request, mark_safe(f"Data '<strong>{data_details['dataName']}</strong>' has been deleted successfully"))
            return redi

        if 'del-all-finished' in request.POST: # this for deleting all the finished data 
            all_data = mongoClient.find_(request.user.id)['to_do_list']
            for data in all_data:
                if data['isFinished']:
                    mongoClient.remove_data(request.user.id, data['dataID'], 'to_do_list')
                    messages.success(request, mark_safe(f"Data '<strong>{data['dataName']}</strong>' has been deleted successfully"))
            return redi

        if 'del-all-un-finished' in request.POST: # this for delete all un finished data
            all_data = mongoClient.find_(request.user.id)['to_do_list']
            for data in all_data:
                if data['isFinished'] == False:
                    mongoClient.remove_data(request.user.id, data['dataID'], 'to_do_list')
                    messages.success(request, mark_safe(f"Data '<strong>{data['dataName']}</strong>' has been deleted successfully"))
            return redi

        if 'del-all' in request.POST: # this will delete all the data
            all_data = mongoClient.find_(request.user.id)['to_do_list']
            for data in all_data:
                mongoClient.remove_data(request.user.id, data['dataID'], 'to_do_list')
                messages.success(request, mark_safe(f"Data '<strong>{data['dataName']}</strong>' has been deleted successfully"))
            return redi

    else:
        return redi

@login_required(login_url='/login')  # redirect when user is not logged in
@csrf_exempt 
def handle_data(request):
    redi = redirect('index')
    if request.method == 'POST': 
        if 'check_finished' in request.POST: # this for update the data and make it checked or not
            data_id = request.POST['check_finished']
            data_stat = mongoClient.find_data(request.user.id, data_id, 'to_do_list')['to_do_list']
            for data in data_stat:
                pass
            if data['isFinished']:
                data_context = {
                    'isFinished':False
                }
                mongoClient.update_data(request.user.id, data_id, 'to_do_list', **data_context)
                return redi
            if data['isFinished'] == False:
                data_context = {
                    'isFinished':True
                }
                mongoClient.update_data(request.user.id, data_id, 'to_do_list', **data_context)
                return redi
        if 'update-si0Data-btn' in request.POST:
            data_id = request.POST['update-si0Data-btn']
            dataName = request.POST['data-name-view-stage']
            dataList = request.POST['data-list-view-stage']
            data = {
                'dataName':dataName, 
                'list':dataList,
            }

            mongoClient.update_data(request.user.id, data_id, 'to_do_list', **data)
            messages.success(request, mark_safe(f"Data '<strong>{dataName}</strong>' has been updated"))
    return redi

@login_required(login_url='/login')  # redirect when user is not logged in
def get(request, data_id):
    if request.method == 'GET':
        try:
            all_data = mongoClient.find_data(request.user.id, data_id, 'to_do_list')['to_do_list']
            for data in all_data:
                pass
            data_context = [
                {
                    'dataID':data['dataID'],
                    'dataName':data['dataName'],
                    "isFinished":data['isFinished'],
                    "list":data['list']
                }
            ]
            response = json.dumps(data_context)
        except:
            response = json.dumps([{'ERROR':'DATA NOT FOUND'}])
        return HttpResponse(response, content_type = 'text/json')

@login_required(login_url='/login')  # redirect when user is not logged in
def search(request, query):
    if request.method == 'GET':
        data_query = request.GET.get('q', '')
        if len(data_query) == 0:
            messages.info(request,"You can't search for an empty string")
            return redirect('index')
        else:
            if 'q' in request.GET:
                pass # that means we can still accebt the request from the user 
            else: # this will check that the search is not valid and then will return empty data
                resp_msg = [{
                    'ERROR': 'NOT A VALID WAY TO SEARCH'
                }]
                response = json.dumps(resp_msg)
                return HttpResponse(response, content_type = 'text/json')
                
            query_list = [] # will use this to store the data to work with in the end
            found_data = [] # will store the stored data to display

            all_data = mongoClient.find_(request.user.id)['to_do_list']

            for data in all_data:
                query_list.append(
                    {
                        'dataID':data['dataID'],
                        'dataName':data['dataName']
                    }
                )
                x = re.findall(data_query.lower(), data['dataName'].lower())
                if len(x) == 0:
                    pass
                else:
                    
                    found_data.append(
                        {
                            'dataID':data['dataID'],
                            'dataName':data['dataName'],
                            'isFinished':data['isFinished'],
                            'list':data['list'],
                        },
                    )
            
            if len(found_data) == 0: # this will check if the data was not found
                pass
                found_data = [{
                    'ERROR': 'NO DATA FOUND'
                }]
                if 'frm-search' in request.GET: # that means that the request was from our template not a server get request so we will render a template
                    found_data = None
                    return render(request, 'search.html', {'data_context':found_data, 'search_query':data_query})
                else:
                    response = json.dumps(found_data)
                    return HttpResponse(response, content_type = 'text/json')
            else:
                if 'frm-search' in request.GET: # that means that the request was from our template not a server get request so we will render a template
                    return render(request, 'search.html', {'data_context':found_data})
                else:
                    pass # we will pass that the user can get the get request json data
            response = json.dumps(found_data)
            return HttpResponse(response, content_type = 'text/json') # this will return the data as json data