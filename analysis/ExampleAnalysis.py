import ROOT
from analysis import Analysis

class ExampleHistograms(Analysis.Histograms):
    def create_histograms(self):
        self.hist_muon0Pt=ROOT.TH1F("muon0_pt", f'{self.title};leading muon p_{{T}} [GeV];a.u.', 50, 0, 5000)
        self.hist_muon1Pt=ROOT.TH1F("muon1_pt", f'{self.title};subleading muon p_{{T}} [GeV];a.u.', 50, 0, 5000)

        self.hist_dimuonPt=ROOT.TH1F("dimuon_pt", f'{self.title};di-muon p_{{T}} [GeV];a.u.', 50, 0, 5000)

    def fill_histograms(self, sample):
        self.hist_muon0Pt.Fill(sample.Muon[0].PT)
        self.hist_muon1Pt.Fill(sample.Muon[1].PT)

        # Add muons using pT
        dimuon=sample.Muon[0].P4()+sample.Muon[1].P4()
        self.hist_dimuonPt.Fill(dimuon.Pt())

class ExampleAnalysis(Analysis.Analysis):
    """
    An example analysis that plots the pT of the leading muon.
    """
    def __init__(self):
        super(ExampleAnalysis, self).__init__(ExampleHistograms)

    def selection(self, sample):
        if sample.Muon.GetEntries()<2:
            return False
        return True
