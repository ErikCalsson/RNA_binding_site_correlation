# RNA_binding_site_correlation

## Core part: Binding site correlation python tool
The scope of this project is to write a small tool to analyze the overlap between two BED files (BED6, i.e. tab separated CHROM, START, END, NAME, SCORE, STRAND) and return a statistic whether both files are dissimilar and how significant this dissimilarity is.


### Input

Two BED6 formatted files.
One FA formatted file

### Output

Statisticts about the overlap of the BED files.


# Installation instructions

Download the current version:
```
git clone https://github.com/ErikCalsson/RNA_binding_site_correlation.git
```

Install requirements via pip3:
```
pip3 install -r requirements.txt
```
