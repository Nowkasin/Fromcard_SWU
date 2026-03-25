from django import forms
from .models import PersonnelCardRequest
from django.utils.translation import gettext_lazy as _

STAFF_CHOICES = [
    ('university_staff','พนักงานมหาวิทยาลัย'),
    ('employee','ลูกจ้างมหาวิทยาลัย'),
    ('foreign_temp','ลูกจ้างชั่วคราวชาวต่างประเทศ'),
    ('civil_servant','ข้าราชการ'),
    ('permanent_employee','ลูกจ้างประจำ'),
    ('retired_civil_servant','ข้าราชการบำนาญ'),
    ('retired', 'ผู้เกษียณอายุ'),
]

NEW_REASON_CHOICES = [
    ('expired','บัตรหมดอายุ'),
    ('lost','บัตรสูญหายหรือถูกทำลาย'),
    ('damaged','บัตรชำรุด'),
]

CHANGE_REASON_CHOICES = [
    ('position_change','เปลี่ยนตำแหน่ง/เปลี่ยนระดับ/เลื่อนยศ'),
    ('name_change','เปลี่ยนชื่อ'),
    ('surname_change','เปลี่ยนนามสกุล'),
    ('title_name_change','เปลี่ยนคำนำหน้าและชื่อสกุล'),
]

CASE_CHOICES = [
    ('first_card','ขอมีบัตรครั้งแรก'),
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
    ('A','A'),('B','B'),('AB','AB'),('O','O'),('ไม่ระบุ',_('ไม่ระบุ')),
]

RH_CHOICES = [
    ('', _('-- เลือก Rh --')),
    ('+', 'Rh+'),
    ('-', 'Rh-'),
]

class PersonnelCardRequestForm(forms.ModelForm):

    # ===== checkbox groups =====
    staff_type = forms.MultipleChoiceField(
        choices=STAFF_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='ประเภทบุคลากร'
    )

    new_reason = forms.MultipleChoiceField(
        choices=NEW_REASON_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='ขอมีบัตรใหม่เนื่องจาก'
    )

    change_reason = forms.MultipleChoiceField(
        choices=CHANGE_REASON_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='ขอเปลี่ยนบัตรใหม่เนื่องจาก'
    )

    case_type = forms.MultipleChoiceField(
        choices=CASE_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='กรณี'
    )

    # ===== 🔥 เพิ่มตรงนี้ =====
    photo1 = forms.ImageField(required=True, label='รูปถ่ายใบที่ 1')
    photo2 = forms.ImageField(required=True, label='รูปถ่ายใบที่ 2')

    photo_confirm = forms.BooleanField(
        required=True,
        label='ได้แนบรูปถ่ายสองใบมาพร้อมกับคำขอนี้แล้ว'
    )

    # ===== dropdown =====
    nationality = forms.ChoiceField(
        choices=NATIONALITY_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'mt-1 w-full border-b border-slate-700 py-1 bg-white'
        })
    )

    blood_type = forms.ChoiceField(
        choices=BLOOD_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'mt-1 w-full border-b border-slate-700 py-1 bg-white'
        })
    )
    rh_factor = forms.ChoiceField(
        choices=RH_CHOICES,
        required=False,  # 🔥 สำคัญ
        widget=forms.Select(attrs={
            "class": "mt-1 w-full border-b border-slate-700 py-1 bg-white"
        })
    )

    class Meta:
        model = PersonnelCardRequest
        fields = [
            'fullname','name','birth_date','nationality','blood_type','rh_factor',
            'reg_address','reg_district','phone','id_card',
            'use_reg_address','contact_address',
            'department','old_card_number','evidence',

            # 🔥 เพิ่มตรงนี้
            'photo1','photo2','photo_confirm',
        ]

        widgets = {
            'birth_date': forms.HiddenInput(),
            'reg_address': forms.TextInput(attrs={'id':'regAddress'}),
            'reg_district': forms.TextInput(attrs={'id':'regDistrict'}),
            'contact_address': forms.Textarea(attrs={'rows':2,'id':'contactAddress'}),
            'fullname': forms.TextInput(attrs={'id':'fullname'}),
            'name': forms.TextInput(attrs={'id':'name'}),
            'phone': forms.TextInput(attrs={'id':'phone'}),
            'id_card': forms.TextInput(attrs={'id':'idCard'}),
        }

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        super().__init__(*args, **kwargs)

        if instance:
            self.fields['staff_type'].initial = instance.staff_types or []
            self.fields['new_reason'].initial = instance.new_reasons or []
            self.fields['change_reason'].initial = instance.change_reasons or []
            self.fields['case_type'].initial = instance.case_types or []

    def clean_id_card(self):
        v = self.cleaned_data.get('id_card', '').strip()
        digits = ''.join(ch for ch in v if ch.isdigit())
        if digits and len(digits) != 13:
            raise forms.ValidationError(_('หมายเลขบัตรประชาชนต้องมี 13 หลัก'))
        return digits

    def save(self, commit=True):
        instance = super().save(commit=False)

        instance.staff_types = self.cleaned_data.get('staff_type', [])
        instance.new_reasons = self.cleaned_data.get('new_reason', [])
        instance.change_reasons = self.cleaned_data.get('change_reason', [])
        instance.case_types = self.cleaned_data.get('case_type', [])

        # 🔥 ถ้ามี field ใน model
        if hasattr(instance, 'photo1'):
            instance.photo1 = self.cleaned_data.get('photo1')
        if hasattr(instance, 'photo2'):
            instance.photo2 = self.cleaned_data.get('photo2')

        if commit:
            instance.save()

        return instance