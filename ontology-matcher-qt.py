import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QLabel, QPushButton, QMessageBox, QInputDialog, QCheckBox, QLineEdit
from PyQt5.QtGui import QDoubleValidator
from ontCompare import alignGraphs, writeGraph




class RDFCompare(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 900, 600)
        self.setWindowTitle("Alignement d'ontologies RDF")

        self.measures ={'jaro':0, 'jaro-winkler':0, 'levenshtein':0, 'string-equality':0}

        self.file1_label = QLabel('Fichier 1:', self)
        self.file1_label.move(350, 70)
        self.file1_label.resize(200,20)

        self.file1_button = QPushButton('Choisissez Fichier 1', self)
        self.file1_button.move(350, 100)
        self.file1_button.clicked.connect(self.select_file1)

        self.file2_label = QLabel('Fichier 2:', self)
        self.file2_label.move(350, 150)
        self.file2_label.resize(200,20)

        self.file2_button = QPushButton('Choisissez Fichier 2', self)
        self.file2_button.move(350, 180)
        self.file2_button.clicked.connect(self.select_file2)


        self.properties_label = QLabel(self)
        self.properties_label.setText('Propriétés (séparées par des virgules) :')
        self.properties_label.move(100, 230)
        self.properties_input = QLineEdit(self)
        self.properties_input.move(430, 230)
        self.properties_input.resize(350, 32)


        self.checkBox_jaro = QCheckBox(self)
        self.checkBox_jaro.move(150, 270)
        self.checkBox_jaro.setText("Jaro")
        self.checkBox_jaro.stateChanged.connect((lambda c: self.checked_measure(c, 'jaro')))


        self.checkBox_jw = QCheckBox(self)
        self.checkBox_jw.move(150, 300)
        self.checkBox_jw.setText("Jaro-Winkler")
        self.checkBox_jw.stateChanged.connect((lambda c: self.checked_measure(c, 'jaro-winkler')))

        self.checkBox_lev = QCheckBox(self)
        self.checkBox_lev.move(150, 330)
        self.checkBox_lev.setText("Levenshtein")
        self.checkBox_lev.stateChanged.connect((lambda c: self.checked_measure(c, 'levenshtein')))

        self.checkBox_seq = QCheckBox(self)
        self.checkBox_seq.move(150, 360)
        self.checkBox_seq.setText("String Equality")
        self.checkBox_seq.stateChanged.connect((lambda c: self.checked_measure(c, 'string-equality')))

        self.checkBox_ueq = QCheckBox(self)
        self.checkBox_ueq.move(400, 270)
        self.checkBox_ueq.setText("URI Equality")
        self.checkBox_ueq.stateChanged.connect((lambda c: self.checked_measure(c, 'uri-equality')))

        self.checkBox_2g = QCheckBox(self)
        self.checkBox_2g.move(400, 300)
        self.checkBox_2g.setText("2-Grams")
        self.checkBox_2g.stateChanged.connect((lambda c: self.checked_measure(c, '2-gram')))

        self.checkBox_3g = QCheckBox(self)
        self.checkBox_3g.move(400, 330)
        self.checkBox_3g.setText("3-Grams")
        self.checkBox_3g.stateChanged.connect((lambda c: self.checked_measure(c, '3-gram')))

        self.threshold_label = QLabel(self)
        self.threshold_label.setText('Seuil de similarité :')
        self.threshold_label.move(250, 400)
        self.threshold_input = QLineEdit(self)
        self.threshold_input.setValidator(QDoubleValidator(0.0,1.0,10))
        self.threshold_input.move(430, 400)


        self.compare_button = QPushButton('Comparer', self)
        self.compare_button.move(400, 500)
        self.compare_button.clicked.connect(self.compare_files)


        self.show()

    def select_file1(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file1, _ = QFileDialog.getOpenFileName(
            self, "Select File 1", "", "RDF Files (*.rdf *.ttl)", options=options)
        self.file1_label.setText('File 1: ' + os.path.basename(file1))
        self.source_file = file1

    def select_file2(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file2, _ = QFileDialog.getOpenFileName(
            self, "Select File 2", "", "RDF Files (*.rdf *.ttl)", options=options)
        self.file2_label.setText('File 2: ' + os.path.basename(file2))
        self.target_file = file2

    
    def checked_measure(self, checked, measure):
        if checked:
            self.measures[measure] = 1
        else:
            self.measures[measure] = 0
        self.show()



    def saveAs(self, alignment):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, 
            "Save File", "", "All Files(*);;Text Files(*.txt)", options = options)
        if fileName:
            writeGraph(alignment, fileName)

   
    def compare_files(self):
        if not hasattr(self, 'source_file') or not hasattr(self, 'target_file'):
            QMessageBox.warning(self, "Warning", "Please select two RDF files to compare.")
            return

        # user input 
        propertiesString = self.properties_input.text()
        threshold = float(self.threshold_input.text())

        properties = [prop.strip() for prop in propertiesString.split(',')]
        similarities = [measure for measure, v in self.measures.items() if v == 1]

        print(properties)
        print(similarities)
        print(threshold)

        
        if len(properties) < 1:
            QMessageBox.warning(self, "Warning", "Please choose at least one property")
            return

        if len(similarities) < 1:
            QMessageBox.warning(self, "Warning", "Please choose at least one similarity measure")
            return


        prop_sim_dict = {}

        for prop in properties:
            prop_sim_dict[prop] = similarities

        alignment = alignGraphs(self.source_file, self.target_file, prop_sim_dict, threshold)

        self.saveAs(alignment)
        #writeGraph(alignment, outputFile)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = RDFCompare()
    sys.exit(app.exec_())