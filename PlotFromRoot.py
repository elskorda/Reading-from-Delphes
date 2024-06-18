import ROOT
from contextlib import redirect_stdout
from itertools import combinations
import argparse

def read_tree_and_print_contents(root_file):
    """
    Opens the signal and background ROOT files, retrieves the 'Delphes' tree,
    prints the tree structure.
    You need to change the name of the tree, to the name of your tree
    explanation of output https://cp3.irmp.ucl.ac.be/projects/delphes/wiki/WorkBook/RootTreeDescription
    """
    # Open the signal and background files
    root_f = ROOT.TFile(root_file)

    # Get the tree from the file
    # ----> change the name here
    root_tree = root_f.Get("Delphes")
    
    root_tree.Print()
        
    # Close the files
    root_f.Close()

    

def create_and_plot_distributions(signal_file, background_file):
    """
    This fuction loops through events in the signal and background trees,
    and fills histograms then plots and saves the histograms.
    """
    # Open the signal and background files
    signal_f = ROOT.TFile(signal_file)
    background_f = ROOT.TFile(background_file)

    # Get the tree from both files
    # ----> change the name here if needed
    signal_tree = signal_f.Get("Delphes")
    background_tree = background_f.Get("Delphes")
        
    # Define histograms
    signal_hist = ROOT.TH1F("signal_hist", "Muon P_{T} Signal", 50, 0, 200)
    background_hist = ROOT.TH1F("background_hist", "Muon  P_{T} Background", 50, 0, 200)

    # Fill histograms 
    for event in signal_tree:
        muon_pt = event.GetLeaf("Muon.PT").GetValue()
        if (muon_pt):
            signal_hist.Fill(muon_pt)

    for event in background_tree:
        muon_pt = event.GetLeaf("Muon.PT").GetValue()
        if(muon_pt):
            background_hist.Fill(muon_pt)
        
    plot_and_save_histograms(signal_hist, background_hist,
                             title="p_{T} distribution of muons",
                             x_label="p_{T} (GeV)",
                             y_label="Number of Events",
                             output_png_file="MuonPT.png")


            
def plot_and_save_histograms(signal_hist, background_hist, title, x_label, y_label, output_png_file):
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
    signal_hist.SetFillColor(ROOT.kRed)
    background_hist.SetLineColor(ROOT.kBlue)
    background_hist.SetFillColor(ROOT.kBlue)

    
    stack.Add(signal_hist)
    stack.Add(background_hist)

    # Draw stack
    stack.Draw()
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
    # Read tree and print contents
    #read_tree_and_print_contents(signal_file)

    # Create and plot distributions
    create_and_plot_distributions(signal_file, background_file)

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="script that reads root files to create and plot distributions.")
    parser.add_argument("--signal_file",default="uC_ww_leplep_sqrts01000_mw80419.root", type=str, help="Path to the signal ROOT file.")
    parser.add_argument("--background_file", default="uC_ww_leplep_sqrts01000_mw80419.root", type=str, help="Path to the background ROOT file.")
    
    
    # Parse the arguments
    args = parser.parse_args()

    # Execute the main function with the provided arguments
    main(args.signal_file, args.background_file)
