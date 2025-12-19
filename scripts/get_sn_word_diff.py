# For numbers reported in p. 191 n. 21

from glob import glob

speech = glob("data/speech_texts/*speech.txt")
narrative = glob("data/speech_texts/*narrative.txt")

print("Speech word count")
speech_count = sum([len(open(file).read().split()) for file in speech])
print(speech_count, "\n")

print("Narrative word count")
narrative_count = sum([len(open(file).read().split()) for file in narrative])
print(narrative_count, "\n")

print("Total word count")
total_count = speech_count + narrative_count
print(total_count, "\n")

print("Speech percentage")
print(f"{(speech_count / total_count) * 100:.1f}%", "\n")

print("Narrative percentage")
print(f"{(narrative_count / total_count) * 100:.1f}%", "\n")
