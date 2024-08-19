from django.shortcuts import render, redirect
from website import models


def depart_list(request):
    queryset = models.Department.objects.all()
    # 取到一个个对象（数据后），去html中循环
    return render(request, 'depart_list.html', {'queryset': queryset})


def depart_add(request):
    if request.method == "GET":
        return render(request, 'depart_add.html')
    title = request.POST.get("title")

    models.Department.objects.create(title=title)

    return redirect("/depart/list/")


def depart_delete(request):
    nid = request.GET.get('nid')
    models.Department.objects.filter(id=nid).delete()
    return redirect("/depart/list/")


def depart_edit(request, nid):
    if request.method == "GET":
        row = models.Department.objects.filter(id=nid).first()
        return render(request, 'depart_edit.html', {"row": row})

    title = request.POST.get("title")
    models.Department.objects.filter(id=nid).update(title=title)
    return redirect("/depart/list/")
