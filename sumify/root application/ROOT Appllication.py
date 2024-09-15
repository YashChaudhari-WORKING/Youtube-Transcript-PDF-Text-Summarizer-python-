import tkinter as tk
from tkinter import Toplevel, scrolledtext, messagebox, filedialog
from youtube_transcript_api import YouTubeTranscriptApi
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
from PyPDF2 import PdfReader, PdfWriter
from PIL import Image, ImageTk
import traceback

class YouTubeTranscriptApp:
    def _init_(self, master):
        self.master = master
        master.title("YouTube Transcript App")
        
        # Set window size
        master.geometry("650x670")

        # Load and place background image
        try:
            background_image = Image.open("youtube1.png")  # Replace "youtube_bg.png" with your image path
            background_photo = ImageTk.PhotoImage(background_image)
            background_label = tk.Label(master, image=background_photo)
            background_label.place(relwidth=1, relheight=1)
            background_label.image = background_photo  # Keep a reference to prevent garbage collection
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load background image: {e}")
            traceback.print_exc()

        # Apply blur effect to text fields
        self.transcript_output = scrolledtext.ScrolledText(master, width=69, height=9, bg="white", wrap=tk.WORD)
        self.transcript_output.place(x=40, y=210)

        self.summary_output = scrolledtext.ScrolledText(master, width=69, height=9, bg="white", wrap=tk.WORD)
        self.summary_output.place(x=40, y=415)

        # Create YouTube link entry
        self.youtube_link_entry = tk.Entry(master, width=58, bg="Gray", highlightthickness=5)
        self.youtube_link_entry.config(font=('Arial', 12), relief=tk.FLAT)
        self.youtube_link_entry.place(x=60, y=105, height=50)

        # Create generate transcript button
        self.transcript_button = tk.Button(master, text="Generate", command=self.generate_and_summarize_transcript, width=15, height=2, bg="#80EAFF")
        self.transcript_button.place(x=400, y=590)

        # Create copy button
        self.copy_button = tk.Button(master, text="Copy Summary", command=self.copy_summary, width=15, height=2, bg="#008000")
        self.copy_button.place(x=70, y=591)

        # Create reset button
        self.reset_button = tk.Button(master, text="Reset", command=self.reset, width=10, height=2, bg="#CC2200")
        self.reset_button.place(x=230, y=591)

    def generate_and_summarize_transcript(self):
        youtube_link = self.youtube_link_entry.get()
        if not youtube_link.strip():
            messagebox.showerror("Error", "Please enter a YouTube link.")
            return

        try:
            video_id = self.extract_video_id(youtube_link)
            transcript = self.get_youtube_transcript(video_id)
            if transcript:
                self.transcript_output.delete('1.0', tk.END)
                self.transcript_output.insert(tk.END, transcript)
                summary = self.summarize_text(transcript)
                self.summary_output.delete('1.0', tk.END)
                self.summary_output.insert(tk.END, summary)
            else:
                messagebox.showerror("Error", "Failed to fetch transcript.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def extract_video_id(self, youtube_link):
        if 'youtube.com' in youtube_link:
            video_id = youtube_link.split('=')[-1]
            return video_id
        elif 'youtu.be' in youtube_link:
            video_id = youtube_link.split('/')[-1]
            return video_id
        else:
            raise ValueError("Invalid YouTube link format.")

    def get_youtube_transcript(self, video_id):
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        text = ''
        for line in transcript:
            text += line['text'] + ' '
        return text

    def summarize_text(self, text):
        stopwords = list(STOP_WORDS)
        nlp = spacy.load('en_core_web_sm')
        doc = nlp(text)

        wordFrequency = {}
        for word in doc:
            if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
                if word.text not in wordFrequency.keys():
                    wordFrequency[word.text] = 1
                else:
                    wordFrequency[word.text] += 1

        maxFrequency = max(wordFrequency.values())

        for word in wordFrequency.keys():
            wordFrequency[word] = wordFrequency[word] / maxFrequency

        sent_token = [sent for sent in doc.sents]

        sent_score = {}
        for sent in sent_token:
            for word in sent:
                if word.text in wordFrequency.keys():
                    if sent not in sent_score.keys():
                        sent_score[sent] = wordFrequency[word.text]
                    else:
                        sent_score[sent] += wordFrequency[word.text]

        select_len = int(len(sent_token) * 0.3)
        summary = nlargest(select_len, sent_score, key=sent_score.get)

        final_summary = [word.text for word in summary]
        return ' '.join(final_summary)

    def copy_summary(self):
        summary_text = self.summary_output.get("1.0", tk.END)
        self.master.clipboard_clear()
        self.master.clipboard_append(summary_text)

    def reset(self):
        self.youtube_link_entry.delete(0, tk.END)
        self.transcript_output.delete('1.0', tk.END)
        self.summary_output.delete('1.0', tk.END)

class TextSummarizerApp:
    def _init_(self, master):
        self.master = master
        master.title("Text Summarizer")
        
        # Set window size
        master.geometry("650x670")

        # Load and place background image
        try:
            background_image = Image.open("text1.jpeg")  # Replace "text_bg.png" with your image path
            background_photo = ImageTk.PhotoImage(background_image)
            background_label = tk.Label(master, image=background_photo)
            background_label.place(relwidth=1, relheight=1)
            background_label.image = background_photo  # Keep a reference to prevent garbage collection
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load background image: {e}")
            traceback.print_exc()

        # Create text input area with blurred background color
        self.text_input = scrolledtext.ScrolledText(master, width=69, height=9, bg="lightblue")
        self.text_input.place(x=38, y=105)

        # Create summarize button with custom properties
        self.summarize_button = tk.Button(master, text="Summarize", command=self.summarize_text, bg="green", fg="black", width=10, height=1, font=("Arial", 12, "bold"))
        self.summarize_button.place(x=460, y=497)

        # Create summary output area with blurred background color
        self.summary_output = scrolledtext.ScrolledText(master, width=69, height=9, bg="lightblue")
        self.summary_output.place(x=38, y=305)

        # Create word count label for input text
        self.input_word_count_label = tk.Label(master, text="Input Word Count:", font=("Arial", 12))
        self.input_word_count_label.place(x=40, y=580)

        # Create word count output label for input text
        self.input_word_count_output = tk.Label(master, text="", bg="red", font=("Arial", 12))
        self.input_word_count_output.place(x=190, y=580)

        # Create word count label for summary text
        self.summary_word_count_label = tk.Label(master, text="Summary Word Count:", font=("Arial", 12))
        self.summary_word_count_label.place(x=330, y=580)

        # Create word count output label for summary text
        self.summary_word_count_output = tk.Label(master, text="", bg="green", font=("Arial", 12))
        self.summary_word_count_output.place(x=510, y=580)

        # Create reset button with custom properties
        self.reset_button = tk.Button(master, text="Reset", command=self.reset, bg="red", fg="black", width=8, height=1, font=("Arial", 12, "bold"))
        self.reset_button.place(x=80, y=497)

        # Create copy button with custom properties
        self.copy_button = tk.Button(master, text="Copy Summary", command=self.copy_summary, bg="orange", fg="black", width=12, height=1, font=("Arial", 12, "bold"))
        self.copy_button.place(x=220, y=497)

    def summarize_text(self):
        text = self.text_input.get("1.0", tk.END)
        if not text.strip():
            messagebox.showerror("Error", "Please enter some text to summarize.")
            return

        stopwords = list(STOP_WORDS)
        nlp = spacy.load('en_core_web_sm')
        doc = nlp(text)

        # Calculate word count for input text
        input_word_count = len(text.split())
        self.input_word_count_output.config(text=str(input_word_count))

        wordFrequency = {}
        for word in doc:
            if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
                if word.text not in wordFrequency.keys():
                    wordFrequency[word.text] = 1
                else:
                    wordFrequency[word.text] += 1

        maxFrequency = max(wordFrequency.values())

        for word in wordFrequency.keys():
            wordFrequency[word] = wordFrequency[word] / maxFrequency

        sent_token = [sent for sent in doc.sents]

        sent_score = {}
        for sent in sent_token:
            for word in sent:
                if word.text in wordFrequency.keys():
                    if sent not in sent_score.keys():
                        sent_score[sent] = wordFrequency[word.text]
                    else:
                        sent_score[sent] += wordFrequency[word.text]

        select_len = int(len(sent_token) * 0.3)
        summary = nlargest(select_len, sent_score, key=sent_score.get)

        final_summary = ' '.join([sent.text for sent in summary])  # Extract text from Spacy Span objects
        self.summary_output.delete('1.0', tk.END)
        self.summary_output.insert(tk.END, final_summary)

        # Calculate word count for summary text
        summary_word_count = len(final_summary.split())
        self.summary_word_count_output.config(text=str(summary_word_count))

    def copy_summary(self):
        summary_text = self.summary_output.get("1.0", tk.END)
        self.master.clipboard_clear()
        self.master.clipboard_append(summary_text)

    def reset(self):
        self.text_input.delete('1.0', tk.END)
        self.summary_output.delete('1.0', tk.END)
        self.input_word_count_output.config(text="")
        self.summary_word_count_output.config(text="")

class PDFReaderApp:
    def _init_(self, master):
        self.master = master
        master.title("PDF Reader")
        master.geometry("650x670")

        # Create a label for the background image
        self.background_label = tk.Label(master)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Load and place background image
        try:
            background_image = tk.PhotoImage(file="E:\\nlp\\pdf.png")  # Replace "pdf_bg.png" with your image path
            self.background_label.configure(image=background_image)
            self.background_label.image = background_image  # Keep a reference
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load background image: {e}")

        # Create browse button
        self.browse_button = tk.Button(master, text="Browse PDF", command=self.browse_pdf, bg="#d1c2c7", width=15, height=2, font=("Arial", 10, "bold"))
        self.browse_button.place(x=275, y=120)

        # Create text box for displaying summarized text
        self.summary_text_box = scrolledtext.ScrolledText(master, width=68, height=15, bg="white")
        self.summary_text_box.place(x=39, y=230)

        # Create copy button
        self.copy_button = tk.Button(master, text="Copy Summary", command=self.copy_summary, bg="#d18b00", width=12, height=2, font=("Arial", 10, "bold"))
        self.copy_button.place(x=85, y=512)

        # Create save as PDF button
        self.save_as_pdf_button = tk.Button(master, text="Save as PDF", command=self.save_as_pdf, bg="#004D1A", height=2, font=("Arial", 10, "bold"))
        self.save_as_pdf_button.place(x=275, y=572)

        # Create reset button
        self.reset_button = tk.Button(master, text="Reset", command=self.reset, bg="#940000", width=12, height=2, font=("Arial", 10, "bold"))
        self.reset_button.place(x=240, y=512)

    def browse_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            try:
                summarized_text = self.summarize_text_from_pdf(file_path)
                self.summary_text_box.delete('1.0', tk.END)
                self.summary_text_box.insert(tk.END, summarized_text)
            except Exception as e:
                self.summary_text_box.delete('1.0', tk.END)
                self.summary_text_box.insert(tk.END, f"An error occurred: {str(e)}")

    def summarize_text_from_pdf(self, file_path):
        text = ''
        with open(file_path, 'rb') as file:
            reader = PdfReader(file)
            num_pages = len(reader.pages)
            for page_num in range(num_pages):
                page = reader.pages[page_num]
                text += page.extract_text()

        stopwords = list(STOP_WORDS)
        nlp = spacy.load('en_core_web_sm')
        doc = nlp(text)

        wordFrequency = {}
        for word in doc:
            if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
                if word.text not in wordFrequency.keys():
                    wordFrequency[word.text] = 1
                else:
                    wordFrequency[word.text] += 1

        maxFrequency = max(wordFrequency.values())

        for word in wordFrequency.keys():
            wordFrequency[word] = wordFrequency[word] / maxFrequency

        word_scores = {}
        for token in doc:
            if token.text in wordFrequency.keys():
                word_scores[token.text] = wordFrequency[token.text]

        select_len = int(len(doc) * 0.3)
        summary = nlargest(select_len, word_scores, key=word_scores.get)

        final_summary = ' '.join(summary)
        return final_summary

    def copy_summary(self):
        summary_text = self.summary_text_box.get("1.0", tk.END)
        self.master.clipboard_clear()
        self.master.clipboard_append(summary_text)

    def save_as_pdf(self):
        summary_text = self.summary_text_box.get("1.0", tk.END)
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if file_path:
            writer = PdfWriter()
            writer.add_page(summary_text)
            with open(file_path, 'wb') as f:
                writer.write(f)

    def reset(self):
        self.summary_text_box.delete('1.0', tk.END)

    def change_button_color(self, button, rgb):
        button.config(bg='#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2]))

def open_youtube_transcript_app():
    window = Toplevel(root)
    app = YouTubeTranscriptApp(window)

def open_text_summarizer_app():
    window = Toplevel(root)
    app = TextSummarizerApp(window)

def open_pdf_reader_app():
    window = Toplevel(root)
    app = PDFReaderApp(window)

root = tk.Tk()
root.title("Main Application")
root.geometry("1200x650")

# Set background image
background_image = Image.open("main.jpeg")  # Replace "main_bg.png" with your image path
background_photo = ImageTk.PhotoImage(background_image)
background_label = tk.Label(root, image=background_photo)
background_label.place(relwidth=1, relheight=1)
background_label.image = background_photo  # Keep a reference to prevent garbage collection

# Create buttons to open applications
youtube_button = tk.Button(root, text="OPEN", command=open_youtube_transcript_app, bg="#F87F7F", fg="black", font=("Arial", 18),height=1,width=8)
youtube_button.place(x=95, y=345)

text_summarizer_button = tk.Button(root, text="OPEN", command=open_text_summarizer_app, bg="#BF8AE4", fg="black", font=("Arial", 18),height=1,width=8)
text_summarizer_button.place(x=490, y=328)

pdf_reader_button = tk.Button(root, text="OPEN", command=open_pdf_reader_app, bg="#5195DC", fg="black", font=("Arial", 18),height=1,width=8)
pdf_reader_button.place(x=875, y=325)

root.mainloop()