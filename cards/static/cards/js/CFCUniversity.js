// static/cards/js/CFCUnuversity.js
(function () {
  // ================= HELPERS =================
  const thaiMonths = [
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
  ];

  const pad = (n) => String(n).padStart(2, "0");
  const beToGregorian = (be) => be - 543;
  const gregorianToBE = (g) => g + 543;
  const $ = (id) => document.getElementById(id);

  // ================= DATE =================
  const birthDisplay = $("birthDisplay");
  const birthDateHidden = $("birth_date");
  const ageField = $("age");

  function initBirthDatePicker() {
  if (!birthDisplay || !birthDateHidden) return;

  const dp = $("dp");
  const yearView = $("yearView");
  const monthView = $("monthView");
  const dayView = $("dayView");
  const daysGrid = $("daysGrid");
  const monthYearLabel = $("monthYearLabel");

  const prevBtn = $("prevMonth");
  const nextBtn = $("nextMonth");
  const cancelBtn = $("dpCancel");
  const clearBtn = $("dpClear");

  if (!dp) return;

  let selectedYear = null;
  let selectedMonth = null;

  // ================= OPEN =================
  birthDisplay.addEventListener("click", () => {
    dp.classList.remove("hidden");
    showYearView();
  });

  // ================= CLOSE =================
  cancelBtn?.addEventListener("click", () => {
    dp.classList.add("hidden");
  });

  clearBtn?.addEventListener("click", () => {
    birthDisplay.value = "";
    birthDateHidden.value = "";
    if (ageField) ageField.value = "";
    dp.classList.add("hidden");
  });

  // ================= YEAR =================
  function showYearView() {
    yearView.innerHTML = "";
    yearView.classList.remove("hidden");
    monthView.classList.add("hidden");
    dayView.classList.add("hidden");

    const currentYear = new Date().getFullYear() + 543;

    for (let y = currentYear; y >= currentYear - 100; y--) {
      const btn = document.createElement("button");
      btn.textContent = y;
      btn.className = "border rounded p-1 hover:bg-blue-100";

      btn.onclick = () => {
        selectedYear = y;
        showMonthView();
      };

      yearView.appendChild(btn);
    }
  }

  // ================= MONTH =================
  function showMonthView() {
    monthView.innerHTML = "";
    monthView.classList.remove("hidden");
    yearView.classList.add("hidden");

    thaiMonths.forEach((m, i) => {
      const btn = document.createElement("button");
      btn.textContent = m;
      btn.className = "border rounded p-2 hover:bg-blue-100";

      btn.onclick = () => {
        selectedMonth = i;
        showDayView();
      };

      monthView.appendChild(btn);
    });
  }

  // ================= DAY =================
  function showDayView() {
    dayView.classList.remove("hidden");
    monthView.classList.add("hidden");
    renderCalendar();
  }

  function renderCalendar() {
    daysGrid.innerHTML = "";

    const gYear = beToGregorian(selectedYear);
    const firstDay = new Date(gYear, selectedMonth, 1);
    const lastDate = new Date(gYear, selectedMonth + 1, 0).getDate();

    monthYearLabel.textContent =
      thaiMonths[selectedMonth] + " " + selectedYear;

    // ช่องว่างก่อนวันแรก
    for (let i = 0; i < firstDay.getDay(); i++) {
      const empty = document.createElement("div");
      daysGrid.appendChild(empty);
    }

    for (let d = 1; d <= lastDate; d++) {
      const btn = document.createElement("button");
      btn.textContent = d;
      btn.className = "p-1 hover:bg-green-200 rounded";

      btn.onclick = () => {
        const iso =
          gYear + "-" + pad(selectedMonth + 1) + "-" + pad(d);

        birthDateHidden.value = iso;

        birthDisplay.value =
          d + " " + thaiMonths[selectedMonth] + " " + selectedYear;

        updateAge();
        dp.classList.add("hidden");
      };

      daysGrid.appendChild(btn);
    }
  }

  // ================= NAV =================
  prevBtn?.addEventListener("click", () => {
    selectedMonth--;
    if (selectedMonth < 0) {
      selectedMonth = 11;
      selectedYear--;
    }
    renderCalendar();
  });

  nextBtn?.addEventListener("click", () => {
    selectedMonth++;
    if (selectedMonth > 11) {
      selectedMonth = 0;
      selectedYear++;
    }
    renderCalendar();
  });

  // ================= LOAD OLD VALUE =================
  if (birthDateHidden.value) {
    const d = new Date(birthDateHidden.value);
    const beYear = gregorianToBE(d.getFullYear());

    birthDisplay.value =
      d.getDate() +
      " " +
      thaiMonths[d.getMonth()] +
      " " +
      beYear;
  }
}
  function setTodayFields() {
    const now = new Date();
    const day = pad(now.getDate());
    const month = thaiMonths[now.getMonth()];
    const year = now.getFullYear() + 543;

    if ($("todayDay") && !$("todayDay").value) $("todayDay").value = day;
    if ($("todayMonth") && !$("todayMonth").value)
      $("todayMonth").value = month;
    if ($("todayYear") && !$("todayYear").value) $("todayYear").value = year;
    if ($("todayISO") && !$("todayISO").value)
      $("todayISO").value = now.toISOString().slice(0, 10);
  }

  function updateAge() {
    if (!birthDateHidden?.value || !ageField) return;

    const today = new Date();
    const b = new Date(birthDateHidden.value);

    let age = today.getFullYear() - b.getFullYear();

    if (
      today.getMonth() < b.getMonth() ||
      (today.getMonth() === b.getMonth() && today.getDate() < b.getDate())
    ) {
      age--;
    }

    ageField.value = age >= 0 ? age : "";
  }

  // ================= VALIDATION =================
  function initValidation() {
    const form = $("cardForm");
    const errorBox = $("formErrorBox");
    if (!form) return;

    const showError = (msg) => {
      if (!errorBox) return;
      errorBox.textContent = msg;
      errorBox.classList.remove("hidden");
      errorBox.scrollIntoView({ behavior: "smooth", block: "center" });
    };

    const clearError = () => {
      if (!errorBox) return;
      errorBox.textContent = "";
      errorBox.classList.add("hidden");
    };

    const isEmpty = (v) => !v || String(v).trim() === "";

    const markInvalid = (el, invalid) => {
      if (!el) return;
      el.classList.toggle("border-red-500", invalid);
      el.classList.toggle("ring-1", invalid);
      el.classList.toggle("ring-red-400", invalid);
    };

    const requiredFields = [
      "fullname",
      "name",
      "birthDisplay",
      "idCard",
      "contactAddress",
      "subdistrict",
      "district",
      "province",
      "zipcode",
      "phone",
      "writtenAt",
      "department",
    ];

    form.addEventListener("submit", function (e) {
      clearError();

      // ✅ 1. birth date (สำคัญสุด)
      if (!birthDateHidden.value) {
        showError("กรุณาเลือกวันเกิด");
        e.preventDefault();
        return;
      }

      // ✅ 2. staff type
      if (
        document.querySelectorAll('[name="staff_types"]:checked').length === 0
      ) {
        showError("กรุณาเลือกประเภทบุคลากร");
        e.preventDefault();
        return;
      }

      // ✅ 3. reasons
      if (
        document.querySelectorAll('[name="new_reasons"]:checked').length ===
          0 &&
        document.querySelectorAll('[name="change_reasons"]:checked').length ===
          0
      ) {
        showError("กรุณาเลือกเหตุผลอย่างน้อย 1 รายการ");
        e.preventDefault();
        return;
      }

      // ✅ 4. input ทั่วไป
      let firstInvalid = null;

      requiredFields.forEach((id) => {
        const el = $(id);
        if (!el) return;

        const invalid = isEmpty(el.value);
        markInvalid(el, invalid);

        if (invalid && !firstInvalid) firstInvalid = el;
      });

      if (firstInvalid) {
        showError("กรุณากรอกข้อมูลให้ครบ");
        firstInvalid.focus();
        e.preventDefault();
      }
    });

    form.addEventListener("input", (e) => {
      const el = e.target;
      if (["INPUT", "SELECT", "TEXTAREA"].includes(el.tagName)) {
        markInvalid(el, isEmpty(el.value));
        clearError();
      }
    });
  }

  // ================= ADDRESS COPY =================
  function initAddressCopy() {
    const chk = $("useRegAddress");
    const contact = $("contactAddress");

    if (!chk || !contact) return;

    chk.addEventListener("change", () => {
      if (!chk.checked) {
        contact.readOnly = false;
        contact.classList.remove("bg-slate-100/40");
        return;
      }

      const parts = [];

      const reg = document.querySelector('[name="reg_address"]')?.value || "";
      const clean = reg
        .replace(/(แขวง|ตำบล|เขต|อำเภอ|จังหวัด)/gi, "")
        .replace(/[,;()]/g, " ")
        .replace(/\s+/g, " ")
        .trim();

      if (clean) parts.push(clean);

      ["subdistrict", "district", "province", "zipcode"].forEach((id) => {
        const val = $(id)?.value;
        if (val) parts.push(val.trim());
      });

      contact.value = parts.join(" ");
      contact.readOnly = true;
      contact.classList.add("bg-slate-100/40");
    });
  }

  // ================= ID CARD =================
  function initIdCard() {
    const boxes = document.querySelectorAll("#idBoxContainer input");
    const hidden = document.querySelector('[name="id_card"]');

    if (!boxes.length || !hidden) return;

    boxes.forEach((input, i) => {
      input.addEventListener("input", () => {
        input.value = input.value.replace(/\D/g, "").slice(0, 1);
        if (input.value && boxes[i + 1]) boxes[i + 1].focus();

        hidden.value = [...boxes].map((x) => x.value || "").join("");
      });
    });
  }

  // ================= SIGNATURE =================
  function initSignature() {
    const input = $("signatureInput");
    const preview = $("signaturePreview");
    const placeholder = $("placeholderText");

    if (!input) return;

    input.addEventListener("change", (e) => {
      const file = e.target.files[0];
      if (!file) return;

      const reader = new FileReader();
      reader.onload = (ev) => {
        preview.src = ev.target.result;
        preview.classList.remove("hidden");
        placeholder.classList.add("hidden");
      };
      reader.readAsDataURL(file);
    });
  }

  // ================= RESET =================
  function initReset() {
    const btn = $("resetBtn");
    if (!btn) return;

    btn.addEventListener("click", () => {
      document
        .querySelectorAll("#cardForm input, textarea, select")
        .forEach((el) => {
          if (el.type === "checkbox") el.checked = false;
          else if (el.type !== "hidden") el.value = "";
        });
    });
  }

  // ================= INIT =================
  document.addEventListener("DOMContentLoaded", () => {
    initBirthDatePicker();
    setTodayFields();
    updateAge();
    initValidation();
    initAddressCopy();
    initIdCard();
    initSignature();
    initReset();
  });
})();
