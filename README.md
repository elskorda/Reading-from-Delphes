# Reading-from-Delphes
Simple pyroot scripts to read from Delphes output and produce simple histograms.

## Installation

How to download and install this package on the B'ham PP cluster.

```shell
git clone https://github.com/elskorda/Reading-from-Delphes.git
cd Reading-from-Delphes
pipenv install --site-packages .
```

Create a local configuration file and edit it to include the path to your aMC@NLO with Delphes installed.
```shell
cp analysis.yaml.example .analysis.yaml
vim .analysis.yaml
```

## How to use
Run the following inside the `Reading-from-Delphes` directory.

```
python PlotFromRoot.py example.yaml
```

It works with signal samples provided [here](https://bilpa.docs.cern.ch/projects/wmass/samples/).

