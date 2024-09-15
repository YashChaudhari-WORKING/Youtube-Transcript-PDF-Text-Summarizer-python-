import tkinter as tk
from youtube_transcript_app import YouTubeTranscriptApp
from text_summarizer_app import TextSummarizerApp
from pdf_reader_app import PDFReaderApp

def main():
    root = tk.Tk()
    root.title("Main Menu")

    def open_youtube_transcript_app():
        root.withdraw()
        new_window = tk.Toplevel(root)
        YouTubeTranscriptApp(new_window)
    
    def open_text_summarizer_app():
        root.withdraw()
        new_window = tk.Toplevel(root)
        TextSummarizerApp(new_window)
    
    def open_pdf_reader_app():
        root.withdraw()
        new_window = tk.Toplevel(root)
        PDFReaderApp(new_window)

    tk.Button(root, text="YouTube Transcript App", command=open_youtube_transcript_app).pack(pady=10)
    tk.Button(root, text="Text Summarizer App", command=open_text_summarizer_app).pack(pady=10)
    tk.Button(root, text="PDF Reader App", command=open_pdf_reader_app).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
