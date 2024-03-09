from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from core.models import Violation
from django.contrib import messages

def user_is_admin(user):
    return user.is_authenticated and user.is_staff

leen = len(Violation.objects.all())-5

@user_passes_test(user_is_admin)
def adminView(request):
    if request.method == 'POST':
        room = request.POST.get('query', '')

        vios=Violation.objects.filter(room=room)[::-1]
        vios2 = Violation.objects.all()[leen::-1]
        context = {
            'vios': vios,
            'vios2': vios2,
            'room': room,
            'count': len(vios),
            
        }
        return render(request, 'admin_soop/index.html', context) 
        
    vios = Violation.objects.all()[::-1]

    vios2 = Violation.objects.all()[leen::-1]
    context = {
        'vios': vios,
        'vios2': vios2,
        'count': len(vios),
        
    }
    return render(request, 'admin_soop/index.html', context)




def deleteVIO(request, pk):
    vio = Violation.objects.get(pk=pk)

    if request.method == 'POST':
        password = request.POST.get('password', '')

        if password == 'deleteVIO': 
            vio.delete()
            messages.success(request, 'Нарушение успешно удалено.')
            return redirect('admin_page')
        else:
            messages.error(request, 'Неверный пароль. Нарушение не удалено.')
            return redirect('delete', pk=pk)  

    return render(request, 'admin_soop/delete.html', {'vio': vio})


def filterByRoom(request, room):
    vios=Violation.objects.filter(room=room)[::-1]
    vios2 = Violation.objects.all()[leen::-1]
    context = {
        'vios': vios,
        'vios2': vios2,
        'room': room,
        'count': len(vios),
        
    }
    return render(request, 'admin_soop/index.html', context)

def filterByDate(request, date):
    vios=Violation.objects.filter(date__icontains=date)[::-1]
    vios2 = Violation.objects.all()[leen::-1]

    context = {
        'vios': vios,
        'vios2': vios2,
        'date': date,
        'count': len(vios),
        
    }
    return render(request, 'admin_soop/index.html', context)

def filterBySoop_fio(request, soop_fio):
    vios=Violation.objects.filter(soop_fio__icontains=soop_fio)[::-1]
    vios2 = Violation.objects.all()[leen::-1]

    context = {
        'vios': vios,
        'vios2': vios2,
        'date': 'Oтправитель: '+ soop_fio,
        'count': len(vios),
        
    }
    return render(request, 'admin_soop/index.html', context)
