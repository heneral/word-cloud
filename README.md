# Survey Word Collector

This project is a simple survey form that allows users to submit words or short text responses.
Each submission is automatically saved (appended) to a .txt file for later analysis (e.g., word cloud generation).

It is designed for:

- Survey data collection
- Feedback gathering
- Research preparation

## 🎯 Features

- Simple survey response form
- Automatic saving to .txt file
- Timestamped entries
- Optional question field
- View collected responses
- Response statistics
- Download responses file
- Clean, form-based interface

## 🧰 Technologies Used

- Python 3
- Streamlit (Web-based user interface)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/heneral/word-cloud.git
   cd word-cloud
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Web Application

Run the survey collection form:

```bash
streamlit run app.py
```

Then open your browser to `http://localhost:8501`

**Features:**
- Text area for survey responses
- Optional question field
- Automatic saving with timestamps
- View all collected responses
- Basic statistics
- Download responses as .txt file

### Response Format

Each saved response includes:
```
[2025-12-30 20:15:30] Question: What did you think of the service?
Response: The service was excellent and very helpful.
--------------------------------------------------
```

## 📁 File Structure

```
survey-word-collector/
│
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── survey_responses.txt   # Auto-generated responses file
└── README.md             # This file
```

## 🔄 Workflow

1. User opens the survey form
2. User enters their response (and optional question)
3. Clicks "Save Response"
4. Response is appended to `survey_responses.txt` with timestamp
5. User can view all responses or download the file
6. Later, use the collected data for word cloud analysis or other processing

## 📊 Use Cases

- **Academic Research**: Collect student feedback or survey responses
- **Customer Feedback**: Gather opinions before analysis
- **Event Surveys**: Collect attendee responses
- **Product Testing**: Gather user impressions
- **Research Preparation**: Build datasets for analysis

## 📋 Response Management

- **View Responses**: Click "View All Responses" to see all collected data
- **Statistics**: Get basic counts of responses, words, and file size
- **Download**: Export all responses as a .txt file for external analysis
- **File Location**: Responses are saved as `survey_responses.txt` in the app directory

## 🔒 Data Storage

- All responses are stored locally in a plain text file
- No external databases required
- Easy to backup and share
- Human-readable format for manual review

## 📈 Next Steps

Once you've collected survey responses, you can:

1. **Generate Word Clouds**: Use the collected data with word cloud tools
2. **Text Analysis**: Perform sentiment analysis or topic modeling
3. **Data Export**: Import into Excel, SPSS, or other analysis tools
4. **Reporting**: Create visualizations and reports from the collected feedback

## 📄 License

This project is open-source and intended for educational and research use.</content>
<parameter name="filePath">/home/richardsawanaka/Documents/Workspace/word-cloud/word-cloud/README.md
