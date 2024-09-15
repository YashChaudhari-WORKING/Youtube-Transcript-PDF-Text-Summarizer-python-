import tkinter as tk
from tkinter import scrolledtext, messagebox
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest

class TextSummarizerApp:
    def __init__(self, master):
        self.master = master
        master.title("Text Summarizer")
        
        # Set window size
        master.geometry("650x670")

        # Load and place background image
        try:
            background_image = Image.open("text1.jpeg")  # Replace "text1.jpeg" with your image path
            background_photo = ImageTk.PhotoImage(background_image)
            background_label = tk.Label(master, image=background_photo)
            background_label.place(relwidth=1, relheight=1)
            background_label.image = background_photo  # Keep a reference to prevent garbage collection
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load background image: {e}")

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
        self.summary_output.delete('1.0', tk.END)
        self.summary_output.insert(tk.END, ' '.join(final_summary))
        self.update_word_counts(text, ' '.join(final_summary))

    def update_word_counts(self, input_text, summary_text):
        input_word_count = len(input_text.split())
        summary_word_count = len(summary_text.split())

        self.input_word_count_output.config(text=str(input_word_count))
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
