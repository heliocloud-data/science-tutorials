# Guide to HelioCloud Tutorials
S. Antunes (APL)
December 2023

HelioCloud is a cloud platform, an analysis cache of datasets, and an exploratory platform with tutorials to get researchers started. Our best introduction to 'why' is our [AGU_Demo-Populated.ipynb](AGU_Demo-Populated.ipynb) Notebook, which explains what HelioCloud can do and introduces a basic Python science example for looking at time-series data and at images.

There are many tutorials here and we'll help walk you through them. At this point we'll assume you're already in your account and able to run a Notebook.  We will walk through examples of data reads from AWS S3 storage, using Dask for compute power, using the core PyHC packages in Python, and working in IDL.  We also include a link to a local copy of the PyHC summer school package tutorials for SunPy, SpacePy, AstroPy, HAPI, and others.

The core HelioCloud notebooks to date are:
1) Overall intro in [AGU_Demo-Populated.ipynb](AGU_Demo-Populated.ipynb)
2) basic file access of FITS, CDF and NetCDF data that is stored in AWS S3 cloud storage, in [S3-Access-Demo.ipynb](S3-Access-Demo.ipynb)
3) 'bursting' a job onto multiple temporary CPUs in [Dask-Gateway-Example.ipynb](Dask-Gateway-Example.ipynb)
4) combining accessing private or public S3 files with bursting via Dask in [S3-Dask-Demo.ipynb](S3-Dask-Demo.ipynb)
5) finding datasets and lists of data files within one more more HelioClouds, in the [CloudCatalog-Demo.ipynb](CloudCatalog-Demo.ipynb)
6) extended example MMS: searching for MMS data by instrument name and time range, then analyzing and plotting them, in [MMS-Catalog-Demo.ipynb](MMS-Catalog-Demo.ipynb)
7) extended example SDO: searching for SDO data then processing a large set on multiple CPUs via Dask and gathering the results, in [HelioCloud-SDO-Demo.ipynb](HelioCloud-SDO-Demo.ipynb)
8) a brief 'everything' tutorial including how to do all the above in brief, and a walkthrough of each core PyHC package, in [Testing_Notebook.ipynb](Testing_Notebook.ipynb)

We start off with the 'Science in the Browser' approach where the Juptyer Notebook suffices to find, analyze and plot data entirely within the cloud.  We also include additional material for power users who prefer to work in their own cloud VM or cloud console environment.

## About HelioCloud, Notebooks, and Dask

HelioCloud is a software stack enabling you to do research in the Amazon Web Services (AWS) high performance cloud from within your browser or laptop terminal.

"Daskhub" is the name of the web-based Jupyter Notebook interface for most HelioCloud users, which enables running these notebooks.  'Dask' itself is a way to quickly parallelize your code by throwing it to multiple CPUs.  So Daskhub is a Notebook-based IDE that has access to dask 'burst' processing.

"Jupyter Notebooks" aka Notebooks are a way to write code and descriptive text in the same document.  Notebooks also store output, and can serve as a publication of both code, documentation and results.  The intent is that a Notebook that works in one HelioCloud will work in other HelioClouds.

If you are interested in how to write in Jupyter notebooks to make attractive presentation-ready pages, read the [Additional/OutputTypes notebook](Additional/OutputTypes.ipynb)


### First: What is S3?

S3 stands for "Simple Storage Service," which provides object storage for for AWS. https://aws.amazon.com/s3/

It allows people to query and access data from a common location reference. The buckets can be made web accessible to users outside of daskhub if web access is enabled.

S3 buckets are individual storage elements.

## Everything at Once

If you are new to everything, look at our short [AGU_Demo-Populated.ipynb](AGU_Demo-Populated.ipynb) tutorial.

If you are already familiar with Python and PyHC, the  brief 'everything' tutorial in [Testing_Notebook.ipynb](Testing_Notebook.ipynb) will show you how to (briefly) do typical desktop science tasks, but in the cloud.

## Science Part 1: Cloud storage and using multiple CPUs in Python

Python practice examples for reading sample data in FITS, CDF or NetCDF that are stored in this cloud is in our [S3-Access-Demo notebook](S3-Access-Demo.ipynb). These make use of AstroPy for FITS files, cdflib for CDF files, and Xarray for NetCDF files.

Dask is software that lets you 'burst' a job onto multiple temporary CPUs by defining then using a cluster of CPUs to lazily parallelize jobs. Using Dask in a notebook is in [Dask-Gateway-Example notebook](Dask-Gateway-Example.ipynb)

We then combine reading from cloud S3 storage then using Dask to 'burst' the problem solving in [S3-Dask-Demo.ipynb](S3-Dask-Demo.ipynb)

## Science Part 2: Big Data Sets

Cloud means never having to download datasets. Instead, you find data across multiple HelioClouds and directly access it without downloading it locally.  The [CloudCatalog API](https://pypi.org/project/cloudcatalog/) on top of the CloudCatalog sharing standard enables finding and listing cloud-stored scientific datasets such as CDAWeb, SDO, MMS and others.

Our initial example for finding datasets and lists of data files within one more more HelioClouds is in the [CloudCatalog-Demo.ipynb](CloudCatalog-Demo.ipynb)

## Science Part 3: Using real MMS and SDO data

We present two sample tasks wherein we first query the cloud for instrument data. We then pull a list of files for a given instrument and time range, then process it, all within the cloud (not using your local storage or laptop CPU).

A serial example is searching for MMS data by instrument name and time range, then analyzing and plotting them, in the [MMS-Catalog-Demo notebook](MMS-Catalog-Demo.ipynb)

We then add Dask 'burst' capabilities to tackle 2TB of data rapidly.  Here we search for SDO data then processing a large set on multiple CPUs via Dask and gathering the results, in the [HelioCloud-SDO-Demo notebook](HelioCloud-SDO-Demo.ipynb)

## Working with IDL

We provide an example for using IDL in the [IDL/IDL_examples notebook](IDL/IDL_examples.ipynb) and, additionally, accessing S3 in IDL in the [IDL/IDL-S3 notebook](IDL/IDL-S3.ipynb)

## Power users

Pushing data on or off S3 using SFTP is in [Setup/SFTP service notebook](Setup/SFTP service.ipynb)

A simple "hello world" in Fortran is in the [Additional/fortran_helloworld notebook](Additional/fortran_helloworld.ipynb)

Updating your personal Conda environment is in the [Setup/Conda_instructions_for_cloud notebook](Setup/Conda_instructions_for_cloud.ipynb)

Testing if GPUs are enabled, in the[Additional/GPU-Info notebook](Additonal/GPU-Info.ipynb)
