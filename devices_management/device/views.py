from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect, render_to_response
from django.conf import settings
from device.form import addForm, bookForm, editForm, bookFormAdmin, sttForm, suppForm, prjForm
from .models import devices, order, Project, supplement
from django.contrib.auth.decorators import login_required
from account.decorators import bse_required, ad_required, ns_required
from django.http import Http404, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
@login_required
def listdevices(request):
    device_list = devices.objects.all()
    paginator = Paginator(device_list, 5)

    pageNumber = request.GET.get('page')
    try:
        device = paginator.page(pageNumber)
    except PageNotAnInteger:
        device = paginator.page(1)
    except EmptyPage:
        device = paginator.page(paginator.num_pages)

    return render(request, 'device/listdevices.html', {'devices': device})


@login_required
def search(request):
    if request.method == "GET":

        if 'srh' in request.GET and request.GET['srh']:
            srch = request.GET['srh']
            match = devices.objects.filter(Q(code__icontains=srch) |
                                           Q(name__icontains=srch) |
                                           Q(type__icontains=srch) |
                                           Q(osType__icontains=srch) |
                                           Q(version__icontains=srch) |
                                           Q(keeper__username__icontains=srch) |
                                           Q(project__name__icontains=srch) |
                                           Q(bookedFrom__icontains=srch) |
                                           Q(bookedTo__icontains=srch) |
                                           Q(status__icontains=srch)
                                           )
            if match:

                search_list = match.all()
                paginator = Paginator(search_list, 5)

                pageNum = request.GET.get('page')
                try:
                    md = paginator.page(pageNum)
                except PageNotAnInteger:
                    md = paginator.page(1)
                except EmptyPage:
                    md = paginator.page(paginator.num_pages)
                return render(request, 'device/listdevices.html', {'sr': md, 'ct': srch})
            else:
                messages.error(request, 'no result found')
        else:
            return HttpResponseRedirect('/listdevices/')
    return render(request, 'device/listdevices.html')


@ad_required
@login_required
def add(request):
    form = addForm()
    if request.method == 'POST':
        form = addForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/listdevices')
    return render(request, 'device/add.html', {'form': form})


@login_required
def book(request, id):
    if id == 0:
        form = bookForm()
    else:
        device = devices.objects.get(id=id)
        form = bookForm(initial={'code': device.code})

    if request.method == 'POST':
        form = bookForm(request.POST)
        keeper = request.POST['keeper']
        user = User.objects.get(username=keeper)
        if form.is_valid():
            form.save(user.id)
            return redirect('/book/' + str(id))

    return render(request, 'device/bookDeviceAdmin.html', {'form': form, 'id': id})


@ad_required
def bookAdmin(request, id):
    if id == 0:
        form = bookFormAdmin()
    else:
        device = devices.objects.get(id=id)
        form = bookFormAdmin(initial={'code': device.code})
    if request.method == 'POST':
        form = bookFormAdmin(request.POST)
        if form.is_valid():
            form.update()
            return redirect('/bookAdmin/' + str(id))

    return render(request, 'device/bookDeviceAdmin.html', {'form': form, 'id': id})


@ad_required
@login_required
def edit(request, id):
    device = devices.objects.get(id=id)
    if device.status=='Free' or device.status=='Out of Stock':
        form = editForm(initial={'code': device.code,
                                 'name': device.name,
                                 'type': device.type,
                                 'os_Type': device.osType,
                                 'version': device.version,
                                 'status': device.status})
    else:
        form = editForm(initial={'code': device.code,
                                 'name': device.name,
                                 'type': device.type,
                                 'os_Type': device.osType,
                                 'version': device.version})

    if request.method == 'POST' and 'btnform1' in request.POST:
        form = editForm(request.POST)
        if form.is_valid():
            form.edit(id)
            return redirect('/listdevices')

    if request.method == 'POST' and 'btnform2' in request.POST:
        device.delete()
        return redirect('/listdevices')

    return render(request, 'device/edit.html', {'form': form, 'device': device, 'id': id})


@ad_required
def orderlists(request):
    orders_list = order.objects.all().order_by('-orderFrom')
    form = sttForm()
    if request.method == 'POST' and 'confirmorder' in request.POST:
        form = sttForm(request.POST)
        orderid = request.POST['orderid']
        stt = 'Confirmed'
        form.updatestt(orderid, stt)
        form.confirm(orderid)
    if request.method == 'POST' and 'rejectorder' in request.POST:
        orderid = request.POST['orderid']
        stt = 'Rejected'
        form.updatestt(orderid, stt)
        form.reject(orderid)

    return render(request, 'device/listorders.html', {'orders': orders_list, 'form': form})


@ns_required
def mydevices(request):
    device_list = devices.objects.all()
    return render(request, 'device/mydevices.html', {'devices': device_list})


@ns_required
def myorders(request):
    order_list = order.objects.all()
    return render(request, 'device/myorders.html', {'orders': order_list})


@bse_required
def addsup(request):
    form = suppForm()
    if request.method == 'POST':
        form = suppForm(request.POST)
        suppu = request.POST['suppu']
        user = User.objects.get(username=suppu)
        if form.is_valid():
            form.save(user.id)
            return redirect('/addsup/')
    return render(request, 'device/addsup.html', {'form': form})


@ad_required()
def supplistadmin(request):
    supp_list = supplement.objects.all()
    return render(request, 'device/supplistadmin.html', {'supps': supp_list})


@bse_required
def mysupps(request):
    supp_list = supplement.objects.all()
    return render(request, 'device/mysupps.html', {'supps': supp_list})

@ad_required
def addprj(request):
    form = prjForm()
    if request.method == 'POST':
        form = prjForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/addprj')
    return render(request, 'device/addprj.html', {'form': form})
