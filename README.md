# superSci
Superconductors and Scientific embeddings 

### Getting started 

Create a new virtual environment
> conda create -n superSci
> conda activate superSci

Install requirements, models and packages
> conda install --file requirements.txt

> python -m spacy download en_core_web_sm

Then install the package lxml (in CENTOS is called `python-lxml`). 

Missing lxml package error: 
```
Traceback (most recent call last):
  File "jats2text.py", line 67, in <module>
    soup = BeautifulSoup(f, 'lxml')
  File "/home/Luca/.conda/envs/superSci/lib/python3.7/site-packages/bs4/__init__.py", line 196, in __init__
    % ",".join(features))
bs4.FeatureNotFound: Couldn't find a tree builder with the features you requested: lxml. Do you need to install a parser library?
```
