import docx2txt
from PyPDF2 import PdfReader
import os


# usage
# rf = ReadFiles(r"C:\Users\manoj\Desktop\projectresumes\pdf")
# rf.read_resumes()
# print(rf.text_dict) text_dict- is a dictionary to store filepath and text in that file

# Input folder where the resumes are present to read all the resumes in the folder
# It can detect extensions and read resumes based on extension.
class ReadFiles:

    def __init__(self, folder_path):
        self.files_path = list()
        self.text_dict = dict()
        if os.path.exists(folder_path):
            self.folder_path = folder_path
        else:
            raise ValueError("Path not found!!")

    # list all the files present in a folder
    @staticmethod
    def get_files(filepath):
        return os.listdir(filepath)

    # Get file extension
    @staticmethod
    def get_file_extension(filepath):
        return os.path.splitext(filepath)[-1]

    # Read all the resumes from a given folder and return list of text from resumes
    def read_resumes(self):
        self.files_path = list()
        self.files_path = [os.path.join(self.folder_path, file) for file in self.get_files(self.folder_path)]
        for path in self.files_path[:10]:
            # Reading pdf
            if self.get_file_extension(path) == '.pdf':
                try:
                    reader = PdfReader(path)
                    text = ""
                    for page in reader.pages:
                        text = text + page.extract_text() + "\n"
                    self.text_dict[path] = text
                except:
                    print(f"Returned error when reading pdf: {path}")
            # Reading documents
            elif self.get_file_extension(path) == '.docx':
                try:
                    self.text_dict[path] = docx2txt.process(path)
                except:
                    print(f"Returned error when reading document: {path}")

            else:
                print(f"File format {self.get_file_extension(path)} not supported")

    def refresh_dict(self):
        self.text_dict = dict()
