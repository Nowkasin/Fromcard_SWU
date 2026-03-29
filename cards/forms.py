from django import forms
from .models import PersonnelCardRequest
from django.utils.translation import gettext_lazy as _

# Base Form
class BasePersonnelForm(forms.ModelForm):
    class Meta:
        model = PersonnelCardRequest
        fields = [
            'first_name','surname', 'birth_date',
            'nationality', 'blood_type', 'rh_factor',

            'reg_address',
            'subdistrict', 'district', 'province', 'zipcode',
            'use_reg_address', 'contact_address',

            'phone', 'id_card',
            'old_card_number',
        ]
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }

RH_CHOICES = [
    ('', _('-- เลือก Rh --')),
    ('+', 'Rh+'),
    ('-', 'Rh-'),
]

# 🟦 University Form
class UniversityForm(BasePersonnelForm):

    STAFF_CHOICES = [
        ('university_staff', 'พนักงานมหาวิทยาลัย'),
        ('employee', 'ลูกจ้างมหาวิทยาลัย'),
        ('foreign_temp', 'ลูกจ้างชั่วคราวชาวต่างประเทศ'),
        ('civil_servant', 'ข้าราชการ'),
        ('permanent_employee', 'ลูกจ้างประจำ'),
        ('retired_civil_servant', 'ข้าราชการบำนาญ'),
        ('retired', 'ผู้เกษียณอายุ'),
    ]

    CASE_CHOICES = [
        ('new', 'ขอมีบัตรใหม่'),
        ('change', 'ขอเปลี่ยนบัตร'),
        ('expired', 'บัตรหมดอายุ'),
        ('lost', 'บัตรหาย'),
        ('damaged', 'บัตรชำรุด'),
    ]

    # 🔥 FIX: เพิ่ม expired
    NEW_REASON_CHOICES = [
        ('first', 'บัตรครั้งแรก'),
        ('lost', 'บัตรหาย'),
        ('damaged', 'บัตรชำรุด'),
        ('expired', 'บัตรหมดอายุ'),  # ✅ แก้ตรงนี้
    ]

    CHANGE_REASON_CHOICES = [
        ('name_change', 'เปลี่ยนชื่อ'),
        ('position_change', 'เปลี่ยนตำแหน่ง'),
    ]

    # 🔥 FIX: รองรับหลายแบบ (กัน HTML ไม่ตรง)
    EVIDENCE_CHOICES = [
        ('id_copy', 'สำเนาบัตรประชาชน'),
        ('house_copy', 'สำเนาทะเบียนบ้าน'),
        ('id_card', 'สำเนาบัตรประชาชน'),  # ✅ กันกรณี HTML ใช้ id_card
        ('house', 'สำเนาทะเบียนบ้าน'),    # ✅ กันกรณี HTML ใช้ house
    ]

    NATIONALITY_CHOICES = [
        ('', _('-- เลือกสัญชาติ --')),
        ('ไทย', _('ไทย')),
        ('อังกฤษ', _('อังกฤษ')),
        ('เยอรมัน', _('เยอรมัน')),
        ('ญี่ปุ่น', _('ญี่ปุ่น')),
        ('จีน', _('จีน')),
        ('เกาหลี', _('เกาหลี')),
        ('เมียนม่า', _('เมียนมา')),
        ('เวียดนาม', _('เวียดนาม')),
        ('อื่นๆ', _('อื่นๆ')),
    ]

    BLOOD_CHOICES = [
        ('', _('-- หมู่โลหิต --')),
        ('A', 'A'), ('B', 'B'), ('AB', 'AB'), ('O', 'O'),
        ('ไม่ระบุ', _('ไม่ระบุ')),
    ]

    RH_CHOICES = [
        ('', _('-- เลือก Rh --')),
        ('+', 'Rh+'),
        ('-', 'Rh-'),
    ]

    staff_types = forms.MultipleChoiceField(
        choices=STAFF_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    case_types = forms.MultipleChoiceField(
        choices=CASE_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    new_reasons = forms.MultipleChoiceField(
        choices=NEW_REASON_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    change_reasons = forms.MultipleChoiceField(
        choices=CHANGE_REASON_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    evidence = forms.CharField(required=False)

    # 🔥 FIX: ไม่บังคับกรอก (กัน form ไม่ผ่าน)
    nationality = forms.ChoiceField(
        choices=NATIONALITY_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'mt-1 w-full border-b border-slate-700 py-1'})
    )

    blood_type = forms.ChoiceField(
        choices=BLOOD_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'mt-1 w-full border-b border-slate-700 py-1'})
    )
    rh_factor = forms.ChoiceField(
        choices=RH_CHOICES,
        required=False,  # 🔥 สำคัญ
        widget=forms.Select(attrs={
            "class": "mt-1 w-full border-b border-slate-700 py-1 bg-white"
        })
    )

    rh_factor = forms.ChoiceField(
        choices=RH_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'mt-1 w-full border-b border-slate-700 py-1'})
    )

    class Meta(BasePersonnelForm.Meta):
        fields = BasePersonnelForm.Meta.fields + [
            'department',
            'staff_types',
            'case_types',
            'new_reasons',
            'change_reasons',
            'evidence',
            'signature',
        ]


# 🟩 Gov Form
class GovForm(BasePersonnelForm):

    staff_types = forms.MultipleChoiceField(
        choices=UniversityForm.STAFF_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta(BasePersonnelForm.Meta):
        fields = BasePersonnelForm.Meta.fields + [
            'department',
            'staff_types',
            'section', 'subsection', 'division',
            'organization', 'ministry',
            'job_title', 'level', 'purpose',
            'photo1', 'photo2'
        ]