# Guide to HelioCloud Tutorials
S. Antunes (APL)
March 10, 2026

HelioCloud is a cloud platform, an analysis cache of datasets, and an exploratory platform with tutorials to get researchers started. Our best introduction to 'why' is our [02b_AGU_Demo-Populated.ipynb](02b_AGU_Demo-Populated.ipynb) Notebook, which explains what HelioCloud can do and introduces a basic Python science example for looking at time-series data and at images.

There are many tutorials here and we'll help walk you through them. At this point we'll assume you're already in your account and able to run a Notebook.  We will walk through examples of data reads from AWS S3 storage, using Dask for compute power, using the core PyHC packages in Python, and working in IDL.  We also include a link to a local copy of the PyHC summer school package tutorials for SunPy, SpacePy, AstroPy, HAPI, and others.  Also advice for using GPUs to speed calculations. And the ability to ask AIs to help you with your code.

The core HelioCloud notebooks to date are:
1) A brief 'everything' tutorial including how to do all the below in brief, and a walkthrough of each core PyHC package, in [01_Testing_Notebook.ipynb](01_Testing_Notebook.ipynb)
2) More detailed intro in our AGU Demo notebook, available as [02b_AGU_Demo-Populated.ipynb](02b_AGU_Demo-Populated.ipynb) or in the run-it-yourself [02a_AGU_Demo-Base.ipynb)](02a_AGU_Demo-Bare.ipynb)
3) Using AWS S3 cloud storage, with basic file access of FITS, CDF and NetCDF data stored in S3, in [03_S3_Explained.ipynb](03_S3_Explained.ipynb)
4) 'bursting' a job onto multiple temporary CPUs using Dask in [04_Dask_Explained.ipynb](04_Dask_Explained.ipynb)
5) Use of CloudCatalog for finding and exploring datasets across all HelioClouds, in the [05_CloudCatalog_Demo.ipynb](05_CloudCatalog_Demo.ipynb)
6) An extended science example: searching for SDO data then processing a large set on multiple CPUs via Dask and gathering the results, in [06_SDO_Demo.ipynb](06_SDO_Demo.ipynb)

We start off with the 'Science in the Browser' approach where the Juptyer Notebook suffices to find, analyze and plot data entirely within the cloud.  We also include additional material for power users who prefer to work in their own cloud VM or cloud console environment.

We also have advice for our GPU-enabled machines:
8) Using a GPU and speed comparisons between CPU & GPU in [GPU-tutorials/CPU_vs_GPU_Speed_Test.ipynb](GPU-tutorials/CPU_vs_GPU_Speed_Test.ipynb)
9) Doing Dask bursts onto multiple GPUs, in [GPU-tutorials/GPU_Dask_Cluster_Demo.ipynb](GPU-tutorials/GPU_Dask_Cluster_Demo.ipynb)
10) GPUs for CME prediction, a science demo from the HelioML.org book, in
[GPU-tutorials/HelioML_GPU_Demo.ipynb](GPU-tutorials/HelioML_GPU_Demo.ipynb)

Ready to use AI to help you code? Follow our examples in
11) [Model_Testing.ipynb](Model_Testing.ipynb)
12) And setup help in [Using_Free_Google_API_Key.ipynb](Using_Free_Google_API_Key.ipynb) and [Save_JupyterAI_APIs.ipynb](Save_JupyterAI_APIs.ipynb)

## About HelioCloud, Notebooks, and Dask

HelioCloud is a software stack enabling you to do research in the Amazon Web Services (AWS) high performance cloud from within your browser or laptop terminal.

"Daskhub" is the name of the web-based Jupyter Notebook interface for most HelioCloud users, which enables running these notebooks.  'Dask' itself is a way to quickly parallelize your code by throwing it to multiple CPUs.  So Daskhub is a Notebook-based IDE that has access to dask 'burst' processing.

"Jupyter Notebooks" aka Notebooks are a way to write code and descriptive text in the same document.  Notebooks also store output, and can serve as a publication of both code, documentation and results.  The intent is that a Notebook that works in one HelioCloud will work in other HelioClouds.

If you are interested in how to write in Jupyter notebooks to make attractive presentation-ready pages, read the [Additional/OutputTypes notebook](Additional/OutputTypes.ipynb)


### First: What is S3 Cloud Storage?

S3 stands for "Simple Storage Service," which provides object storage for for AWS. https://aws.amazon.com/s3/

It allows people to query and access data from a common location reference. The buckets can be made web accessible to users outside of daskhub if web access is enabled. S3 buckets behave Objects are stored in buckets and addressed by key (a flat namespace). There are no true directories; “folders” are key prefixes. Conceptually, S3 behaves more like a network-attached tape library than a block device: high capacity, high durability, optimized for streaming access, and tolerant of latency.

HelioCloud has 1.5PB of data available in public S3 for you, including all of CDAWeb, much of the SPDF datasets, and various contributed datasets.

## Everything at Once

If you are already familiar with Python and PyHC, the  brief 'everything' tutorial in [01_Testing_Notebook.ipynb](01_Testing_Notebook.ipynb) will show you how to (briefly) do typical desktop science tasks, but in the cloud.

If you are new to everything, look at our short [02b_AGU_Demo-Populated.ipynb](02b_AGU_Demo-Populated.ipynb) tutorial or in the run-it-yourself [02a_AGU_Demo-Base.ipynb)](02a_AGU_Demo-Bare.ipynb)


## Science Part 1: Cloud storage and using multiple CPUs in Python

Python practice examples for reading sample data in FITS, CDF or NetCDF that are stored in this cloud is in our [03_S3_Explained notebook](03_S3_Explained.ipynb). These make use of AstroPy for FITS files, cdflib for CDF files, and Xarray for NetCDF files.

Dask is software that lets you 'burst' a job onto multiple temporary CPUs by defining then using a cluster of CPUs to lazily parallelize jobs. Using Dask in a notebook is in [04_Dask_Explained.ipynb](04_Dask_Explained.ipynb), showing both generic Dask usage and an actual SDO calculation example case.

## Science Part 2: Big Data Sets

Cloud means never having to download datasets. Instead, you find data across multiple HelioClouds and directly access it without downloading it locally.  The [CloudCatalog API](https://pypi.org/project/cloudcatalog/) on top of the CloudCatalog sharing standard enables finding and listing cloud-stored scientific datasets such as CDAWeb, SDO, MMS and others.

Our initial example for finding datasets and lists of data files within one more more HelioClouds is in the [05_CloudCatalog_Demo.ipynb](05_CloudCatalog_Demo.ipynb), using the MMS dataset.

We then add a big data task using Dask 'burst' capabilities to tackle 2TB of data rapidly.  Here we search for SDO data then processing a large set on multiple CPUs via Dask and gathering the results, in the [06_SDO_Demo notebook](06_SDO_Demo.ipynb)

## Using GPUs

If you are completely new to GPUs, we provide the [GPU-tutorials/CPU_vs_GPU_Speed_Test.ipynb](GPU-tutorials/CPU_vs_GPU_Speed_Test.ipynb) for use in our Tensorflow-equipped single GPU machines.

We show how you can do your work on a temporary cluster of GPUs, just as we did with a cluster of CPUs in our SDO demo. The GPU cluster is created using Dask, a tool that allows us to scale up our compute based on the size of the problem we want to solve.
The full demo is in [GPU-tutorials/GPU_Dask_Cluster_Demo.ipynb](GPU-tutorials/GPU_Dask_Cluster_Demo.ipynb).

We also rework a [https://helioml.org](HelioML.org) JupyterBook example using GPUs for CME prediction, in [GPU-tutorials/HelioML_GPU_Demo.ipynb](GPU-tutorials/HelioML_GPU_Demo.ipynb).

## AI via %jupyter-ai

Ready to use AI to help you code? Follow our examples in [Model_Testing.ipynb](Model_Testing.ipynb) to see how AI can help you understand, document, modify, and test code within a Jupyter Notebook cell.

Use of AI requires you have an account or keys for one of the many AI providers out there (OpenAI, Google, etc), and we provide setup help in [Using_Free_Google_API_Key.ipynb](Using_Free_Google_API_Key.ipynb) plus a tool for saving keys privately and securely in [Save_JupyterAI_APIs.ipynb](Save_JupyterAI_APIs.ipynb).

## Working with IDL

We provide an example for using IDL in the [IDL/IDL_examples notebook](IDL/IDL_examples.ipynb) and, additionally, accessing S3 in IDL in the [IDL/IDL-S3 notebook](IDL/IDL-S3.ipynb)

## Power users

Pushing data on or off S3 using SFTP is in [Setup/SFTP service notebook](Setup/SFTP service.ipynb)

A simple "hello world" in Fortran is in the [Additional/fortran_helloworld notebook](Additional/fortran_helloworld.ipynb)

An example of plotting a contributed dataset is shown in [Additional/EUVML_viewer](Additional/EUVML_viewer.ipynb)

Updating your personal Conda environment is in the [Setup/Conda_instructions_for_cloud notebook](Setup/Conda_instructions_for_cloud.ipynb)

A helper function for saving Portal-generated AWS keys into your local ~/.aws/credentials directory is in [Tools/Save_Credentials](Tools/Save_Credentials.ipynb)

Testing if GPUs are enabled, in the [Additional/GPU-Info notebook](Additional/GPU-Info.ipynb)

# Sample PyHC Tutorials

To get a feel for using a Notebook (whether in cloud or on your laptop), we provide an excerpt of tutorials from the PyHC 2022 Summer School.  This highlights using the standard packages, fetching data, and plotting where the cloud usage and laptop usage are identical.

1) [AstroPy_FITS-files-demo.ipynb](pyhc/AstroPy_FITS-files-demo.ipynb)
2) [HAPI_01.ipynb](pyhc/HAPI_01.ipynb) basics and
[HAPI_03.ipynb](pyhc/HAPI_03.ipynb) plotting
3) [Kamodo_04-Visualization.ipynb](pyhc/Kamodo_04-Visualization.ipynb)
4) [PlasmaPy-tutorial-instructor.ipynb](pyhc/PlasmaPy-tutorial-instructor.ipynb)
5) [PySPEDAS_Summer_School_2022.ipynb](pyhc/PySPEDAS_Summer_School_2022.ipynb)
6) [SolarMach_notebook.ipynb](pyhc/SolarMach_notebook.ipynb)
7) [SunPy_part-1-search-and-download_Instructor.ipynb](pyhc/SunPy_part-1-search-and-download_Instructor.ipynb), 
[SunPy_part-2-data-structures_Instructor.ipynb](pyhc/SunPy_part-2-data-structures_Instructor.ipynb) and
[SunPy_part-3-coordinates_Instructor.ipynb](pyhc/SunPy_part-3-coordinates_Instructor.ipynb)

## About HelioCloud

HelioCloud is cloud software for the Heliophysics research community.  HelioCloud is a time-saving tool for heliophysics researchers to rapidly access and analyze high-volume datasets from a web browser.  It includes easy-to-navigate cloud-based software with big data storage offers an innovative, streamlined approach for conducting research.  An Open Science framework breaks down barriers to collaboration by enabling multipoint access to shared data, code, and analysis tools in a secure environment.  You can download and install the software at your institution to connect with other HelioCloud communities and contribute to the project.  More at [https://heliocloud.org](https://heliocloud.org)
