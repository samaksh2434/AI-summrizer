from src.summarizer import summarize

print("Paste your text (end with ENTER):")
text = input()

length = input("Enter summary length (short / medium / long): ").strip().lower()

print("\nSUMMARY:\n")
print(summarize(text, length))
