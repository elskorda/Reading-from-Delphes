import ROOT

class Histograms:
    def __init__(self, title, style):
        self.title = title
        self.style = style

    def create_histograms(self):
        """
        OVERLOAD THIS FUNCTION

        Create new histogram classes and add them as member objects. Any
        object that starts with `hist_` will be later plotted.

        This function in called only at the start.
        """
        pass

    def fill_histograms(self, sample):
        """
        OVERLOAD THIS FUNCTION

        Fill histograms with the currently loaded event inside the `sample`.

        This function in called for each event.

            Parameters
        ----------
        sample : Analysis.Sample
            A sample object with the currently loaded event.
        """
        pass

class Analysis:
    def __init__(self, histogrammer):
        self.histogrammer = histogrammer

    def selection(self, sample):
        """
        OPTIONALLY OVERLOAD THIS FUNCTION

        Decide if an event passes your selection. The event under question
        is the currently loaded entry inside `sample`.

        This function in called for each event.

        Parameters
        ----------
        sample : Analysis.Sample
            A sample object with the currently loaded event.

        Returns
        -------
        bool
            True if the currently loaded event passes the selection.
        """
        return True

    def run(self, sample):
        """
        Runs the analysis.
        """
        histograms = self.histogrammer(sample.title, sample.style)
        histograms.create_histograms()

        for idx in range(sample.reader.GetEntries()):
            sample.reader.ReadEntry(idx)

            if not self.selection(sample):
                continue

            histograms.fill_histograms(sample)

        # Normalize all histograms to unity
        for attrname in dir(histograms):
            attr=getattr(histograms, attrname)
            if not isinstance(attr,ROOT.TH1):
                continue # not a histogram
            attr.Scale(1./sample.reader.GetEntries())

        return histograms
