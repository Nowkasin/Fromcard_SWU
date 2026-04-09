from django.db import models


class PersonnelCardRequest(models.Model):
    # ข้อมูลพื้นฐาน
    first_name = models.CharField(max_length=100, blank=True)
    surname = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField("วันเกิด", null=True, blank=True)
    nationality = models.CharField("สัญชาติ", max_length=100, blank=True)
    blood_type = models.CharField("หมู่โลหิต", max_length=10, blank=True)
    rh_factor = models.CharField("Rh", max_length=5, blank=True, null=True)

    reg_address = models.TextField("ที่อยู่ตามทะเบียนบ้าน", blank=True)
    subdistrict = models.CharField("ตำบล/แขวง", max_length=200, blank=True)
    district = models.CharField("อำเภอ/เขต", max_length=200, blank=True)
    province = models.CharField("จังหวัด", max_length=200, blank=True)
    zipcode = models.CharField("รหัสไปรษณีย์", max_length=5, blank=True)
    evidence_slip = models.FileField(upload_to="evidence_slips/", blank=True, null=True)
    use_reg_address = models.BooleanField("ใช้ที่อยู่ตามทะเบียนบ้าน", default=False)
    contact_address = models.TextField("ที่อยู่ที่สามารถติดต่อได้", blank=True)

    phone = models.CharField("โทรศัพท์", max_length=50, blank=True)
    id_card = models.CharField("หมายเลขบัตรประชาชน", max_length=20, blank=True)

    department = models.CharField("หน่วยงาน/สังกัด", max_length=300, blank=True)
    position = models.CharField("ตำแหน่ง", max_length=255, blank=True)
    affiliation = models.CharField("สังกัด", max_length=255, blank=True)
    section = models.CharField("กอง", max_length=255, blank=True)
    subsection = models.CharField("ฝ่าย", max_length=255, blank=True)
    division = models.CharField("ส่วน", max_length=255, blank=True)
    organization = models.CharField("หน่วยงาน", max_length=255, blank=True)
    ministry = models.CharField("กระทรวง", max_length=255, blank=True)
    job_title = models.CharField("ตำแหน่ง", max_length=255, blank=True)
    level = models.CharField("ระดับ", max_length=255, blank=True)
    purpose = models.TextField("วัตถุประสงค์", blank=True)

    old_card_number = models.CharField("หมายเลขบัตรเดิม", max_length=100, blank=True)

    # ลายเซ็นเอาไว้แค่ตัวเดียว
    signature = models.ImageField(upload_to='signatures/', blank=True, null=True)

    staff_types = models.CharField(max_length=50, blank=True)
    case_types = models.JSONField(default=list, blank=True)
    new_reasons = models.CharField(max_length=50, blank=True)
    change_reasons = models.CharField(max_length=50, blank=True)
    evidence = models.JSONField(default=list, blank=True)

    # รูปภาพอื่น ๆ
    photo1 = models.ImageField(upload_to="photos/", null=True, blank=True)
    photo2 = models.ImageField(upload_to="photos/", null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.first_name} ({self.created_at.date()})"
# Address master (ใช้ autocomplete)
class ThaiAddress(models.Model):
    subdistrict = models.CharField(max_length=200)  # แขวง / ตำบล
    district = models.CharField(max_length=200)  # เขต / อำเภอ
    province = models.CharField(max_length=200)  # จังหวัด
    zipcode = models.CharField(max_length=5)  # รหัสไปรษณีย์

    def __str__(self):
        return f"{self.subdistrict} {self.district} {self.province} {self.zipcode}"

class EvidenceFile(models.Model):
    request = models.ForeignKey(
        PersonnelCardRequest,
        on_delete=models.CASCADE,
        related_name="evidences"
    )
    file = models.FileField(upload_to="evidence_files/")
    file_type = models.CharField(max_length=50, blank=True)  # optional

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.name}"