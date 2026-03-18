import json

with open("db 2.json", encoding="utf-8") as f:
    data = json.load(f)

result = []

for province in data:
    province_name = province[0]

    for district in province[1]:
        district_name = district[0]

        for sub in district[1]:
            sub_name = sub[0]

            zipcode = sub[1][0] if isinstance(sub[1], list) else sub[1]

            if isinstance(sub_name, int):
                continue
            if isinstance(district_name, int):
                continue

            result.append({
                "subdistrict": sub_name,
                "district": district_name,
                "province": province_name,
                "zipcode": str(zipcode)
            })

with open("thai_address_data.js", "w", encoding="utf-8") as f:
    f.write("const THAI_ADDRESS = ")
    json.dump(result, f, ensure_ascii=False, indent=2)
    f.write(";")

print("สร้างไฟล์ thai_address_data.js เรียบร้อย")