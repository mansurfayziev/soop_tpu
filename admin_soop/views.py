from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from core.models import Violation, Akt
from django.contrib import messages
from django.http import HttpResponse
import xlwt

def user_is_admin(user):
    return user.is_authenticated and user.is_staff


@user_passes_test(user_is_admin)
def adminView(request):
    if request.method == 'POST':
        room = request.POST.get('query', '')

        vios=Violation.objects.filter(room=room)[::-1]
        akts=Akt.objects.filter(room=room)[::-1]
        vios2 = Violation.objects.all().order_by('-id')[:5]
        if vios:
            context = {
                'vios': vios,
                'akts': akts,
                'vios2': vios2,
                'room': room,
                'count': len(vios),
                'count2': len(akts),

            }
            return render(request, 'admin_soop/index.html', context)
        else:
            messages.error(request, 'Комната не найдено.')
            return redirect('admin_page')

    vios = Violation.objects.all()[::-1]
    akts = Akt.objects.all()[::-1]
    vios2 = Violation.objects.all().order_by('-id')[:5]
    context = {
        'vios': vios,
        'akts':akts,
        'vios2': vios2,
        'count': len(vios),
        'count2': len(akts),

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
    akts=Akt.objects.filter(room=room)[::-1]
    vios2 = Violation.objects.all().order_by('-id')[:5]
    context = {
        'vios': vios,
        'akts':akts,
        'vios2': vios2,
        'room': room,
        'count': len(vios),
        'count2': len(akts),

    }
    return render(request, 'admin_soop/index.html', context)

def filterByDate(request, date):
    vios=Violation.objects.filter(date__icontains=date)[::-1]
    akts=Akt.objects.filter(date__icontains=date)[::-1]
    vios2 = Violation.objects.all().order_by('-id')[:5]

    context = {
        'vios': vios,
        'akts': akts,
        'vios2': vios2,
        'date': date,
        'count': len(vios),
        'count2': len(akts),

    }
    return render(request, 'admin_soop/index.html', context)

def filterBySoop_fio(request, soop_fio):
    vios=Violation.objects.filter(soop_fio__icontains=soop_fio)[::-1]
    akts=Akt.objects.filter(soop_fio__icontains=soop_fio)[::-1]
    vios2 = Violation.objects.all().order_by('-id')[:5]

    context = {
        'vios': vios,
        'akts': akts,
        'vios2': vios2,
        'date': 'Oтправитель: '+ soop_fio,
        'count': len(vios),
        'count2': len(akts),

    }
    return render(request, 'admin_soop/index.html', context)



def update(request, pk):
        vio = Violation.objects.get(pk=pk)

        if request.method=='POST':
            fio=request.POST['fio']
            comment=request.POST['comment']
            cam_checks = request.POST.getlist('camCheck')
            f=''
            for check in cam_checks:
                f+=check+'. '
            if comment:
                f+=comment+'. '

            if f.strip()!='' or fio.strip()!='':
                rr = Violation.objects.get(pk=pk)
                if f.strip()!='':
                    rr.comment=f
                if fio.strip()!='':
                    rr.fio=fio
                rr.save()

                messages.success(request, 'Успешно); Нарушения отредактирована!')

                return redirect('admin_page')
            else:
                messages.error(request, 'Нарушения не отредактирована!')


        return render(request, 'admin_soop/update.html', {'vio': vio})


def export_to_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="SOOP-Web-site.xls"'

    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('fayziev.pythonanywhere.com')

    # Добавляем заголовки
    columns = ['Комната', 'Нарушител', 'Причина', 'Отправил','Дата']
    for col_num, column_title in enumerate(columns):
        worksheet.write(0, col_num, column_title)

    # Извлекаем данные из базы данных и добавляем их в файл Excel
    queryset = Violation.objects.all()
    queryset_akt = Akt.objects.all()
    row_num = 1
    for obj in queryset:
        worksheet.write(row_num, 0, obj.room)
        worksheet.write(row_num, 1, obj.fio)
        worksheet.write(row_num, 2, obj.comment)
        worksheet.write(row_num, 3, obj.soop_fio)
        worksheet.write(row_num, 4, obj.date.strftime('%Y-%m-%d | %H:%M'))
        row_num += 1


    for _ in range(1):
        row_num += 1

    worksheet.write_merge(row_num, row_num, 0, 4, 'Акты')

    row_num += 1

    for obj in queryset_akt:
        worksheet.write(row_num, 0, obj.room)
        worksheet.write(row_num, 1, obj.fio)
        worksheet.write(row_num, 2, obj.comment)
        worksheet.write(row_num, 3, obj.soop_fio)
        worksheet.write(row_num, 4, obj.date.strftime('%Y-%m-%d | %H:%M'))
        row_num += 1

    workbook.save(response)
    return response


def deleteAkt(request,pk):
    vio = Akt.objects.get(pk=pk)

    if request.method == 'POST':
        password = request.POST.get('password', '')

        if password == 'deleteVIO':
            vio.delete()
            messages.success(request, 'Акт успешно удалено.')
            return redirect('admin_page')
        else:
            messages.error(request, 'Неверный пароль. Акт не удалено.')
            return redirect('delete', pk=pk)

    return render(request, 'admin_soop/delete.html', {'vio': vio, 'akt':True})



def updateAkt(request, pk):
        vio = Akt.objects.get(pk=pk)

        if request.method=='POST':
            fio=request.POST['fio']
            comment=request.POST['comment']
            cam_checks = request.POST.getlist('camCheck')
            f=''
            for check in cam_checks:
                f+=check+'. '
            if comment:
                f+=comment+'. '

            if f.strip()!='' or fio.strip()!='':
                rr = Akt.objects.get(pk=pk)
                if f.strip()!='':
                    rr.comment=f
                if fio.strip()!='':
                    rr.fio=fio
                rr.save()

                messages.success(request, 'Успешно); Акт отредактирована!')

                return redirect('admin_page')
            else:
                messages.error(request, 'Акт не отредактирована!')


        return render(request, 'admin_soop/update.html', {'vio': vio, 'akt':True,})





