from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse
from django.contrib import messages
from django.utils.translation import gettext as _
from datetime import date

from .forms import PersonnelCardRequestForm
from .models import PersonnelCardRequest, ThaiAddress

def print_card_view(request, pk):
    obj = get_object_or_404(PersonnelCardRequest, pk=pk)
    # เตรียมเลขบัตรแบ่งเป็น list 13 ช่อง
    id_digits = list(obj.id_card or '')
    # pad ให้ยาว 13
    id_digits += [''] * (13 - len(id_digits))
    context = {
        'object': obj,
        'id_digits': id_digits,
        # ถ้าต้องการวันที่ปัจจุบัน (เช่น header)
        'today_day': ...,
        'today_month_name': ...,
        'today_be_year': ...,
    }
    return render(request, 'cards/request_card_print.html', context)

def request_card_view(request):
    if request.method == 'POST':
        form = PersonnelCardRequestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _("บันทึกเรียบร้อย (ตัวอย่าง)"))
            return redirect(reverse('cards:request_card'))
        else:
            messages.error(request, _("ข้อมูลไม่สมบูรณ์, กรุณาตรวจสอบ"))
    else:
        form = PersonnelCardRequestForm()

    today = date.today()

    months = [
        _("มกราคม"), _("กุมภาพันธ์"), _("มีนาคม"), _("เมษายน"),
        _("พฤษภาคม"), _("มิถุนายน"), _("กรกฎาคม"), _("สิงหาคม"),
        _("กันยายน"), _("ตุลาคม"), _("พฤศจิกายน"), _("ธันวาคม")
    ]

    context = {
        'form': form,
        'today_iso': today.isoformat(),
        'today_day': f"{today.day:02d}",
        'today_month_name': months[today.month - 1],
        'today_be_year': today.year + 543,
    }

    return render(request, 'cards/request_card.html', context)

def gov_card_view(request):
    """แสดง/บันทึกฟอร์มแบบ GOVCard (template: templates/cards/Gov_card.html)"""
    if request.method == 'POST':
        form = PersonnelCardRequestForm(request.POST)
        if form.is_valid():
            obj = form.save()
            messages.success(request, _("บันทึกเรียบร้อย (ตัวอย่าง)"))
            # redirect ไปที่หน้าเดียวกัน (หรือไปหน้า print หากต้องการ)
            return redirect(reverse('cards:gov_card'))
        else:
            messages.error(request, _("ข้อมูลไม่สมบูรณ์, กรุณาตรวจสอบ"))
    else:
        form = PersonnelCardRequestForm()

    today = date.today()
    months = [
        _("มกราคม"), _("กุมภาพันธ์"), _("มีนาคม"), _("เมษายน"),
        _("พฤษภาคม"), _("มิถุนายน"), _("กรกฎาคม"), _("สิงหาคม"),
        _("กันยายน"), _("ตุลาคม"), _("พฤศจิกายน"), _("ธันวาคม")
    ]

    context = {
        'form': form,
        'today_iso': today.isoformat(),
        'today_day': f"{today.day:02d}",
        'today_month_name': months[today.month - 1],
        'today_be_year': today.year + 543,
    }
    return render(request, 'cards/Gov_card.html', context)

def address_api(request):
    q = request.GET.get("q", "").strip()

    if not q:
        return JsonResponse({"results": []})

    addresses = ThaiAddress.objects.filter(
        subdistrict__icontains=q
    )[:10]

    data = []

    for a in addresses:
        data.append({
            "subdistrict": a.subdistrict,
            "district": a.district,
            "province": a.province,
            "zipcode": a.zipcode,
        })

    return JsonResponse({"results": data})