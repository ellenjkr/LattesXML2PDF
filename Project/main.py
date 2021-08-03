from app import App
from word import WordFile
from os import listdir

for resume in listdir("Resumes"):
	resume_path = "Resumes/" + resume
	app = App(resume_path)

	word = WordFile(app.presentation, app.abstract, app.identification)
	word.save_document('test')