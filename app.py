import streamlit as st
from huggingface_hub import InferenceClient

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import io

st.set_page_config(page_title="AI Travel Planner for Students")

st.title("🎒 AI Travel Planner for Students")
st.write("AI-powered, personalized, budget-friendly travel plans with maps, stays, transport info & PDF download")

# ---------------- LOAD HF TOKEN ----------------
HF_TOKEN = st.secrets["HF_TOKEN"]

client = InferenceClient(
    model="meta-llama/Meta-Llama-3-8B-Instruct",
    token=HF_TOKEN
)

# ---------------- MAP FUNCTION ----------------
def show_map_for_location(location_name):
    map_url = f"https://www.google.com/maps?q={location_name}&output=embed"
    st.components.v1.iframe(map_url, width=700, height=400)

# ---------------- BUDGET STAYS FUNCTION ----------------
def get_budget_stays_list(city):
    prompt = f"""
List 4 budget-friendly hostels or hotels for students in {city}.
Return ONLY the names, one per line. No explanation.
"""

    messages = [
        {"role": "system", "content": "You are a helpful travel assistant."},
        {"role": "user", "content": prompt}
    ]

    response = client.chat_completion(
        messages=messages,
        max_tokens=200,
        temperature=0.6
    )

    text = response.choices[0].message.content

    stays = []
    for line in text.split("\n"):
        line = line.strip()
        if line:
            stays.append(line.lstrip("-•0123456789. ").strip())

    return stays

# ---------------- TRAVEL OPTIONS FUNCTION ----------------
def get_travel_options(city):
    prompt = f"""
Explain how students can travel to and within {city} using:
1. Bus
2. Train
3. Flight
4. Car

Give short, simple, student-friendly points.
"""

    messages = [
        {"role": "system", "content": "You are a helpful travel assistant."},
        {"role": "user", "content": prompt}
    ]

    response = client.chat_completion(
        messages=messages,
        max_tokens=300,
        temperature=0.6
    )

    return response.choices[0].message.content

# ---------------- PDF GENERATION FUNCTION ----------------
def generate_pdf(content_text):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    for line in content_text.split("\n"):
        story.append(Paragraph(line, styles["Normal"]))
        story.append(Spacer(1, 8))

    doc.build(story)
    buffer.seek(0)
    return buffer

# ---------------- USER INPUTS ----------------
place = st.text_input("📍 Enter Destination", placeholder="Eg: Delhi, Goa, Paris")
days = st.number_input("📅 Number of Days", min_value=1, max_value=30, value=3)
budget = st.number_input("💰 Budget (INR)", min_value=1000, value=3000)

ALL_INTERESTS = [
    "Adventure", "Relaxation", "Culture", "Food", "Nature",
    "Historical Places", "Shopping", "Photography", "Nightlife",
    "Spiritual", "Wildlife", "Budget Travel"
]

selected = st.multiselect(
    "🎯 Select Interests (You can choose multiple)",
    ["Select All"] + ALL_INTERESTS
)

if "Select All" in selected:
    interests = ALL_INTERESTS
else:
    interests = selected

# ---------------- GENERATE PLAN ----------------
if st.button("Generate Travel Plan"):
    if place.strip() == "":
        st.error("Please enter a destination")
    else:
        st.success("Your AI Travel Plan is Ready!")

        pdf_text = ""

        # Destination Map
        st.subheader("🗺️ Destination Location")
        show_map_for_location(place)

        interest_text = ", ".join(interests) if interests else "general travel"

        # ---------------- AI PROMPT ----------------
        messages = [
            {
                "role": "system",
                "content": "You are an expert travel planner for students."
            },
            {
                "role": "user",
                "content": f"""
Create a {days}-day budget-friendly travel itinerary for {place}.
Budget: {budget} INR.
Interests: {interest_text}.

Important:
- Start each day with "Day 1:", "Day 2:" etc.
- Use real famous places in {place}
- After each Day line, give Morning, Afternoon, Evening details.
- Do NOT write summary or budget before Day 1.

Format example:
Day 1: <Place Name>, {place} - Short title
Morning: ...
Afternoon: ...
Evening: ...
"""
            }
        ]

        try:
            with st.spinner("AI is generating your itinerary..."):
                response = client.chat_completion(
                    messages=messages,
                    max_tokens=900,
                    temperature=0.7
                )

                itinerary = response.choices[0].message.content

            pdf_text += "DAY-WISE ITINERARY\n" + itinerary + "\n\n"

            # ---------------- DAY-WISE ITINERARY + MAP ----------------
            st.subheader("📅 Day-wise Itinerary with Location Maps")

            lines = itinerary.split("\n")

            current_day_block = []
            current_place = ""
            day_started = False

            for line in lines:
                line = line.strip()

                if line.lower().startswith("day"):
                    day_started = True

                    if current_day_block:
                        st.markdown("\n".join(current_day_block))
                        if current_place:
                            show_map_for_location(f"{current_place}, {place}")
                        st.markdown("---")

                    current_day_block = [f"### {line}"]
                    current_place = ""

                    try:
                        _, rest = line.split(":", 1)
                        place_part = rest.split("-")[0].strip()
                        current_place = place_part
                    except:
                        current_place = ""

                else:
                    if day_started and line != "":
                        current_day_block.append(f"- {line}")

            if current_day_block:
                st.markdown("\n".join(current_day_block))
                if current_place:
                    show_map_for_location(f"{current_place}, {place}")

        except Exception as e:
            st.error(f"AI Error: {e}")

        # ---------------- BUDGET HOSTELS / STAYS ----------------
        st.markdown("---")
        st.subheader("🏨 Budget-Friendly Hostels & Stays for Students")

        with st.spinner("Finding budget hostels and stays for students..."):
            stays = get_budget_stays_list(place)

        pdf_text += "BUDGET HOSTELS / STAYS\n"

        if stays:
            for stay in stays:
                st.markdown(f"**{stay}**")
                show_map_for_location(f"{stay}, {place}")
                pdf_text += f"- {stay}\n"
        else:
            st.write("No hostel data found. Try another destination.")

        pdf_text += "\n"

        # ---------------- TRAVEL OPTIONS ----------------
        st.markdown("---")
        st.subheader("🚌✈️🚆 Travel Options for Students")

        with st.spinner("Finding best travel options for students..."):
            travel_info = get_travel_options(place)

        st.write(travel_info)
        pdf_text += "TRAVEL OPTIONS\n" + travel_info + "\n\n"

        # ---------------- ESTIMATED BUDGET SPLIT ----------------
        st.markdown("---")
        st.subheader("💸 Estimated Budget Split")
        st.write(f"🚕 Travel: ₹{int(budget * 0.4)}")
        st.write(f"🏨 Stay: ₹{int(budget * 0.3)}")
        st.write(f"🍴 Food: ₹{int(budget * 0.2)}")
        st.write(f"🛍️ Others: ₹{int(budget * 0.1)}")

        pdf_text += "ESTIMATED BUDGET SPLIT\n"
        pdf_text += f"Travel: ₹{int(budget * 0.4)}\n"
        pdf_text += f"Stay: ₹{int(budget * 0.3)}\n"
        pdf_text += f"Food: ₹{int(budget * 0.2)}\n"
        pdf_text += f"Others: ₹{int(budget * 0.1)}\n\n"

        # ---------------- STUDENT TIPS ----------------
        st.markdown("---")
        st.subheader("🎓 Student Tips")
        st.write("✔ Use public transport")
        st.write("✔ Book hostels or budget stays")
        st.write("✔ Travel in groups")
        st.write("✔ Avoid peak seasons")

        pdf_text += "STUDENT TIPS\n"
        pdf_text += "• Use public transport\n• Book hostels or budget stays\n• Travel in groups\n• Avoid peak seasons\n\n"

        # ---------------- DOWNLOAD PDF ----------------
        st.markdown("---")
        st.subheader("⬇️ Download Your Travel Plan")

        pdf_file = generate_pdf(pdf_text)

        st.download_button(
            label="Download Travel Plan as PDF",
            data=pdf_file,
            file_name="AI_Travel_Plan.pdf",
            mime="application/pdf"
        )
