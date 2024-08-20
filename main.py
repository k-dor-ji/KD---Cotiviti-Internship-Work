#nltk -- reportlab required

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Download NLTK resources if not already downloaded
# nltk.download('punkt')
# nltk.download('stopwords')

def summarize_text():
    text = text_area.get("1.0", tk.END).strip()
    stopWords = set(stopwords.words("english"))
    words = word_tokenize(text)

    freqTable = {}
    for word in words:
        word = word.lower()
        if word not in stopWords:
            if word in freqTable:
                freqTable[word] += 1
            else:
                freqTable[word] = 1

    max_freq = max(freqTable.values())  # Find the maximum frequency
    for word in freqTable:
        freqTable[word] = (freqTable[word] / max_freq)  # Normalize frequencies

    sentences = sent_tokenize(text)
    sentenceValue = {}

    for sentence in sentences:
        for word, freq in freqTable.items():
            if word in sentence.lower():
                if sentence in sentenceValue:
                    sentenceValue[sentence] += freq
                else:
                    sentenceValue[sentence] = freq

    threshold = 1.5 * sum(sentenceValue.values()) / len(sentenceValue)

    summary = ""
    for sentence in sentences:
        if sentence in sentenceValue and sentenceValue[sentence] >= threshold:
            summary += " " + sentence

    summary_area.delete("1.0", tk.END)
    summary_area.insert(tk.END, summary)

def reset_text():
    text_area.delete("1.0", tk.END)
    summary_area.delete("1.0", tk.END)

def export_text():
    summary = summary_area.get("1.0", tk.END).strip()
    if not summary:
        messagebox.showerror("Error", "No summary to export")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(summary)
        messagebox.showinfo("Success", "Summary exported successfully")

# GUI
root = tk.Tk()
root.title("Text Summarizer")

text_label = tk.Label(root, text="Enter text to summarize:")
text_label.pack(pady=5)
text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=10)
text_area.pack(pady=5)

summarize_button = tk.Button(root, text="Summarize", command=summarize_text)
summarize_button.pack(pady=5)

reset_button = tk.Button(root, text="Reset", command=reset_text)
reset_button.pack(pady=5)

export_button = tk.Button(root, text="Export as Text File", command=export_text)
export_button.pack(pady=5)

summary_label = tk.Label(root, text="Summary:")
summary_label.pack(pady=5)
summary_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=10)
summary_area.pack(pady=5)

root.mainloop()
