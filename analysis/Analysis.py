class Analysis:
    def __init__(self, sample):
        self.sample = sample

    def create_histograms(self):
        """
        OVERLOAD THIS FUNCTION

        Create new histogram classes and add them as member objects. Any
        object that starts with `hist_` will be later plotted.

        This function in called only at the start.
        """
        pass

    def selection(self):
        """
        OPTIONALLY OVERLOAD THIS FUNCTION

        Decide if an event passes your selection. The event under question
        is the currently loaded entry inside `sample`.

        This function in called for each event.

        Returns
        -------
        bool
            True if the currently loaded event passes the selection.
        """
        return True

    def fill_histograms(self):
        """
        OVERLOAD THIS FUNCTION

        Fill histograms with the currently loaded event inside the `sample`.

        This function in called for each event.
        """
        pass

    def run(self):
        """
        Runs the analysis.
        """
        self.create_histograms()

        for idx in range(self.sample.reader.GetEntries()):
            self.sample.reader.ReadEntry(idx)

            if not self.selection():
                continue

            self.fill_histograms()
