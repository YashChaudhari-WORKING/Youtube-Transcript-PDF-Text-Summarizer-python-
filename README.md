

# Youtube Transcript , pdf , text summarizer

## Introduction

The Multi-Application Summarizer is a Python project that provides three distinct applications for summarizing text:

1. **YouTube Transcript App**: Extracts and summarizes transcripts from YouTube videos.
2. **Text Summarizer App**: Summarizes user-provided text.
3. **PDF Reader App**: Extracts and summarizes text from PDF files.

The applications are accessible through a main menu and offer a user-friendly graphical interface built with Tkinter.

## Libraries and Installation

### Required Libraries

To run this project, you need to install the following Python libraries:

- `tkinter` - For the graphical user interface.
- `spacy` - For natural language processing and text summarization.
- `youtube_transcript_api` - For extracting YouTube video transcripts.
- `PyPDF2` - For reading PDF files.
- `Pillow` - For handling images in the GUI.

### Installation Steps

1. **Clone the repository**:

2. **Install required packages**:
   ```bash
   pip install spacy youtube-transcript-api PyPDF2 Pillow
   ```

3. **Download the spaCy model**:
   ```bash
   python -m spacy download en_core_web_sm
   ```

## Troubleshooting

If you encounter errors related to UI images, please check the following:

- Ensure that the image files are correctly named and placed in the appropriate directory. The paths specified in the code should match the locations of your image files.

- Common image paths to verify:
  - For the main application: `main.jpeg`
  - For the YouTube Transcript App: `youtube1.png`
  - For the Text Summarizer App: `text1.jpeg`
  - For the PDF Reader App: `pdf.png`

If you continue to face issues, please verify the file paths and ensure that the image files are in the correct format and accessible.

## Running the Application

To start the main application, run the following command:

```bash
python main.py
```

This will launch the main menu from which you can select and open any of the three summarizer applications.

For further assistance or to report issues, please open an issue on the GitHub repository.

```

