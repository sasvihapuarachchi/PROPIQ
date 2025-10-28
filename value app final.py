import streamlit as st
import json
import os
from fpdf import FPDF
from datetime import datetime
import base64

# --- PAGE CONFIG ---
st.set_page_config(page_title="PROPIQ | Valuation Report", page_icon="📄", layout="wide")

# --- USERS JSON FILE ---
USERS_FILE = "users.json"

# --- HELPER FUNCTIONS ---
def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

def register_user(username, password):
    users = load_users()
    if username in users:
        return False, "Username already exists!"
    users[username] = password
    save_users(users)
    return True, "User registered successfully!"

def login_user(username, password):
    users = load_users()
    if username not in users:
        return False, "Username does not exist!"
    if users[username] != password:
        return False, "Incorrect password!"
    return True, "Logged in successfully!"

# --- SESSION STATE ---
if "page" not in st.session_state:
    st.session_state.page = "login"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# --- CUSTOM STYLES ---
st.markdown("""
<style>
body {background-color: #f8f8f8; font-family: 'Segoe UI', sans-serif;}
main .block-container {padding-top: 0rem !important; margin-top: 0rem !important;}
.header {
    background: linear-gradient(90deg, #800000, #a52a2a);
    padding: 25px 20px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0 3px 15px rgba(0,0,0,0.15);
}
.header h1 {color: #FFD700; font-size: 40px; font-weight: 800; margin: 0;}
.header h4 {color: #fff8dc; font-weight: 500; margin: 5px 0 0;}
.card {
    background: linear-gradient(180deg, #fff, #fdfdfd);
    border-radius: 18px;
    box-shadow: 0 6px 24px rgba(0,0,0,0.08);
    padding: 2.5rem;
    transition: 0.3s ease-in-out;
}
.card:hover {transform: translateY(-3px); box-shadow: 0 8px 28px rgba(0,0,0,0.1);}
.section-title {color: #800000; font-size: 20px; font-weight: 700; margin-bottom: 10px;}
label {color: #800000; font-weight: 600;}
.stTextInput input, .stTextArea textarea {
    background-color: #fff; border: 2px solid #80000033; border-radius: 8px; color: black;
}
.stButton > button {
    background-color: #800000;
    color: white;
    border-radius: 10px;
    font-weight: 600;
    padding: 0.6rem 1rem;
    transition: all 0.25s ease;
}
.stButton > button:hover {
    background-color: #DAA520;
    color: black;
    transform: scale(1.02);
}
hr {border: 1px solid #80000033; margin: 20px 0;}
.footer {text-align: center; color: #555; font-size: 13px; margin-top: 40px;}
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("""
<div class="header">
    <h1>PROPIQ</h1>
    <h4>Valuation Report Generator - University of Sri Jayewardenepura</h4>
</div>
""", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://www.sjp.ac.lk/wp-content/uploads/2020/10/usjp-logo-300x300.png", width=120)
    if st.session_state.logged_in:
        st.markdown(f"**👋 Welcome, {st.session_state.username}**")
        st.divider()
        if st.button("🏠 Home"):
            st.session_state.page = "home"
            st.rerun()
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.page = "login"
            st.rerun()
    else:
        st.markdown("Please log in to access the system.")

# --- LOGIN & REGISTER ---
if not st.session_state.logged_in:
    if st.session_state.page == "login":
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🔐 Login to PROPIQ")
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login", use_container_width=True):
            success, msg = login_user(username, password)
            if success:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)
        st.markdown("</div>", unsafe_allow_html=True)
        st.info("Don't have an account?")
        if st.button("🆕 Register as a new member"):
            st.session_state.page = "register"
            st.rerun()

    elif st.session_state.page == "register":
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🆕 Register a New Account")
        username_r = st.text_input("Create Username", key="reg_username")
        password_r = st.text_input("Create Password", type="password", key="reg_password")
        confirm_r = st.text_input("Confirm Password", type="password", key="reg_confirm_password")
        if st.button("Register", use_container_width=True):
            if password_r != confirm_r:
                st.error("Passwords do not match!")
            elif username_r == "" or password_r == "":
                st.error("Enter username and password!")
            else:
                success, msg = register_user(username_r, password_r)
                if success:
                    st.success(msg)
                    st.session_state.page = "login"
                    st.rerun()
                else:
                    st.error(msg)
        if st.button("🔙 Back to Login"):
            st.session_state.page = "login"
            st.rerun()

# --- MAIN DASHBOARD ---
if st.session_state.logged_in:
    st.markdown(f"<h3 style='color:#800000;'>Welcome, {st.session_state.username}! 👋</h3>", unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Valuation Report Form</div>', unsafe_allow_html=True)
    fields = {}

    with st.expander("📋 General Valuation Information", expanded=True):
        fields["a) Identification and status of the valuer"] = st.text_input("a) Identification and status of the valuer")
        fields["b) Client details"] = st.text_input("b) Identification of the client and intended users")
        fields["c) Purpose of the valuation"] = st.text_area("c) Purpose of the valuation")
        fields["d) Identification of the property"] = st.text_area("d) Identification of the asset(s) or liability(ies) valued")
        fields["e) Basis of value adopted"] = st.text_input("e) Basis(es) of value adopted")
        fields["f) Valuation date"] = st.date_input("f) Valuation date")

    with st.expander("🏗️ Property & Valuation Details"):
        fields["g) Nature of the property"] = st.text_area("g) Nature of property")
        fields["h) Site profile"] = st.text_area("h) Site profile (land/building)")
        fields["i) Market value evidence"] = st.text_area("i) Evidence of market values")
        fields["j) Assumptions and reservations"] = st.text_area("j) Assumptions and special reservations")
        fields["k) Valuation approach"] = st.text_area("k) Valuation approach and reasoning")
        fields["l) Amount of valuation"] = st.text_input("l) Amount of valuation (LKR)")
        fields["m) Date of report"] = st.date_input("m) Date of the valuation report")

    with st.expander("🏠 Property Details"):
        st.markdown('<div class="section-title">Select Property Parts</div>', unsafe_allow_html=True)
        parts = {
            "Living Room": st.checkbox("Living Room"),
            "Bedroom": st.checkbox("Bedroom"),
            "Dining Room": st.checkbox("Dining Room"),
            "Open Veranda": st.checkbox("Open Veranda"),
            "Other": st.checkbox("Other"),
        }
        other_part = st.text_input("Specify other:", "") if parts["Other"] else None
        selected_parts = [p for p, v in parts.items() if v and p != "Other"]
        if other_part:
            selected_parts.append(other_part)
        fields["q) Selected Property Parts"] = selected_parts

    with st.expander("🏠 Property Images"):
        property_images = []
        img = st.file_uploader("Upload main property photo", type=["jpg", "jpeg", "png"], key="main_img")
        if img:
            path = "cover_property.jpg"
            with open(path, "wb") as f:
                f.write(img.getbuffer())
            property_images.append({"part": "Subject Property", "path": path})

        if selected_parts:
            for i, part in enumerate(selected_parts, start=1):
                img2 = st.file_uploader(f"Upload image for {part}", type=["jpg", "jpeg", "png"], key=f"img_{i}")
                if img2:
                    path2 = f"property_image_{i}.jpg"
                    with open(path2, "wb") as f:
                        f.write(img2.getbuffer())
                    property_images.append({"part": part, "path": path2})
            fields["r) Property Images"] = property_images
        else:
            st.info("Select at least one property part first.")

    # Safe progress bar
    progress = int((sum(1 for v in fields.values() if v) / len(fields)) * 100) if len(fields) > 0 else 0
    st.progress(progress)
    st.caption(f"Form Completion: {progress}%")

    # --- PDF CLASS ---
    class PDF(FPDF):
        def header(self):
            self.set_fill_color(128, 0, 0)
            self.rect(0, 0, 210, 20, 'F')
            self.set_text_color(255, 215, 0)
            self.set_font('Arial', 'B', 16)
            self.cell(0, 10, "PROPIQ | University of Sri Jayewardenepura", ln=True, align='C')
            self.ln(10)

        def footer(self):
            self.set_y(-15)
            self.set_text_color(128, 0, 0)
            self.set_font('Arial', 'I', 10)
            self.cell(0, 10, "Generated by PROPIQ | USJP", 0, 0, 'C')

    # --- Helper to print a template paragraph and then the user's input in bold (if provided) ---
    def add_template_paragraph(pdf, template_text, input_text=None):
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", "", 11)
        # print the template explanatory text
        for line in template_text.split("\n"):
            pdf.multi_cell(0, 6, line.strip())
        pdf.ln(2)
        # print the user input as bold (if provided)
        if input_text:
            pdf.set_font("Arial", "B", 11)
            # if the input is a list (e.g., selected parts), join them
            if isinstance(input_text, list):
                input_text_str = ", ".join(input_text) if input_text else "N/A"
            else:
                input_text_str = str(input_text)
            pdf.multi_cell(0, 6, input_text_str)
            pdf.ln(4)
        else:
            pdf.set_font("Arial", "I", 10)
            pdf.multi_cell(0, 6, "N/A")
            pdf.ln(4)
        # reset normal font
        pdf.set_font("Arial", "", 11)

    # --- Template paragraphs (taken / paraphrased from your uploaded template) ---
    TEMPLATE = {
        "01.0 PURPOSE OF VALUATION": """The purpose of this valuation is to determine the Market Value of the subject property for the intended purpose as described below.""",
        "02.0 DATE OF INSPECTION": """I inspected the subject property on the date noted below in the presence of the agent of the applicant. The date of inspection is generally accepted as the date of valuation.""",
        "03.0 IDENTIFICATION OF PROPERTY": """Explain how you identify the property. Includes boundary demarcation/plan and deed particulars. It is ideal to give reference to the survey plan details including the plan number, name of the land, name of the surveyor and the date of the survey plan. Indicate assessment number and postal address wherever applicable.""",
        "04.0 NATURE OF PROPERTY": """Explain the use of the property and occupancy: e.g., owner-occupied residential, commercial or industrial property. Whenever the occupant is not the owner of the property, the status of the occupancy and relationship between owner and occupant should be explained.""",
        "05.0 SITE PROFILE": """06.1 LAND - Explain the geographical features of the land such as shape, terrain, topography, soil condition, elevation, plantation, etc.\n\n06.2 BUILDING - Describe the building. Generally, this explanation should start from the top of the building (Roof) to the bottom (Foundation). All internal and external features including conveniences should be explained. The floor area of different constructions/ different ages have to be declared. It is recommended to add a pictorial view of the different sections/parts of the building with a small description.""",
        "06.0 EVIDENCE OF MARKET VALUES": """Details of evidence on land values and rentals as well as cost information should be given here. The types of data needed must be collected from reliable sources both private and public and recorded for future use, and the accuracy of data must be verified.""",
        "07.0 ASSUMPTION AND RESERVATION": """Assumptions and any special assumptions should be clearly stated. The Assumption is made that a specific investigation by the valuer is not required to prove that something is true. Special Assumptions are those things that are not true but have been assumed to be true.""",
        "08.0 BASIS OF VALUATION": """This explains the meaning of the value figure reported. Examples: Market Value, Forced Sale Value, Insurance Value. The following definitions (derived from IVS) have been used.""",
        "09.0 VALUATION APPROACH AND REASONING": """Explain the selected valuation approach and reasoning. This may be the Market approach, Income approach, or Cost approach. The valuation techniques used, and any adjustments should be stated.""",
        "10.0 CERTIFICATE": """Prepared by the valuer. The valuation was done according to the standards. This report is confidential to the client and is not allowed to be used by any other party for any other purpose. The validity period of this report is as stated below.""",
    }

    # --- PDF GENERATION FUNCTION ---
    def generate_pdf(data_dict):
        pdf = PDF()
        pdf.set_auto_page_break(auto=True, margin=15)

        # --- COVER PAGE (keep as-is) ---
        pdf.add_page()


        # --- University Logo (top center) ---
        # --- COVER PAGE ---
        pdf.image("https://www.sjp.ac.lk/wp-content/uploads/2020/10/usjp-logo-300x300.png", x=85, y=25, w=40)

        pdf.ln(60)
        pdf.set_font("Arial", "B", 20)
        pdf.set_text_color(128, 0, 0)
        pdf.cell(0, 15, "VALUATION REPORT", ln=True, align="C")
        pdf.ln(10)

        amount = data_dict.get("l) Amount of valuation", "LKR. ___________")
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, f"{amount}", ln=True, align="C")
        pdf.set_font("Arial", "I", 12)
        pdf.cell(0, 10, "The term of currency is Sri Lankan Rupees", ln=True, align="C")
        pdf.ln(15)

        report_id = datetime.now().strftime("PROPIQ-%Y%m%d-%H%M%S")
        pdf.set_font("Arial", "", 12)
        pdf.cell(0, 10, f"Reference Number of the Report: {report_id}", ln=True, align="C")
        pdf.ln(15)

        # main cover image (if available)
        if data_dict.get("r) Property Images"):
            try:
                if os.path.exists(data_dict["r) Property Images"][0]["path"]):
                    pdf.image(data_dict["r) Property Images"][0]["path"], x=25, y=None, w=160)
            except Exception:
                # if image fails, continue gracefully
                pass

        # --- Add rest of report pages based on template structure ---
        pdf.add_page()

        # Helper to write a section heading
        def write_section_heading(title):
            pdf.set_text_color(128, 0, 0)
            pdf.set_font("Arial", "B", 13)
            pdf.multi_cell(0, 8, title)
            pdf.ln(2)



        # 01.0 PURPOSE
        write_section_heading("01.0 PURPOSE OF VALUATION")
        add_template_paragraph(pdf, TEMPLATE["01.0 PURPOSE OF VALUATION"], data_dict.get("c) Purpose of the valuation"))

        # 02.0 DATE OF INSPECTION
        write_section_heading("02.0 DATE OF INSPECTION")
        date_of_inspection = data_dict.get("f) Valuation date")
        add_template_paragraph(pdf, TEMPLATE["02.0 DATE OF INSPECTION"], date_of_inspection.strftime("%Y-%m-%d") if date_of_inspection else None)

        # 03.0 IDENTIFICATION OF PROPERTY
        write_section_heading("03.0 IDENTIFICATION OF PROPERTY")
        add_template_paragraph(pdf, TEMPLATE["03.0 IDENTIFICATION OF PROPERTY"], data_dict.get("d) Identification of the property"))

        # 04.0 NATURE OF PROPERTY
        write_section_heading("04.0 NATURE OF PROPERTY")
        add_template_paragraph(pdf, TEMPLATE["04.0 NATURE OF PROPERTY"], data_dict.get("g) Nature of the property"))

        # 05.0 SITE PROFILE
        write_section_heading("05.0 SITE PROFILE")
        # 05.1 LAND
        add_template_paragraph(pdf, "05.1 LAND\n" + "Explain the geographical features of the land (shape, terrain, topography, soil condition, elevation, plantation, etc.).", data_dict.get("h) Site profile"))
        # 05.2 BUILDING
        write_section_heading("05.2 BUILDING")
        add_template_paragraph(pdf, "Describe the building (roof to foundation), internal/external features and floor area. A pictorial view is recommended below.", None)

        # Insert property images for parts (after heading)
        if data_dict.get("r) Property Images"):
            for img_info in data_dict["r) Property Images"]:
                try:
                    pdf.set_font("Arial", "I", 11)
                    pdf.multi_cell(0, 6, f"{img_info['part']}:")
                    # insert image and keep width consistent
                    if os.path.exists(img_info["path"]):
                        pdf.image(img_info["path"], x=25, y=None, w=160)
                    pdf.ln(4)
                except Exception:
                    # ignore individual image errors
                    pass

        # 06.0 EVIDENCE OF MARKET VALUES
        write_section_heading("06.0 EVIDENCE OF MARKET VALUES")
        add_template_paragraph(pdf, TEMPLATE["06.0 EVIDENCE OF MARKET VALUES"], data_dict.get("i) Market value evidence"))

        # 07.0 ASSUMPTION AND RESERVATION
        write_section_heading("07.0 ASSUMPTION AND RESERVATION")
        add_template_paragraph(pdf, TEMPLATE["07.0 ASSUMPTION AND RESERVATION"], data_dict.get("j) Assumptions and reservations"))

        # 08.0 BASIS OF VALUATION
        write_section_heading("08.0 BASIS OF VALUATION")
        add_template_paragraph(pdf, TEMPLATE["08.0 BASIS OF VALUATION"], data_dict.get("e) Basis of value adopted"))

        # 09.0 VALUATION APPROACH AND REASONING
        write_section_heading("09.0 VALUATION APPROACH AND REASONING")
        add_template_paragraph(pdf, TEMPLATE["09.0 VALUATION APPROACH AND REASONING"], data_dict.get("k) Valuation approach"))

        # 10.0 CERTIFICATE
        write_section_heading("10.0 CERTIFICATE")
        # We'll include the prepared-by block using the valuer name and report date
        certificate_paragraph = TEMPLATE["10.0 CERTIFICATE"] + "\n\n" + \
                                "Yours Sincerely,\n\n" + \
                                "{valuer_name}\nChartered Valuation Surveyor\n\n" + \
                                "Date of Report: {date_of_report}\n\nDISCLAIMER:\nThis template is intended as a general framework only..."

        # replace placeholders
        valuer_name = data_dict.get("a) Identification and status of the valuer", "__________")
        date_of_report = data_dict.get("m) Date of the valuation report")
        date_of_report_str = date_of_report.strftime("%Y-%m-%d") if date_of_report else "__________"
        filled_certificate = certificate_paragraph.format(valuer_name=valuer_name, date_of_report=date_of_report_str)
        # print certificate paragraph template (explanatory)
        add_template_paragraph(pdf, filled_certificate, None)

        # Finally generated info and signature
        pdf.ln(6)
        pdf.set_text_color(128, 0, 0)
        pdf.set_font("Arial", "B", 11)
        pdf.cell(0, 10, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align="R")

        # Output file
        filename = f"valuation_report_{report_id}.pdf"
        pdf.output(filename)
        return filename

    # --- GENERATE PDF BUTTON ---
    if st.button("📄 Generate PDF Report", use_container_width=True):
        pdf_path = generate_pdf(fields)
        # show preview and download
        with open(pdf_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode("utf-8")
        with st.expander("📑 View Generated PDF", expanded=True):
            st.markdown(f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="700"></iframe>', unsafe_allow_html=True)
        with open(pdf_path, "rb") as file:
            st.download_button("⬇️ Download Valuation Report PDF", data=file, file_name=os.path.basename(pdf_path), mime="application/pdf")
        # cleanup local files (pdf + images)
        try:
            os.remove(pdf_path)
        except Exception:
            pass
        if fields.get("r) Property Images"):
            for img_info in fields["r) Property Images"]:
                try:
                    if os.path.exists(img_info["path"]):
                        os.remove(img_info["path"])
                except Exception:
                    pass

    st.markdown("</div>", unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("""
<hr>
<div class="footer">
© 2025 PROPIQ | Developed at the University of Sri Jayewardenepura
</div>
""", unsafe_allow_html=True)
