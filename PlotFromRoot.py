import ROOT
import argparse

from analysis import Sample
from analysis import ExampleAnalysis
           
def plot_and_save(*args):
    """
    Creates a THStack to overlay the histograms inside `*args, draws the
    stack on a canvas, and saves the plot as a PNG file.
    """

    #
    # Get a list of histograms

    hnames=filter(lambda key: key.startswith('hist'), dir(args[0]))
    
    for hname in hnames:
        print(f'Plotting {hname}')
        # Create a canvas
        canvas = ROOT.TCanvas()

        # Create THStack
        stack = ROOT.THStack(f"hs_{hname}", '')

        exhist=getattr(args[0],hname)

        # Set histogram colors and add them to the stack
        colors=[ROOT.kBlue, ROOT.kRed]
        for histobj in args:
            hist=getattr(histobj, hname)
            hist.SetLineColor(colors.pop())
    
            stack.Add(hist)

        # Draw stack
        stack.Draw("nostack")
        stack.GetXaxis().SetTitle(exhist.GetXaxis().GetTitle())
        stack.GetYaxis().SetTitle(exhist.GetYaxis().GetTitle())
        canvas.BuildLegend()

        # Save the canvas as a PNG file
        canvas.SaveAs(f'{hname}.png')

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

    analysis=ExampleAnalysis.ExampleAnalysis()

    sig_hists=analysis.run(signal)
    bkg_hists=analysis.run(background)

    plot_and_save(sig_hists, bkg_hists)

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
