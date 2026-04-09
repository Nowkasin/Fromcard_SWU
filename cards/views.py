from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.utils.translation import gettext as _
from django.conf import settings

from datetime import date
import subprocess
import os
import re
import base64

from django.core.files.base import ContentFile

from .forms import UniversityForm, GovForm
from .models import PersonnelCardRequest, ThaiAddress

# 🔥 HELPER: SAVE SIGNATURE (กันพัง 100%)

def format_thai_date(d):
    if not d:
        return "-", "-", "-"

    thai_months = [
        "", "มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน",
        "พฤษภาคม", "มิถุนายน", "กรกฎาคม", "สิงหาคม",
        "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"
    ]

    return d.day, thai_months[d.month], d.year + 543

def save_signature(obj, signature_data):
    if not signature_data:
        print("⚠️ NO SIGNATURE DATA")
        return

    try:
        print("🔥 RAW:", signature_data[:50])

        # ✅ ตรวจ format ให้ชัวร์ก่อน
        if "base64," not in signature_data:
            print("❌ INVALID FORMAT (no base64 prefix)")
            return

        header, imgstr = signature_data.split("base64,", 1)

        print("📏 BASE64 LENGTH:", len(imgstr))

        # ❌ กันข้อมูลพัง
        if len(imgstr) < 1000:
            print("❌ BASE64 TOO SHORT → INVALID")
            return

        # ✅ ดึง ext แบบปลอดภัย
        try:
            ext = header.split("/")[1].split(";")[0]
        except Exception:
            ext = "png"

        # ✅ decode แบบ safe
        image_file = ContentFile(base64.b64decode(imgstr))

        file_name = f"signature_{int(date.today().timestamp())}.{ext}"

        obj.signature.save(file_name, image_file, save=False)

        print("✅ SIGNATURE SAVED:", file_name)

        # 🔥 debug จริง (ไฟล์นี้ต้องเปิดได้)
        debug_path = os.path.join(settings.BASE_DIR, "debug_signature.png")
        with open(debug_path, "wb") as f:
            f.write(base64.b64decode(imgstr))

        print("🧪 DEBUG FILE:", debug_path)

    except Exception as e:
        print("❌ SIGNATURE ERROR:", e)


# 🟦 FORM VIEW (มหาลัย)
def request_card_view(request):
    if request.method == "POST":
        data = request.POST.copy()

        for field in [
            "staff_types",
            "case_types",
            "new_reasons",
            "change_reasons",
            "evidence",
        ]:
            data.setlist(field, request.POST.getlist(field))

        form = UniversityForm(data, request.FILES)

        if form.is_valid():
            obj = form.save(commit=False)

            signature_file = request.FILES.get("signature")
            if signature_file:
                obj.signature = signature_file

            obj.save()

            return redirect("cards:export_pdf", pk=obj.pk)
        else:
            print("❌ FORM ERROR:", form.errors)
            messages.error(request, _("ข้อมูลไม่สมบูรณ์ กรุณาตรวจสอบ"))
    else:
        form = UniversityForm()

    today = date.today()
    months = [
        _("มกราคม"),
        _("กุมภาพันธ์"),
        _("มีนาคม"),
        _("เมษายน"),
        _("พฤษภาคม"),
        _("มิถุนายน"),
        _("กรกฎาคม"),
        _("สิงหาคม"),
        _("กันยายน"),
        _("ตุลาคม"),
        _("พฤศจิกายน"),
        _("ธันวาคม"),
    ]

    return render(
        request,
        "cards/request_card.html",
        {
            "form": form,
            "today_iso": today.isoformat(),
            "today_day": f"{today.day:02d}",
            "today_month_name": months[today.month - 1],
            "today_be_year": today.year + 543,
        },
    )


# 🟩 FORM VIEW (ราชการ)
def gov_card_view(request):
    if request.method == "POST":
        data = request.POST.copy()
        data.setlist("staff_types", request.POST.getlist("staff_types"))

        form = GovForm(data, request.FILES)

        if form.is_valid():
            obj = form.save(commit=False)

            # 🔥 SAVE SIGNATURE
            save_signature(obj, form.cleaned_data.get("signature"))

            obj.save()

            return redirect("cards:export_pdf", pk=obj.pk)

        else:
            print("❌ GOV ERROR:", form.errors)
            messages.error(request, _("ข้อมูลไม่สมบูรณ์"))

    else:
        form = GovForm()

    today = date.today()

    return render(
        request,
        "cards/Gov_card.html",
        {
            "form": form,
            "today_day": f"{today.day:02d}",
            "today_month_name": today.strftime("%B"),
            "today_be_year": today.year + 543,
        },
    )

# 🖨️ PRINT VIEW
def print_card_view(request, pk):
    obj = get_object_or_404(PersonnelCardRequest, pk=pk)
    today = date.today()
    birth_day, birth_month, birth_year = format_thai_date(obj.birth_date)
    age = None
    if obj.birth_date:
        age = today.year - obj.birth_date.year
        if (today.month, today.day) < (obj.birth_date.month, obj.birth_date.day):
            age -= 1

    STAFF_MAP = dict(UniversityForm.STAFF_CHOICES)
    NEW_REASON_MAP = dict(UniversityForm.NEW_REASON_CHOICES)
    CHANGE_REASON_MAP = dict(UniversityForm.CHANGE_REASON_CHOICES)

    staff_types = [STAFF_MAP.get(x, x) for x in (obj.staff_types or [])]
    new_reasons = [NEW_REASON_MAP.get(x, x) for x in (obj.new_reasons or [])]
    change_reasons = [CHANGE_REASON_MAP.get(x, x) for x in (obj.change_reasons or [])]

    id_digits = list(obj.id_card or "")
    id_digits += [""] * (13 - len(id_digits))

    months = [
        "มกราคม",
        "กุมภาพันธ์",
        "มีนาคม",
        "เมษายน",
        "พฤษภาคม",
        "มิถุนายน",
        "กรกฎาคม",
        "สิงหาคม",
        "กันยายน",
        "ตุลาคม",
        "พฤศจิกายน",
        "ธันวาคม",
    ]

    return render(
        request,
        "cards/request_card_print.html",
        {
            "object": obj,
            "age": age,
            "staff_types": staff_types,
            "new_reasons": new_reasons,
            "change_reasons": change_reasons,
            "id_digits": id_digits,
            "today_day": f"{today.day:02d}",
            "today_month_name": months[today.month - 1],
            "today_be_year": today.year + 543,
            "birth_day": birth_day,
            "birth_month": birth_month,
            "birth_year": birth_year,
        },
    )

# 📄 EXPORT PDF
def export_pdf_view(request, pk):
    obj = get_object_or_404(PersonnelCardRequest, pk=pk)
    url = request.build_absolute_uri(reverse("cards:print_card", args=[pk]))
    output_path = os.path.join(os.path.dirname(__file__), f"card_{pk}.pdf")
    try:
        result = subprocess.run(
            [
                "node",
                os.path.join(
                    settings.BASE_DIR,
                    "cards",
                    "static",
                    "cards",
                    "js",
                    "generate_pdf.js",
                ),
                url,
                output_path,
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        print("🟢 Puppeteer:", result.stdout)
        with open(output_path, "rb") as f:
            pdf_bytes = f.read()
        if os.path.exists(output_path):
            os.remove(output_path)
        response = HttpResponse(pdf_bytes, content_type="application/pdf")
        response["Content-Disposition"] = (
            "attachment; filename*=UTF-8''คำขอมีบัตรประจำตัวบุคลากร.pdf"
        )
        return response
    except subprocess.CalledProcessError as e:
        print("❌ PDF ERROR:", e.stderr)
        return JsonResponse({"error": e.stderr}, status=500)

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

# 🧪 TEST PDF
def generate_pdf(request):
    from reportlab.pdfgen import canvas
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="test.pdf"'
    p = canvas.Canvas(response)
    p.drawString(100, 750, "Hello PDF from Django 🔥")
    p.showPage()
    p.save()

    return response
