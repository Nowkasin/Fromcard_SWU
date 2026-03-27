from django.db import models


class PersonnelCardRequest(models.Model): 
    # ข้อมูลพื้นฐาน   
    fullname = models.CharField("ชื่อ-สกุล", max_length=200, blank=True)
    birth_date = models.DateField("วันเกิด", null=True, blank=True)
    nationality = models.CharField("สัญชาติ", max_length=100, blank=True)
    blood_type = models.CharField("หมู่โลหิต", max_length=10, blank=True)
    rh_factor = models.CharField("Rh",max_length=5, blank=True, null=True)  # รองรับ + / - / Rh+
    # ที่อยู่ (แยก field ชัดเจน)
    reg_address = models.TextField("ที่อยู่ตามทะเบียนบ้าน", blank=True)
    subdistrict = models.CharField("ตำบล/แขวง", max_length=200, blank=True)
    district = models.CharField("อำเภอ/เขต", max_length=200, blank=True)
    province = models.CharField("จังหวัด", max_length=200, blank=True)
    zipcode = models.CharField("รหัสไปรษณีย์", max_length=5, blank=True)

    use_reg_address = models.BooleanField("ใช้ที่อยู่ตามทะเบียนบ้าน", default=False)
    contact_address = models.TextField("ที่อยู่ที่สามารถติดต่อได้", blank=True)   
    # ติดต่อ
    phone = models.CharField("โทรศัพท์", max_length=50, blank=True)
    id_card = models.CharField("หมายเลขบัตรประชาชน", max_length=20, blank=True)
    # หน่วยงาน (ใช้ร่วมทั้ง 2 ฟอร์ม)
    department = models.CharField("หน่วยงาน/สังกัด", max_length=300, blank=True)
    # ===== Gov Form เพิ่ม =====
    section = models.CharField("กอง", max_length=255, blank=True)
    subsection = models.CharField("ฝ่าย", max_length=255, blank=True)
    division = models.CharField("ส่วน", max_length=255, blank=True)
    organization = models.CharField("หน่วยงาน", max_length=255, blank=True)
    ministry = models.CharField("กระทรวง", max_length=255, blank=True)
    job_title = models.CharField("ตำแหน่ง", max_length=255, blank=True)
    level = models.CharField("ระดับ", max_length=255, blank=True)
    purpose = models.TextField("วัตถุประสงค์", blank=True)
    # ข้อมูลบัตร    
    old_card_number = models.CharField("หมายเลขบัตรเดิม", max_length=100, blank=True)
    # Checkbox (JSONField → ใช้ list เสมอ)
    staff_types = models.JSONField("ประเภทบุคลากร", default=list, blank=True)
    case_types = models.JSONField("กรณี", default=list, blank=True)
    new_reasons = models.JSONField("เหตุผลขอบัตรใหม่", default=list, blank=True)
    change_reasons = models.JSONField("เหตุผลเปลี่ยนบัตร", default=list, blank=True)
    evidence = models.JSONField("หลักฐานประกอบ", default=list, blank=True)
    # ไฟล์
    signature = models.ImageField(upload_to='signatures/', null=True, blank=True)
    photo1 = models.ImageField(upload_to='photos/', null=True, blank=True)
    photo2 = models.ImageField(upload_to='photos/', null=True, blank=True)
    # system   
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.fullname} ({self.created_at.date()})"
# Address master (ใช้ autocomplete)
class ThaiAddress(models.Model):
    subdistrict = models.CharField(max_length=200)   # แขวง / ตำบล
    district = models.CharField(max_length=200)      # เขต / อำเภอ
    province = models.CharField(max_length=200)      # จังหวัด
    zipcode = models.CharField(max_length=5)         # รหัสไปรษณีย์
    def __str__(self):
        return f"{self.subdistrict} {self.district} {self.province} {self.zipcode}"