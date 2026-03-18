document.addEventListener("DOMContentLoaded", function () {

    const subdistrict = document.getElementById("subdistrict");
    const district = document.getElementById("district");
    const province = document.getElementById("province");
    const zipcode = document.getElementById("zipcode");

    if (!subdistrict) return;

    const list = document.createElement("div");
    list.className = "absolute bg-white border w-full z-50 max-h-60 overflow-auto";
    subdistrict.parentNode.style.position = "relative";
    subdistrict.parentNode.appendChild(list);

    subdistrict.addEventListener("input", function () {

        const q = this.value.trim();
        list.innerHTML = "";

        if (q.length < 2) return;

        const results = THAI_ADDRESS.filter(a =>
            a.subdistrict.includes(q)
        ).slice(0, 10);

        results.forEach(addr => {

            const item = document.createElement("div");
            item.className = "p-2 hover:bg-slate-100 cursor-pointer text-sm";

            item.textContent =
                `${addr.subdistrict} ${addr.district} ${addr.province} ${addr.zipcode}`;

            item.onclick = function () {

                subdistrict.value = addr.subdistrict;
                district.value = addr.district;
                province.value = addr.province;
                zipcode.value = addr.zipcode;

                list.innerHTML = "";
            };

            list.appendChild(item);
        });

    });

});