from resume import Resume
from word import WordFile
from os import listdir

for resume in listdir("Resumes"):
	resume_path = "Resumes/" + resume
	resume = Resume(resume_path)

	word = WordFile(resume.presentation, resume.abstract, resume.identification, resume.address, resume.publications_dict)
	word.save_document('test')