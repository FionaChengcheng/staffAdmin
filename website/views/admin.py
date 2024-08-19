from django.shortcuts import render, redirect
from django import forms
from django.core.exceptions import ValidationError

from website import models
from website.utils.pagination import Pagination
from website.utils.bootstrap import BootStrapModelForm
from website.utils.encrypt import md5


class AdminModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True)
    )

    class Meta:
        model = models.Admin
        fields = ["username", "password", "confirm_password"]
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }

    def clean_password(self):
        pwd = self.cleaned_data.get("password")

        return md5(pwd)

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if confirm != pwd:
            raise ValidationError("密码不一致")
        # 返回值是此字段保存到数据库的值
        return confirm


def admin_list(request):
    queryset = models.Admin.objects.all()
    return render(request, 'admin_list.html', {"queryset": queryset})


def admin_add(request):
    """ 添加管理员 """
    title = "新建管理员"
    if request.method == "GET":
        form = AdminModelForm()
        return render(request, 'change.html', {'form': form, "title": title})
    form = AdminModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')

    return render(request, 'change.html', {'form': form, "title": title})


def admin_edit(request):
    title = "编辑管理员"
    if request.method == "GET":
        form = AdminModelForm()
        return render(request, 'change.html', {'form': form, "title": title})
    form = AdminModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')

    return render(request, 'change.html', {'form': form, "title": title})


def admin_delete(request, nid):
    models.Admin.objects.filter(id=nid).delete()
    return redirect('/admin/list/')

