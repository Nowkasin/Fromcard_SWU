// static/cards/js/CFCUnuversity.js
(function () {
  // helpers
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
  const config = { yearStartBE: 2400, yearEndOffset: 0 };
  const pad = (n) => String(n).padStart(2, "0");
  const beToGregorian = (be) => be - 543;
  const gregorianToBE = (g) => g + 543;

  // Safe element getter
  const $ = (id) => document.getElementById(id) || null;

  // Today fields (use server-provided if present)
  function setTodayFields() {
    const now = new Date();
    const day = pad(now.getDate());
    const monthName = thaiMonths[now.getMonth()];
    const beYear = now.getFullYear() + 543;

    const todayDayEl =
      $("todayDay") ||
      $("today_day") ||
      document.querySelector('[name="today_day"]');
    const todayMonthEl =
      $("todayMonth") ||
      $("today_month") ||
      document.querySelector('[name="today_month_name"]');
    const todayYearEl =
      $("todayYear") ||
      $("today_year") ||
      document.querySelector('[name="today_be_year"]');
    const todayISO =
      $("todayISO") || document.querySelector('[name="today_iso"]');

    if (todayDayEl && !todayDayEl.value) todayDayEl.value = day;
    if (todayMonthEl && !todayMonthEl.value) todayMonthEl.value = monthName;
    if (todayYearEl && !todayYearEl.value) todayYearEl.value = beYear;
    if (todayISO && !todayISO.value)
      todayISO.value = now.toISOString().slice(0, 10);
  }

  /* Datepicker variables (DOM refs) */
  const birthDisplay = $("birthDisplay");
  const dp = $("dp");
  const yearView = $("yearView");
  const monthView = $("monthView");
  const dayView = $("dayView");
  const dpTitle = $("dpTitle");
  const dpStep = $("dpStep");
  const monthYearLabel = $("monthYearLabel");
  const daysGrid = $("daysGrid");
  const dpCancel = $("dpCancel");
  const dpClear = $("dpClear");
  const prevMonthBtn = $("prevMonth");
  const nextMonthBtn = $("nextMonth");
  const birthDateHidden = $("birth_date");
  const ageField = $("age");

  let step = 1;
  let selectedBEYear = null;
  let selectedMonthIndex = null;
  let selectedDateISO = null;
  const todayISO =
    $("todayISO") && $("todayISO").value
      ? $("todayISO").value
      : new Date().toISOString().slice(0, 10);

  function renderYears() {
    if (!yearView) return;
    yearView.innerHTML = "";
    const currentBE = gregorianToBE(new Date().getFullYear());
    const endBE = currentBE + config.yearEndOffset;
    for (let y = endBE; y >= config.yearStartBE; y--) {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "px-2 py-2 border rounded text-sm hover:bg-slate-100";
      btn.textContent = y;
      btn.dataset.be = y;
      btn.addEventListener("click", () => {
        selectedBEYear = Number(btn.dataset.be);
        step = 2;
        updateView();
      });
      yearView.appendChild(btn);
    }
  }

  function renderMonths() {
    if (!monthView) return;
    monthView.innerHTML = "";
    thaiMonths.forEach((m, idx) => {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className =
        "px-3 py-2 border rounded text-sm text-left hover:bg-slate-100";
      btn.textContent = m;
      btn.dataset.month = idx;
      btn.addEventListener("click", () => {
        selectedMonthIndex = Number(btn.dataset.month);
        step = 3;
        updateView();
      });
      monthView.appendChild(btn);
    });
  }

  function renderDays() {
    if (!daysGrid || selectedBEYear === null || selectedMonthIndex === null)
      return;
    daysGrid.innerHTML = "";
    const gYear = beToGregorian(selectedBEYear);
    const month = selectedMonthIndex;
    const firstDay = new Date(gYear, month, 1);
    const lastDay = new Date(gYear, month + 1, 0);
    const startWeekday = firstDay.getDay();
    const totalDays = lastDay.getDate();

    for (let i = 0; i < startWeekday; i++) {
      const blank = document.createElement("div");
      blank.className = "h-9";
      daysGrid.appendChild(blank);
    }

    for (let d = 1; d <= totalDays; d++) {
      const cell = document.createElement("button");
      cell.type = "button";
      cell.className =
        "h-9 flex items-center justify-center rounded hover:bg-sky-100";
      cell.textContent = d;
      cell.dataset.day = d;
      cell.addEventListener("click", () => {
        const gY = gYear;
        const gM = month + 1;
        const gD = d;
        selectedDateISO = `${gY}-${pad(gM)}-${pad(gD)}`;
        if (birthDateHidden) birthDateHidden.value = selectedDateISO;
        if (birthDisplay)
          birthDisplay.value = `${pad(gD)}/${pad(gM)}/${selectedBEYear}`;
        updateAge();
        closeDP();
      });
      daysGrid.appendChild(cell);
    }

    if (monthYearLabel)
      monthYearLabel.textContent = `${thaiMonths[month]} ${selectedBEYear}`;
  }

  function updateAge() {
    if (!birthDateHidden || !ageField) return;
    if (!birthDateHidden.value) {
      ageField.value = "";
      return;
    }
    const ref = new Date(todayISO + "T00:00:00");
    const b = new Date(birthDateHidden.value + "T00:00:00");
    let age = ref.getFullYear() - b.getFullYear();
    const m = ref.getMonth() - b.getMonth();
    if (m < 0 || (m === 0 && ref.getDate() < b.getDate())) age--;
    ageField.value = age >= 0 ? String(age) : "";
  }

  function updateView() {
    if (yearView) yearView.classList.toggle("hidden", step !== 1);
    if (monthView) monthView.classList.toggle("hidden", step !== 2);
    if (dayView) dayView.classList.toggle("hidden", step !== 3);

    if (step === 1 && dpTitle && dpStep) {
      dpTitle.textContent = "เลือกปี (พ.ศ.)";
      dpStep.textContent = "ขั้นตอน 1/3";
    } else if (step === 2 && dpTitle && dpStep) {
      dpTitle.textContent = `ปีที่เลือก: ${selectedBEYear}`;
      dpStep.textContent = "ขั้นตอน 2/3 — เลือกเดือน";
    } else if (step === 3 && dpTitle && dpStep) {
      dpTitle.textContent = `ปี ${selectedBEYear} — เลือกวัน`;
      dpStep.textContent = "ขั้นตอน 3/3";
      renderDays();
    }
  }

  function openDP() {
    if (dp) dp.classList.remove("hidden");
    step = 1;
    updateView();
  }
  function closeDP() {
    if (dp) dp.classList.add("hidden");
  }
const signatureInput = document.getElementById("signatureInput");
const signaturePreview = document.getElementById("signaturePreview");
const signaturePlaceholder = document.getElementById("placeholderText");
  function attachEvents() {
    if (birthDisplay) {
      birthDisplay.addEventListener("click", (e) => {
        e.stopPropagation();
        openDP();
      });
    }

    if (dpCancel) dpCancel.addEventListener("click", () => closeDP());
    if (dpClear)
      dpClear.addEventListener("click", () => {
        selectedBEYear = null;
        selectedMonthIndex = null;
        selectedDateISO = null;
        if (birthDateHidden) birthDateHidden.value = "";
        if (birthDisplay) birthDisplay.value = "";
        if (ageField) ageField.value = "";
        step = 1;
        updateView();
      });
    if (prevMonthBtn)
      prevMonthBtn.addEventListener("click", () => {
        if (selectedMonthIndex === null) return;
        selectedMonthIndex = (selectedMonthIndex - 1 + 12) % 12;
        updateView();
      });
    if (nextMonthBtn)
      nextMonthBtn.addEventListener("click", () => {
        if (selectedMonthIndex === null) return;
        selectedMonthIndex = (selectedMonthIndex + 1) % 12;
        updateView();
      });
    document.addEventListener("click", (e) => {
      if (dp && !dp.contains(e.target) && e.target !== birthDisplay) closeDP();
    });
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape") closeDP();
    });

    // Address copy
const chk = document.getElementById("useRegAddress");

const regAddress = document.querySelector('[name="reg_address"]');
const subdistrict = document.getElementById("subdistrict");
const district = document.getElementById("district");
const province = document.getElementById("province");
const zipcode = document.getElementById("zipcode");

const contact = document.getElementById("contactAddress");

// --- replace the old if (chk) { ... } block with this ---
if (chk) {
  chk.addEventListener("change", function () {
    if (chk.checked) {
      const parts = [];

      // 🔥 ลบแค่คำ label แต่ไม่กันซ้ำแล้ว
      let clean = (regAddress && regAddress.value) ? String(regAddress.value) : ""; //แก้ตรงกรอกให้รองรับ / ด้วย
      clean = clean.replace(/(แขวง|ตำบล|เขต|อำเภอ|จังหวัด)/gi, "")
             .replace(/[,;()]/g, " ")   // <-- ไม่ลบ /
             .replace(/\s{2,}/g, " ")
             .trim();

      if (clean) parts.push(clean);

      // 🔥 ใส่ทุกค่าเลย ไม่เช็คซ้ำ
      if (subdistrict?.value) parts.push(subdistrict.value.trim());
      if (district?.value) parts.push(district.value.trim());
      if (province?.value) parts.push(province.value.trim());
      if (zipcode?.value) parts.push(zipcode.value.trim());

      if (contact) {
        contact.value = parts.join(" ");
        contact.readOnly = true;
        contact.classList.add("bg-slate-100/40");
      }

    } else {
      if (contact) {
        contact.readOnly = false;
        contact.classList.remove("bg-slate-100/40");
      }
    }
  });

  // ให้ทำงานทันทีตอนโหลด
  if (chk.checked) {
    chk.dispatchEvent(new Event("change"));
  }
}
    // ID boxes: join into hidden
    const idBoxes = document.querySelectorAll("#idBoxContainer input");
    const idHidden =
      $("id_card_input") || document.querySelector('input[name="id_card"]');
    if (idBoxes && idBoxes.length) {
      idBoxes.forEach((input, idx) => {
        input.addEventListener("input", (e) => {
          input.value = input.value.replace(/[^0-9]/g, "").slice(0, 1);
          if (input.value && idBoxes[idx + 1]) idBoxes[idx + 1].focus();
          if (idHidden)
            idHidden.value = Array.from(idBoxes)
              .map((x) => x.value || "")
              .join("");
        });
        input.addEventListener("keydown", (e) => {
          if (e.key === "Backspace" && !input.value && idBoxes[idx - 1]) {
            idBoxes[idx - 1].focus();
          }
        });
      });
      // fill from hidden if value exists
      if (idHidden && idHidden.value) {
        const val = idHidden.value;
        for (let i = 0; i < idBoxes.length; i++) {
          if (idBoxes[i]) idBoxes[i].value = val[i] || "";
        }
      }
    }

    // reset button
    const resetBtn = $("resetBtn") || document.getElementById("resetBtn");
    if (resetBtn) {
  resetBtn.addEventListener("click", () => {
    const keep = [
      "writtenAt",
      "todayDay",
      "todayMonth",
      "todayYear",
      "todayISO",
    ];

    document
      .querySelectorAll(
        "#cardForm input, #cardForm textarea, #cardForm select, #govCardForm input, #govCardForm textarea, #govCardForm select",
      )
      .forEach((el) => {
        if (keep.includes(el.id)) return;
        if (el.type === "checkbox") el.checked = false;
        else if (el.type !== "hidden") el.value = "";
      });

    if (contact) {
      contact.readOnly = false;
      contact.classList.remove("bg-slate-100/40");
    }

    // ✅ reset signature ต้องอยู่ในนี้
    if (signatureInput) signatureInput.value = "";

    if (signaturePreview) {
      signaturePreview.src = "";
      signaturePreview.classList.add("hidden");
    }

    if (signaturePlaceholder) {
      signaturePlaceholder.classList.remove("hidden");
    }
  });
}

    // form submit: ensure id_hidden joined
    const formEl = $("cardForm") || $("govCardForm");
    if (formEl) {
      formEl.addEventListener("submit", function (e) {
        if (idHidden)
          idHidden.value = Array.from(
            document.querySelectorAll("#idBoxContainer input"),
          )
            .map((x) => x.value || "")
            .join("");
        // optionally add client-side validation here
      });
    }
    
if (signatureInput) {
  signatureInput.addEventListener("change", function (e) {
    const file = e.target.files[0];

    if (file) {
      const reader = new FileReader();

      reader.onload = function (ev) {
        if (signaturePreview) {
          signaturePreview.src = ev.target.result;
          signaturePreview.classList.remove("hidden");
        }
        if (signaturePlaceholder) {
          signaturePlaceholder.classList.add("hidden");
        }
      };

      reader.readAsDataURL(file);
    }
  });
}
  } // end attachEvents

  // Init
  document.addEventListener("DOMContentLoaded", function () {
    try {
      setTodayFields();
      renderYears();
      renderMonths();
      attachEvents();

      // if birth_date already set from server, show it
      if (birthDateHidden && birthDateHidden.value) {
        const parts = birthDateHidden.value.split("-");
        if (parts.length === 3) {
          const gY = Number(parts[0]),
            gM = Number(parts[1]),
            gD = Number(parts[2]);
          const beY = gY + 543;
          if (birthDisplay) birthDisplay.value = `${pad(gD)}/${pad(gM)}/${beY}`;
          updateAge();
        }
      }
    } catch (err) {
      // console.error('CFCUnuversity.js init error', err);
    }
  });
  // 🔥 EXPORT PDF
// 🔥 EXPORT PDF
const exportBtn = document.getElementById("exportPdfBtn");

if (exportBtn) {
  exportBtn.addEventListener("click", async function () {
    const form =
      document.getElementById("cardForm") ||
      document.getElementById("govCardForm");

    const pk =
      form?.dataset.pk || exportBtn?.dataset.pk;

    if (!pk) {
      alert("❌ ไม่พบ ID (pk)");
      return;
    }

    try {
      const res = await fetch(`/cards/export-pdf/${pk}/`);

      if (!res.ok) throw new Error("PDF failed");

      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);

      const a = document.createElement("a");
      a.href = url;
      a.download = `card_${pk}.pdf`;
      document.body.appendChild(a);
      a.click();
      a.remove();

      window.URL.revokeObjectURL(url);
    } catch (err) {
      alert("❌ สร้าง PDF ไม่สำเร็จ");
      console.error(err);
    }
  });
}
})(); // IIFE
