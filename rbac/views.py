from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from account.forms import RegistrationForm, UserInfoForm
from rbac.forms import RoleForm
from rbac.models import Permission, Menu, Role, User, UserInfo

@csrf_exempt
def permission(request):
    if request.method == "GET":
        permission_list = Permission.objects.all()
        role_list = Role.objects.all()
        role_form = RoleForm()
        user = UserInfo.objects.filter(user_id=request.user.id)
        print(user)
        context = {
            "permission_list": permission_list,
            "user": user,
            'role_list': role_list,
            "role_form": role_form,
        }
        return render(request, 'system/permission.html', context=context)
    if request.method == "POST":
        role_title = request.POST['role']
        roles = Role.objects.filter(title=role_title)
        if roles:
            return HttpResponse('2')
        else:
            Role.objects.create(title=role_title)
            return HttpResponse('1')

@csrf_exempt
def user(request):
    if request.method == "POST":
        user_form = RegistrationForm(request.POST)
        userinfo_form = UserInfoForm(request.POST)
        if user_form.is_valid() * userinfo_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            new_profile = userinfo_form.save(commit=False)
            new_profile.user = new_user
            new_profile.save()
            UserInfo.objects.create(user=new_user)
            return HttpResponse("successfully")
        else:
            return HttpResponse("抱歉，注册失败")
    else:
        user_list = UserInfo.objects.all()
        user_form = RegistrationForm()
        userinfo_form = UserInfoForm()
        return render(request, "system/user.html", {"user_list": user_list, "form": user_form, "userinfo": userinfo_form})
