import ROOT

class Sample:
    def __init__(self, title=''):
        self.title = title
        self.files = []

        self.reader=None

        self.Muon=None

    def add_file(self, path):
        self.files.append(path)

    def open(self):
        # Open the sample and make a reader
        chain = ROOT.TChain("Delphes")
        for path in self.files:
            chain.Add(path)

        # Create object of class ExRootTreeReader
        self.reader = ROOT.ExRootTreeReader(chain)

        # Get pointers to branches used in this analysis
        self.Muon = self.reader.UseBranch("Muon")
