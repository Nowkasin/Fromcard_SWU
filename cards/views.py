from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.utils.translation import gettext as _
from django.conf import settings

from datetime import date
import subprocess
import os
import tempfile

from .forms import UniversityForm, GovForm
from .models import PersonnelCardRequest, ThaiAddress


# 🟦 FORM VIEW (มหาลัย)
def request_card_view(request):
    if request.method == 'POST':
        data = request.POST.copy()
        for field in ['staff_types', 'case_types', 'new_reasons', 'change_reasons', 'evidence']:
            data.setlist(field, request.POST.getlist(field))

        form = UniversityForm(data, request.FILES)

        if form.is_valid():
            obj = form.save()
            return redirect('cards:export_pdf', pk=obj.pk)
        else:
            print("❌ FORM ERROR:", form.errors)
            messages.error(request, _("ข้อมูลไม่สมบูรณ์ กรุณาตรวจสอบ"))
    else:
        form = UniversityForm()

    today = date.today()
    months = [
        _("มกราคม"), _("กุมภาพันธ์"), _("มีนาคม"), _("เมษายน"),
        _("พฤษภาคม"), _("มิถุนายน"), _("กรกฎาคม"), _("สิงหาคม"),
        _("กันยายน"), _("ตุลาคม"), _("พฤศจิกายน"), _("ธันวาคม")
    ]

    return render(request, 'cards/request_card.html', {
        'form': form,
        'today_iso': today.isoformat(),
        'today_day': f"{today.day:02d}",
        'today_month_name': months[today.month - 1],
        'today_be_year': today.year + 543,
    })


# 🟩 FORM VIEW (ราชการ)
def gov_card_view(request):
    if request.method == 'POST':
        data = request.POST.copy()
        data.setlist('staff_types', request.POST.getlist('staff_types'))
        form = GovForm(data, request.FILES)

        if form.is_valid():
            obj = form.save()
            return redirect('cards:export_pdf', pk=obj.pk)
        else:
            print("❌ GOV ERROR:", form.errors)
            messages.error(request, _("ข้อมูลไม่สมบูรณ์"))
    else:
        form = GovForm()

    today = date.today()

    return render(request, 'cards/Gov_card.html', {
        'form': form,
        'today_day': f"{today.day:02d}",
        'today_month_name': today.strftime('%B'),
        'today_be_year': today.year + 543,
    })


# 🖨 PRINT VIEW (HTML)
def print_card_view(request, pk):
    obj = get_object_or_404(PersonnelCardRequest, pk=pk)

    today = date.today()
    months = [
        "มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน",
        "พฤษภาคม", "มิถุนายน", "กรกฎาคม", "สิงหาคม",
        "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"
    ]

    id_digits = list(obj.id_card or '')
    id_digits += [''] * (13 - len(id_digits))

    return render(request, 'cards/request_card_print.html', {
        'object': obj,
        'id_digits': id_digits,
        'today_day': f"{today.day:02d}",
        'today_month_name': months[today.month - 1],
        'today_be_year': today.year + 543,
    })


# 📄 EXPORT PDF (Puppeteer) - พร้อมดาวน์โหลดทันที & log error
# 📄 EXPORT PDF (Puppeteer)
def export_pdf_view(request, pk):
    obj = get_object_or_404(PersonnelCardRequest, pk=pk)

    # URL ของหน้าพิมพ์
    url = request.build_absolute_uri(
        reverse('cards:print_card', args=[pk])
    )
    print("🌐 PRINT URL:", url)

    # Path ชั่วคราวในเครื่อง
    output_path = os.path.join(os.path.dirname(__file__), f"card_{pk}.pdf")

    try:
        # เรียก Node + Puppeteer
        subprocess.run(
            [
                "node",
                os.path.join(settings.BASE_DIR, "cards", "static", "cards", "js", "generate_pdf.js"),
                url,
                output_path,
            ],
            capture_output=True,   # <-- นี่
            text=True,             # <-- นี่
            check=True
        )

        # อ่านไฟล์ PDF เข้า memory
        with open(output_path, "rb") as f:
            pdf_bytes = f.read()

        # ลบไฟล์ชั่วคราว
        if os.path.exists(output_path):
            os.remove(output_path)

        # ส่ง PDF ให้ดาวน์โหลด
        response = HttpResponse(pdf_bytes, content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="card_{pk}.pdf"'
        return response

    except subprocess.CalledProcessError as e:
        print("❌ PDF generation failed:", e)
        return JsonResponse({
            "error": "PDF generation failed",
            "detail": e.stderr  # <-- แสดง error log จาก Node
        }, status=500)

    except Exception as e:
        print("❌ Unexpected error:", e)
        return JsonResponse({
            "error": "Unexpected error",
            "detail": str(e)
        }, status=500)


# 📍 ADDRESS API
def address_api(request):
    q = request.GET.get("q", "").strip()
    if not q:
        return JsonResponse({"results": []})

    addresses = ThaiAddress.objects.filter(subdistrict__icontains=q)[:10]
    data = [
        {
            "subdistrict": a.subdistrict,
            "district": a.district,
            "province": a.province,
            "zipcode": a.zipcode,
        }
        for a in addresses
    ]
    return JsonResponse({"results": data})


# 🧪 TEST PDF (ReportLab)
def generate_pdf(request):
    from reportlab.pdfgen import canvas
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="test.pdf"'

    p = canvas.Canvas(response)
    p.drawString(100, 750, "Hello PDF from Django 🔥")
    p.drawString(100, 730, "This file is downloaded to your computer")
    p.showPage()
    p.save()

    return response
