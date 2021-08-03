from app import App
from os import listdir

for resume in listdir("Resumes"):
	App(resume)