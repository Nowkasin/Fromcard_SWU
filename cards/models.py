# cards/models.py
from django.db import models

class PersonnelCardRequest(models.Model):
    fullname = models.CharField("ข้าพเจ้า", max_length=200, blank=True)
    name = models.CharField("ชื่อ-สกุล", max_length=200, blank=True)

    # เก็บวันเกิดเป็น DateField (birth_date เก็บเป็น ISO date)
    birth_date = models.DateField("วันเกิด", null=True, blank=True)

    nationality = models.CharField("สัญชาติ", max_length=100, blank=True)
    blood_type = models.CharField("หมู่โลหิต", max_length=10, blank=True)
    rh_factor = models.CharField(max_length=1, blank=True, null=True)

    # ที่อยู่ / เบอร์ / บัตรประชาชน
    reg_address = models.TextField("ที่อยู่ตามทะเบียนบ้าน", blank=True)
    reg_district = models.CharField("อำเภอ/เขต/จังหวัด/รหัสไปรษณีย์", max_length=200, blank=True)
    use_reg_address = models.BooleanField("ใช้ที่อยู่ตามทะเบียนบ้าน", default=False)
    contact_address = models.TextField("ที่อยู่ที่สามารถติดต่อได้", blank=True)
    phone = models.CharField("โทรศัพท์", max_length=50, blank=True)
    id_card = models.CharField("หมายเลขบัตรประชาชน", max_length=20, blank=True)

    # ฟิลด์ที่สอดคล้องกับ form ที่เราเพิ่ม
    department = models.CharField("รับราชการ/หน่วยงาน", max_length=300, blank=True)
    old_card_number = models.CharField("หมายเลขบัตรเดิม", max_length=100, blank=True)
    evidence = models.CharField("หลักฐานประกอบ", max_length=300, blank=True)

    # เก็บค่า checkbox หลายตัวเป็น JSON — สะดวกในการค้นหา/ขยาย (Django 3.1+)
    # cards/models.py (แก้เฉพาะส่วน JSONField)
    staff_types = models.JSONField("ประเภทบุคลากร", blank=True, null=True, default=list)
    case_types = models.JSONField("กรณี", blank=True, null=True, default=list)
    new_reasons = models.JSONField("เหตุผลขอบัตรใหม่", blank=True, null=True, default=list)
    change_reasons = models.JSONField("เหตุผลเปลี่ยนบัตร", blank=True, null=True, default=list)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.fullname or self.name} ({self.created_at.date()})"

class ThaiAddress(models.Model):
    subdistrict = models.CharField(max_length=200)   # แขวง / ตำบล
    district = models.CharField(max_length=200)      # เขต / อำเภอ
    province = models.CharField(max_length=200)      # จังหวัด
    zipcode = models.CharField(max_length=5)         # รหัสไปรษณีย์

    def __str__(self):
        return f"{self.subdistrict} {self.district} {self.province} {self.zipcode}"