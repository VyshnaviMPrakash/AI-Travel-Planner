# AI Travel Planner for Students

This project helps students plan trips based on destination, budget, number of days, and interests using AI. It generates day-wise itineraries, shows location maps, suggests budget stays, provides travel options, and allows PDF download.

---

## Features
- Personalized AI travel planning
- Day-wise itinerary (Morning, Afternoon, Evening)
- Location map under each day
- Budget-friendly hostels & stays with maps
- Travel options (Bus, Train, Flight, Car)
- Estimated budget split
- Student travel tips
- Download travel plan as PDF

---

## Technologies Used
- Python
- Streamlit
- Hugging Face API
- Google Maps Embed
- ReportLab (for PDF generation)
- VS Code

---

## Files Explanation
- app.py – Main application file
- data.py - Contains destination data and helper information used in itinerary generation
- requirements.txt – Required libraries
- .streamlit/secrets.toml – API key configuration

---

## How to Run

1. Install the required libraries:
   pip install -r requirements.txt

2. Add your Hugging Face API key in:
   .streamlit/secrets.toml

3. Run the application:
   streamlit run app.py

---

## Project Workflow
1. User enters destination, days, budget, and interests
2. AI generates day-wise itinerary
3. Locations are extracted and shown with maps
4. Budget hostels & stays are suggested
5. Travel options are displayed
6. Budget is split into categories
7. User downloads travel plan as PDF

---

## Advantages
- Student-focused design
- Saves time and money
- Easy to use interface
- Real-world practical application
- All-in-one travel planning solution

---

## Future Scope
- Restaurant recommendations
- Distance calculation between places
- Multi-language support
- Mobile app version
- Group trip planning
- Hotel price comparison

---

## Conclusion
The AI Travel Planner for Students demonstrates how artificial intelligence and location-based services can be combined to build a practical and affordable travel solution for students. This project highlights the real-world application of AI in solving everyday problems.

---
