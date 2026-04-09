from django import forms
from .models import PersonnelCardRequest
from django.utils.translation import gettext_lazy as _


# ================= BASE FORM =================
class BasePersonnelForm(forms.ModelForm):
    class Meta:
        model = PersonnelCardRequest
        fields = [
            "first_name",
            "surname",
            "birth_date",
            "nationality",
            "blood_type",
            "rh_factor",
            "reg_address",
            "subdistrict",
            "district",
            "province",
            "zipcode",
            "use_reg_address",
            "contact_address",
            "phone",
            "id_card",
        ]
        widgets = {
            "birth_date": forms.DateInput(attrs={"type": "date"}),
        }


# ================= UNIVERSITY FORM =================
class UniversityForm(BasePersonnelForm):

    STAFF_CHOICES = [
        ("university_staff", "พนักงานมหาวิทยาลัย"),
        ("employee", "ลูกจ้างมหาวิทยาลัย"),
        ("foreign_temp", "ลูกจ้างชั่วคราวชาวต่างประเทศ"),
        ("civil_servant", "ข้าราชการ"),
        ("permanent_employee", "ลูกจ้างประจำ"),
        ("retired", "ผู้เกษียณอายุ"),
    ]

    NEW_REASON_CHOICES = [
        ("damaged", "บัตรสูญหาย/ถูกทำลาย/บัตรชำรุด"),
        ("expired", "บัตรหมดอายุ"),
    ]

    CHANGE_REASON_CHOICES = [
        ("name_change", "เปลี่ยนชื่อ/เปลี่ยนนามสกุล"),
        ("position_change", "เปลี่ยนชื่อตำแหน่ง/เลื่อนระดับ"),
    ]

    NATIONALITY_CHOICES = [
        ("", _("-- เลือกสัญชาติ --")),
        ("ไทย", _("ไทย")),
        ("อังกฤษ", _("อังกฤษ")),
        ("เยอรมัน", _("เยอรมัน")),
        ("ญี่ปุ่น", _("ญี่ปุ่น")),
        ("จีน", _("จีน")),
        ("เกาหลี", _("เกาหลี")),
        ("เมียนม่า", _("เมียนมา")),
        ("เวียดนาม", _("เวียดนาม")),
        ("อื่นๆ", _("อื่นๆ")),
    ]

    BLOOD_CHOICES = [
        ("", _("-- หมู่โลหิต --")),
        ("A", "A"),
        ("B", "B"),
        ("AB", "AB"),
        ("O", "O"),
        ("ไม่ระบุ", _("ไม่ระบุ")),
    ]

    RH_CHOICES = [
        ("", _("-- เลือก Rh --")),
        ("+", "Rh+"),
        ("-", "Rh-"),
    ]

    # ===== Fields =====
    staff_types = forms.ChoiceField(
        choices=STAFF_CHOICES,
        widget=forms.RadioSelect,
        required=False
    )

    new_reasons = forms.ChoiceField(
        choices=NEW_REASON_CHOICES,
        widget=forms.RadioSelect,
        required=False
    )

    change_reasons = forms.ChoiceField(
        choices=CHANGE_REASON_CHOICES,
        widget=forms.RadioSelect,
        required=False
    )

    # (พัก evidence ไว้ก่อน)
    evidence = forms.CharField(required=False)
    evidence_slip = forms.FileField(required=False)
    
    nationality = forms.ChoiceField(
        choices=NATIONALITY_CHOICES,
        required=False,
        widget=forms.Select(attrs={"class": "mt-1 w-full border-b border-slate-700 py-1"})
    )

    blood_type = forms.ChoiceField(
        choices=BLOOD_CHOICES,
        required=False,
        widget=forms.Select(attrs={"class": "mt-1 w-full border-b border-slate-700 py-1"})
    )

    rh_factor = forms.ChoiceField(
        choices=RH_CHOICES,
        required=False,
        widget=forms.Select(attrs={"class": "mt-1 w-full border-b border-slate-700 py-1 bg-white"})
    )

    class Meta(BasePersonnelForm.Meta):
        fields = BasePersonnelForm.Meta.fields + [
            "department",
            "position",
            "affiliation",
            "staff_types",
            "new_reasons",
            "change_reasons",
            "evidence",
            "signature",
        ]

    # 🔥 FIX สำคัญ: validate reason
    def clean(self):
        cleaned_data = super().clean()

        new_reason = cleaned_data.get("new_reasons")
        change_reason = cleaned_data.get("change_reasons")

        # ❌ เลือก 2 อันไม่ได้
        if new_reason and change_reason:
            raise forms.ValidationError("เลือกเหตุผลได้เพียงอย่างเดียว")

        # ❌ ต้องเลือกอย่างใดอย่างหนึ่ง
        if not new_reason and not change_reason:
            raise forms.ValidationError("กรุณาเลือกเหตุผล")

        return cleaned_data


# ================= GOV FORM =================
class GovForm(BasePersonnelForm):

    staff_types = forms.MultipleChoiceField(
        choices=UniversityForm.STAFF_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta(BasePersonnelForm.Meta):
        fields = BasePersonnelForm.Meta.fields + [
            "department",
            "staff_types",
            "section",
            "subsection",
            "division",
            "organization",
            "ministry",
            "job_title",
            "level",
            "purpose",
            "photo1",
            "photo2",
        ]