from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from .models import Room
import json
# Create your views here.


def check(request):
    try:
        request.session['room']
    except Exception as e:
        request.session['room'] = None
    try:
        request.session['use_name']
    except Exception as e:
        request.session['use_name'] = None


def home(request):
    check(request)
    if request.session['room'] == None:
        if request.method == 'POST':
            my_name = request.POST.get('name')
            room = request.POST.get("room_name")
            if my_name != '' and room != '':
                my_room = Room.objects.filter(name=room)
                if len(my_room) <= 0:
                    my_name = my_name.lower()
                    my_roomie = Room.objects.create(
                        name=room, users=json.dumps({"all": [my_name.lower()]}), messages=json.dumps({'mess': [[]]}))
                    my_roomie.save()
                    request.session['room'] = str(room).capitalize()
                    request.session['use_name'] = my_name
                else:
                    frill = my_room[0].users
                    frill = frill.replace("\'", "\"")
                    frill = json.loads(frill)
                    print(frill, my_name)
                    if my_name not in frill['all']:
                        frill['all'].append(my_name.lower())
                    my_room.update(users=json.dumps(frill))
                    request.session['room'] = str(room).capitalize()
                    request.session['use_name'] = my_name
                return redirect(f"rooms/{request.session['room']}")
        return render(request, "home.html")
    else:
        return redirect(f"rooms/{request.session['room']}")


def request_check(request):
    is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
    return is_ajax


def leave(request):
    my_room = Room.objects.filter(name=request.session['room'].lower())
    if len(my_room) > 0:
        frill = my_room[0].users.replace("\'", "\"")
        frill = json.loads(frill)
        frillo = frill['all']
        print(len(frillo))
        for i in range(len(frillo)):
            print(frillo)
            if frillo[i].lower() == request.session['use_name'].lower():
                frillo.pop(i)
                break
        if len(frillo) <= 0:
            my_room.delete()
        else:
            frill['all'] = frillo
            my_room.update(users=json.dumps(frill))
            my_room[0].save()
        request.session['room'] = None
        request.session['use_name'] = None
        request.build_absolute_uri('')
        return redirect('/')
    else:
        request.session['room'] = None
        request.session['use_name'] = None
        request.build_absolute_uri('')
        return redirect('/')


def sender(request):
    check(request)
    if request.session['room'] != None:
        if request_check(request):
            my_message = request.POST.get("message")
            muted = Room.objects.filter(name=request.session['room'].lower())
            my_dict = json.loads(muted[0].messages)
            my_dict['mess'].append(
                [request.session['use_name'], my_message])
            muted.update(messages=json.dumps(my_dict))
            return JsonResponse({'drax': muted[0].messages})
        else:
            request.build_absolute_uri('')
            return redirect('/')
    else:
        request.build_absolute_uri('')
        return redirect('/')


def getter(request):
    check(request)
    if request.session['room'] != None:
        if request_check(request):
            mess = Room.objects.filter(name=request.session['room'].lower())
            if len(mess) > 0:
                my_dict = json.loads(mess[0].messages)['mess']
                my_str = mess[0].users.replace('\'', '\"')
            else:
                my_dict = {}
                my_str = json.dumps([])
            my_str = json.loads(my_str)
            return JsonResponse({'mess': my_dict, 'mayor': my_str})
        else:
            request.build_absolute_uri('')
            return redirect('/')
    else:
        request.build_absolute_uri('')
        return redirect('/')


def handle(request, slug):
    if request.session['room'] == slug:
        context = {
            'room_name': request.session['room']
        }
        return render(request, "chatting.html", context)
    else:
        request.build_absolute_uri('')
        return redirect('/')
