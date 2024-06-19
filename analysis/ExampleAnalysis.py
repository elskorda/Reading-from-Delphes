import ROOT
from analysis import Analysis

class ExampleAnalysis(Analysis.Analysis):
    """
    An example analysis that plots the pT of the leading muon.
    """
    def create_histograms(self):
        self.hist_muon0Pt=ROOT.TH1F("muon0_pt", self.sample.title, 50, 0, 5000)

    def selection(self):
        if self.sample.Muon.GetEntries()==0:
            return False
        return True

    def fill_histograms(self):
        self.hist_muon0Pt.Fill(self.sample.Muon[0].PT)
