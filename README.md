# Reading-from-Delphes
 Simple pyroot scripts to read from delphes output and produce simple histogra,ms

## How to use 
To get info on how to run open terminal and write 

```
python PlotFromRoot.py -h
```

Example 
```
 PlotFromRoot.py --signal_file uC_ww_leplep_sqrts01000_mw80419.root --background_file uC_ww_leplep_sqrts01000_mw80419.root
```
** In the example above the same file is provided as signal and bg-- need to change**

It works with signal samples provided [here](https://bilpa.docs.cern.ch/projects/wmass/samples/)

