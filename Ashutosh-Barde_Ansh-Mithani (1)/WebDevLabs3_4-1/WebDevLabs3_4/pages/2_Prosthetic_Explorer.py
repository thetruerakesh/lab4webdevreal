import requests
import streamlit as st

st.title("ProstheticMatch: FDA Device Explorer")
st.write("Explore FDA-classified prosthetic device categories and registered GUDID products.")

def get_classifications():
    url = "https://api.fda.gov/device/classification.json"
    params = {
        "search": "device_name:prosthesis OR device_name:prosthetic",
        "limit": 100
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data.get("results", [])
        return []
    except:
        return []

def get_gudid_devices(product_code):
    url = "https://api.fda.gov/device/udi.json"
    params = {
        "search": 'product_codes.code:"' + product_code + '"',
        "limit": 25
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data.get("results", [])
        return []
    except:
        return []

def count_field(items, field_name):
    counts = {}
    for item in items:
        value = item.get(field_name)
        if not value:
            value = "Unknown"
        if value in counts:
            counts[value] = counts[value] + 1
        else:
            counts[value] = 1
    return counts

all_devices = get_classifications()

if len(all_devices) == 0:
    st.error("Could not load data from the openFDA API. Please try again later.")
    st.stop()

st.subheader("1. Filter Prosthetic Categories")

specialties = []
for device in all_devices:
    spec = device.get("medical_specialty_description")
    if spec and spec not in specialties:
        specialties.append(spec)
specialties_sorted = ["All Specialties"] + sorted(specialties)

selected_specialty = st.selectbox("Filter by Medical Specialty", specialties_sorted)
keyword = st.text_input("Search by Keyword (e.g., knee, foot, arm, hip, external)")
keyword = keyword.strip().lower()

filtered_devices = []
for device in all_devices:
    spec = device.get("medical_specialty_description") or "Unknown"
    name = device.get("device_name") or ""
    definition = device.get("definition") or ""

    matches_spec = (selected_specialty == "All Specialties") or (spec == selected_specialty)
    matches_key = (keyword == "") or (keyword in name.lower()) or (keyword in definition.lower())

    if matches_spec and matches_key:
        filtered_devices.append(device)

implant_count = 0
for device in filtered_devices:
    if device.get("implant_flag") == "Y":
        implant_count = implant_count + 1
external_count = len(filtered_devices) - implant_count

col1, col2, col3 = st.columns(3)
col1.metric("Matching Categories", len(filtered_devices))
col2.metric("Implantable Categories", implant_count)
col3.metric("External / Non-Implant", external_count)

if len(filtered_devices) == 0:
    st.warning("No prosthetic categories matched your filters. Try another keyword or specialty.")
    st.stop()

st.subheader("2. Regulatory Overview")

raw_class_counts = count_field(filtered_devices, "device_class")
class_chart = {}
for key in sorted(raw_class_counts.keys()):
    if key == "1":
        class_chart["Class I (Low Risk)"] = raw_class_counts[key]
    elif key == "2":
        class_chart["Class II (Moderate Risk)"] = raw_class_counts[key]
    elif key == "3":
        class_chart["Class III (High Risk)"] = raw_class_counts[key]
    else:
        class_chart["Class " + str(key)] = raw_class_counts[key]

specialty_chart = count_field(filtered_devices, "medical_specialty_description")

chart1, chart2 = st.columns(2)
with chart1:
    st.write("Devices by FDA Class")
    st.bar_chart(class_chart)
with chart2:
    st.write("Devices by Medical Specialty")
    st.bar_chart(specialty_chart)

st.subheader("3. Inspect a Prosthetic Category & Registered Products")

device_labels = []
device_lookup = {}
for device in filtered_devices:
    name = device.get("device_name") or "Unnamed Device"
    code = device.get("product_code") or "N/A"
    label = name + " (" + code + ")"
    if label not in device_lookup:
        device_labels.append(label)
        device_lookup[label] = device

selected_label = st.selectbox("Choose a prosthetic category:", device_labels)
selected_device = device_lookup[selected_label]

st.write("Device Name:", selected_device.get("device_name") or "N/A")
st.write("Product Code:", selected_device.get("product_code") or "N/A")
st.write("FDA Class:", selected_device.get("device_class") or "N/A")
st.write("Specialty:", selected_device.get("medical_specialty_description") or "N/A")
st.write("Definition:", selected_device.get("definition") or "No definition available.")

product_code = selected_device.get("product_code") or ""
gudid_list = []
if product_code:
    gudid_list = get_gudid_devices(product_code)

st.subheader("4. Registered GUDID Products for " + str(product_code))

if len(gudid_list) > 0:
    mfr_counts = count_field(gudid_list, "company_name")
    st.write("Registered Devices by Manufacturer")
    st.bar_chart(mfr_counts)

    rows = []
    for item in gudid_list:
        row = {
            "Brand Name": item.get("brand_name") or "N/A",
            "Manufacturer": item.get("company_name") or "N/A",
            "Model": item.get("version_or_model_number") or "N/A",
            "MRI Safety": item.get("mri_safety") or "Not Specified",
            "Status": item.get("commercial_distribution_status") or "N/A"
        }
        rows.append(row)
    st.dataframe(rows)
else:
    st.info("No registered GUDID products were found for this product code. Try selecting another category above.")