import sys
import subprocess
import ntpath
"""
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, \
    QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon
"""

from PySide2.QtWidgets import QApplication, QWidget, QInputDialog, \
    QLineEdit, QFileDialog
from PySide2.QtGui import QIcon


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 file dialogs - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()

    def saveFileDialog(self, window_title):
        options = QFileDialog.Options()
        (fileName, _) = QFileDialog.getSaveFileName(
            self, window_title, '', 'MP4 File (*.mp4)', options=options)
        if fileName:
            print(fileName)
            return fileName


    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        image_filename = self.openFileNameDialog('Choose Image Filename',
                                                 '(*.jpg *.jpeg *.png)')
        if image_filename is None:
            sys.exit()
            return
        """
        audio_filename = self.openFileNameDialog('Choose Audio Filename',
                                                '(*.mp3 *.wav)')
        """

        audio_filenames = self.openFileNamesDialog()

        if audio_filenames is None:
            sys.exit()
            return

        #save_file_destination = self.saveFileDialog('Name to save the file as')

        save_file_destination =  self.getExistingDirectory('Select folder')
        if save_file_destination is None:
            sys.exit()
            return

        self.close()
        self.fffmpeg_run(image_filename,
                         audio_filenames,
                         save_file_destination)
        sys.exit()

    def getExistingDirectory(self, window_title):
        options = QFileDialog.Options()
        directory_name = QFileDialog.getExistingDirectory(self, window_title, '/home', options=options)
        if directory_name:
            print(directory_name)
            return directory_name

    def openFileNameDialog(self, window_title, file_type):
        options = QFileDialog.Options()

        (fileName, _) = QFileDialog.getOpenFileName(
            self, window_title, '', file_type, options=options)
        if fileName:
            return fileName

    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        (files, _) = QFileDialog.getOpenFileNames(
            self,
            'QFileDialog.getOpenFileNames()', '',
            '(*.mp3 *.wav)', options=options)
        if files:
            print(files)
            return files

    def fffmpeg_run(self, image_filename, audio_filenames,
                    save_file_destination):
        for audio_file in audio_filenames:

            completed = subprocess.run("./fffmpeg -loop 1 -i " + '"'
                                       + image_filename + '"' + " -i " + '"'
                                       + audio_file + '"' + " -c:v libx264"
                                       + " -tune stillimage -c:a aac -b:a 192k"
                                       + " -pix_fmt yuv420p -shortest "
                                       + '"' + save_file_destination + "/"
                                       + ntpath.basename(audio_file).split('.')[0] + ".mp4" + '"', shell=True)
            self.show()
            print('returncode:', completed.returncode)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
