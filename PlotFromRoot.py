import ROOT
import argparse

from analysis import Sample

def event_loop(sample):
    """
    This fuction loops through events inside a sample, applies a basic selection
    and fills histograms.
    """
        
    # Define histograms
    muon0_pt = ROOT.TH1F("muon0_pt", sample.title, 50, 0, 2000)

    # Fill histograms 
    for idx in range(sample.reader.GetEntries()):
        sample.reader.ReadEntry(idx)

        #
        # Apply a selection
        #

        # Keep only events with a muon
        if sample.Muon.GetEntries() == 0:
            continue

        muon0_pt.Fill(sample.Muon[0].PT)

    # Done!
    return muon0_pt
            
def plot_and_save(signal_hist, background_hist, title, x_label, y_label, output_png_file):
    """
    Creates a THStack to overlay the signal and background histograms, draws the 
    stack on a canvas, and saves the plot as a PNG file.
    """
    # Create a canvas
    canvas = ROOT.TCanvas("canvas", title, 800, 600)

    # Create THStack
    stack = ROOT.THStack("stack", title)

    # Set histogram colors
    signal_hist.SetLineColor(ROOT.kRed)
    background_hist.SetLineColor(ROOT.kBlue)
    
    stack.Add(signal_hist)
    stack.Add(background_hist)

    # Draw stack
    stack.Draw("nostack")
    stack.GetXaxis().SetTitle(x_label)
    stack.GetYaxis().SetTitle(y_label)
    canvas.BuildLegend()

    # Save the canvas as a PNG file
    canvas.SaveAs(output_png_file)

def main(signal_file, background_file):
    """
    Main function to read tree contents, create distributions, and plot/save 
    the histograms.
    """

    signal=Sample.Sample('Signal')
    signal.add_file(signal_file)
    signal.open()

    background=Sample.Sample('Background')
    background.add_file(background_file)
    background.open()

    signal_hist=event_loop(signal)
    background_hist=event_loop(background)

    plot_and_save(signal_hist, background_hist, '', 'leading muon p_{T} [GeV]', 'a.u.', 'MuonPT.png')
    
    # Create and plot distributions
    #create_and_plot_distributions(signal_file, background_file)

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="script that reads root files to create and plot distributions.")
    parser.add_argument("--signal_file",default="uC_ww_leplep_sqrts01000_mw80419.root", type=str, help="Path to the signal ROOT file.")
    parser.add_argument("--background_file", default="uC_ww_leplep_sqrts01000_mw80419.root", type=str, help="Path to the background ROOT file.")

    mg5amcnlo = '/home/kkrizka/Sources/mg5amcnlo'

    ROOT.gInterpreter.AddIncludePath(f"{mg5amcnlo}/Delphes");
    ROOT.gInterpreter.AddIncludePath(f"{mg5amcnlo}/Delphes/external");

    ROOT.gSystem.Load(f'{mg5amcnlo}/Delphes/libDelphes.so')
    
    # Parse the arguments
    args = parser.parse_args()

    # Execute the main function with the provided arguments
    main(args.signal_file, args.background_file)
