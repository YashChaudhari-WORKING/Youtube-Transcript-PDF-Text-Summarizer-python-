import tkinter as tk
from tkinter import scrolledtext, messagebox
from youtube_transcript_api import YouTubeTranscriptApi
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest

class YouTubeTranscriptApp:
    def __init__(self, master):
        self.master = master
        master.title("YouTube Transcript App")
        
        # Set window size
        master.geometry("650x670")

        # Load and place background image
        try:
            background_image = Image.open("youtube1.png")  # Replace "youtube1.png" with your image path
            background_photo = ImageTk.PhotoImage(background_image)
            background_label = tk.Label(master, image=background_photo)
            background_label.place(relwidth=1, relheight=1)
            background_label.image = background_photo  # Keep a reference to prevent garbage collection
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load background image: {e}")

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

        final_summary = [sent.text for sent in summary]
        return ' '.join(final_summary)

    def copy_summary(self):
        summary_text = self.summary_output.get("1.0", tk.END)
        self.master.clipboard_clear()
        self.master.clipboard_append(summary_text)

    def reset(self):
        self.youtube_link_entry.delete(0, tk.END)
        self.transcript_output.delete('1.0', tk.END)
        self.summary_output.delete('1.0', tk.END)
