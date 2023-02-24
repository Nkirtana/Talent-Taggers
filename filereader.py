import docx2txt
import pdftotext
import os


# Input folder where the resumes are present to read all the resumes in the folder
# It can detect extensions and read resumes based on extension.
class ReadFiles:

    def __init__(self, folder_path):
        self.files_path = list()
        self.text = dict()
        if os.path.exists(folder_path):
            self.folder_path = folder_path
        else:
            raise ValueError("Path not found!!")

    @staticmethod
    def get_files(filepath):
        return os.listdir(filepath)

    @staticmethod
    def get_file_extension(filepath):
        return os.path.splitext(filepath)[-1]

    def read_resumes(self):
        self.files_path = [os.path.join(self.folder_path, file) for file in self.get_files(self.folder_path)]
        for path in self.files_path[:10]:
            if self.get_file_extension(path) == '.pdf':
                # write code to read pdf
                pass
            elif self.get_file_extension(path) == '.docx':
                # write code to read docx
                self.text[path] = docx2txt.process(path)
                pass
            else:
                print(f"File format {self.get_file_extension(path)} not supported")


rf = ReadFiles(r"C:\Users\manoj\Desktop\projectresumes\word")
rf.read_resumes()
print(rf.text)
print(len(rf.text))

# C:\Users\manoj\Desktop\projectresumes\pdf
# C:\Users\manoj\Desktop\projectresumes\word

