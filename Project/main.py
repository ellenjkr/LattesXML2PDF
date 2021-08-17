from resume import Resume
from word import WordFile
from os import listdir

for resume_name in listdir("Files/Resumes"):
	resume_path = "Files/Resumes/" + resume_name
	resume = Resume(resume_path)

	word = WordFile(resume)
	word.save_document(resume_name.replace('.xml', ''))