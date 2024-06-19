import ROOT
from analysis import Analysis

class ExampleHistograms(Analysis.Histograms):
    def create_histograms(self):
        self.hist_muon0Pt=ROOT.TH1F("muon0_pt", self.title, 50, 0, 5000)

    def fill_histograms(self, sample):
        self.hist_muon0Pt.Fill(sample.Muon[0].PT)

class ExampleAnalysis(Analysis.Analysis):
    """
    An example analysis that plots the pT of the leading muon.
    """
    def __init__(self):
        super(ExampleAnalysis, self).__init__(ExampleHistograms)

    def selection(self, sample):
        if sample.Muon.GetEntries()==0:
            return False
        return True
