import ROOT
import argparse

from analysis import config
from analysis import Sample
from analysis import ExampleAnalysis

from kkconfig import runconfig

from kkroot import style

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

        # Create and style the histogram
        for histobj in args:
            hist=getattr(histobj, hname)
            style.style(hist,**histobj.style)

            stack.Add(hist)

        # Draw stack
        stack.Draw("nostack")
        stack.GetXaxis().SetTitle(exhist.GetXaxis().GetTitle())
        stack.GetYaxis().SetTitle(exhist.GetYaxis().GetTitle())
        canvas.BuildLegend()

        # Save the canvas as a PNG file
        canvas.SaveAs(f'{hname}.png')

def main(runconfig_path):
    """
    Main function to read tree contents, create distributions, and plot/save 
    the histograms.
    """

    runcfg=runconfig.load([runconfig_path])

    samples=[]
    for input in runcfg.get('inputs',[]):

        sample=Sample.Sample(input.get('title',''))

        path=input.get('path',[])
        if type(path) is not list:
            path=[path]

        for p in path:
            sample.add_file(p)
        sample.style=input.get('style', {})
        sample.open()

        samples.append(sample)

    analysis=ExampleAnalysis.ExampleAnalysis()

    hists=map(analysis.run, samples)

    plot_and_save(*list(hists))

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="script that reads root files to create and plot distributions.")
    parser.add_argument("runconfig", type=str, help="Path to the run configuration YAML file.")

    ROOT.gInterpreter.AddIncludePath(f"{config.mg5amcnlo}/Delphes");
    ROOT.gInterpreter.AddIncludePath(f"{config.mg5amcnlo}/Delphes/external");

    ROOT.gSystem.Load(f'{config.mg5amcnlo}/Delphes/libDelphes.so')
    
    # Parse the arguments
    args = parser.parse_args()

    # Execute the main function with the provided arguments
    main(args.runconfig)
