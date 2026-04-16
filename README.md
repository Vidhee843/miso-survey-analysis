# FSU MISO Survey — Data Storytelling & Visualization 📊

A data storytelling project analyzing Florida State University's MISO Survey data to surface actionable IT service insights for university leadership.

## Overview
Cleaned and analyzed two **Qualtrics-exported MISO Survey datasets** (student & staff) to identify gaps between IT service availability and awareness, following Brent Dykes' *Effective Data Storytelling* framework.

## Key Findings
- 📉 Only **7% of students** felt informed about available IT services
- 📉 Only **14% of staff** felt informed — despite **high Help Desk satisfaction ratings**
- 💡 Major gap identified between service quality and service awareness
- 📋 Findings presented as a **Data Trailer memo** to a simulated CIO audience

## Tech Stack
- **Language:** Python
- **Libraries:** Pandas, Matplotlib, Seaborn, NumPy
- **Methods:** Gap Analysis, Frequency Distributions, Animated Visualizations
- **Framework:** Brent Dykes' Effective Data Storytelling

## Project Structure
```
miso-survey-analysis/
│
├── data/                   # Qualtrics exported datasets (student & staff)
├── notebooks/
│   ├── data_cleaning.ipynb
│   ├── gap_analysis.ipynb
│   └── visualizations.ipynb
├── outputs/
│   ├── visualizations/     # 4 animated Python visualizations
│   └── data_trailer_memo/  # Executive summary memo
└── README.md
```

## Methodology
1. **Data Cleaning** — handled missing values, standardized Qualtrics export format
2. **Gap Analysis** — compared awareness vs. satisfaction scores across service categories
3. **Frequency Distributions** — identified most/least known IT services
4. **Storytelling** — structured findings using ABCD data storytelling framework
5. **Visualization** — produced 4 animated charts for executive presentation

## How to Run
```bash
# Clone the repository
git clone https://github.com/Vidhee843/miso-survey-analysis.git

# Install dependencies
pip install -r requirements.txt

# Run analysis notebooks
jupyter notebook notebooks/gap_analysis.ipynb
```

## Business Impact
Recommendations delivered to simulated CIO included targeted IT service awareness campaigns, improved onboarding communication, and department-specific outreach strategies.

## Team
Built as part of MISM 6213 — Business Information Design, Quality & Strategy at Northeastern University (Spring 2025). Prof. Patrick Laughran. Team of 4.
