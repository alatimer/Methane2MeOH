# Methane2MeOH

This repo contains the scripts and data files used to generate
work in publication: https://doi.org/10.1021/acscatal.8b00220.  

If you use this work in your research, please consider citing:

Latimer, A. A.; Kakekhani, A.; Kulkarni, A. R.; Nørskov, J. K. Direct Methane to Methanol : The Selectivity − Conversion Limit and Design Strategies. 2018.

An interactive version of figure 5 can be found at: https://plot.ly/~alatimer/7

## Abstract:
Currently, methane is transformed into methanol through the two-step syngas process which requires high temperatures and centralized production.  While the slightly exothermic direct partial oxidation of methane to methanol would be preferable, no such process has been established despite over a century of research.  Generally, this failure has been attributed to the high barriers required to activate methane, as well as the higher activity of the CH bonds in methanol.  However, a precise and general ab initio quantification of the limitations of catalytic direct methane to methanol has yet to be established.  Herein, we derive from first principles a simple model that successfully captures the selectivity-conversion behavior of much of the catalytic methane to methanol experimental literature.  Stemming from this analysis, we suggest several potential strategies for increasing methanol yields.  These include employing  “collectors,” high surface-area materials with strong methanol adsorption potential which can help to lower the partial pressure of methanol in the gas phase, aqueous reaction conditions, and/or diffusion-limited systems.  By successfully rationalizing a significant number of experimental studies from the diverse fields of heterogeneous, homogeneous, biological and gas-phase catalysis within a single model, we underscore the idea that continuous methane to methanol is generally limited, and provide a framework for understanding and evaluating new processes.

## Dependencies: 

Python 2.7.8

ASE 3.12.0 (see https://wiki.fysik.dtu.dk/ase/ )

Numpy 1.9.0

Scipy 0.14.0

Matplotlib 1.4.0

## Usage:

All scripts used to generate figures in the manuscript are provided here as fig-X-Y.py where X is the figure number and Y is a brief description of the figure.
These can be run as is (python fig-X-Y.py) to generate the same figures seen in the manuscript.  They pull data from expobj.pkl and dftpbj.pkl .

Atoms objects and other attributes related to the DFT calculations performed in this work are available as a "dftclass" object in the pickle file "dftobj.pkl".
The previously published experimental data analyzed in this work is provided in a tab-separated file exp.dat that includes DOI numbers for each paper.  All 
relevant atomic structures can be found in the structures subfolder.

collectExp.py and collectDFT.py were used to scrape data and output the experimental and DFT data used in the analysis in dftobj.pkl and expobj.pkl.  collectDFT.py
should not be re-run.  collectExp.py can be re-run if changes are made to exp.dat (ie if a new data point is added in the specified format).  Running this script
will output a new expobj.pkl file.

