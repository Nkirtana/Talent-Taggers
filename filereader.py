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

    def __init__(self, input_path):
        self.files_path = list()
        self.text_dict = dict()
        if os.path.exists(input_path):
            self.input_path = input_path
        else:
            raise ValueError("Path not found!!")

    # list all the files present in a folder
    @staticmethod
    def get_files(filepath):
        return os.listdir(filepath)

    # Get file extension
    @staticmethod
    def get_file_extension(filepath):
        return os.path.splitext(filepath)[-1].lower()

    def read_pdf(self, pdf_path):
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text = text + page.extract_text() + "\n"
        self.text_dict[pdf_path] = text

    def read_doc(self, doc_path):
        text = docx2txt.process(doc_path)
        self.text_dict[doc_path] = text

    # Read all the resumes from a given folder and return list of text from resumes
    def read_resumes(self):

        # Check if input path is file
        if os.path.isfile(self.input_path):
            if self.get_file_extension(self.input_path) == '.pdf':
                self.read_pdf(self.input_path)

            elif self.get_file_extension(self.input_path) == '.docx':
                self.read_doc(self.input_path)

            else:
                print(f"File format {self.get_file_extension(self.input_path)} not supported")

        # Check if input path is directory
        elif os.path.isdir(self.input_path):
            self.files_path = list()
            self.files_path = [os.path.join(self.input_path, file) for file in self.get_files(self.input_path)]
            for path in self.files_path[:10]:
                # Reading pdf
                if self.get_file_extension(path) == '.pdf':
                    try:
                        self.read_pdf(path)
                    except:
                        print(f"Returned error when reading pdf: {path}")
                # Reading documents
                elif self.get_file_extension(path) == '.docx':
                    try:
                        self.read_doc(path)
                    except:
                        print(f"Returned error when reading document: {path}")

                else:
                    print(f"File format {self.get_file_extension(path)} not supported")

    def refresh_dict(self):
        self.text_dict = dict()
