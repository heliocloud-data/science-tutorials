# Sample Use Cases

Tackling the 'who will use HelioCloud' and 'why use HelioCloud' through likeliest use cases. By targeting known or likely use cases, we can avoid the 'design for everything' to focus on the core abilities we should finalize first.

## Science Use Cases

Themes: Access & Findability, Machine Learning, Big Data, Sharing Data & Code, Performance & HPC

Access & Findability:
* Quick look plots of events for multiple missions (general, WHPI)
* Fit of 2-years of coronagraph data to make a 3D F-corona model (fitting)
* Postdoc wants data but has no knowledge (nor interest) of pipelines
* Visual selection of events/3D panning (HEKB, WHPI)
* Prototyped on 1 month of data and now wants to run on full solar cycle (dev/ops)
* Found/defined event, wants to find others in dataset

Machine Learning
* Found/defined event, wants to find others in dataset
* Running algorithms on data (e.g. MMS), preprocessing to L3, standardizing and scaling
* Testing different ML algorithms, playground
* Flare detection
* ML algorithm updating automatically as new data arrives

Big Data
* Data too big otherwise (Supermag 1 sec data, SDO's PB of size per mission)
* 5TB MHD run outputs unshareable (also, GAMERA)
* Data assimilation (model+reality)
* Hyperspectral imageray (e.g. planetary, SDO images)
* 'Anyone can run my model' (e.g. MHD, IDA4D)

Sharing
* 'Anyone can run my model' (e.g. MHD, IDA4D)
* Storing processed data or analysis outputs, L3/L4 datasets

Performance
* Cloud is faster for existing work and IDE is easy to use
* Code sharing (likely just use Git)
* 'Use cloud not post-docs'

## IT Use Cases

* Everyone is on GSFC HelioCloud (paid by NASA)
* Everyone is on GSFC HelioCloud (paid by self)
* Starting or occasional users on GSFC HelioCloud; heavy users on clone of HelioCloud using own/institute AWS
* PanGeo model: we provide how to ramp up a cloud, users do so however they want

Intro: use GSFC HelioCloud or Your Institute HelioCloud, with IAM lists to allow S3 sharing.  Git as Notebook sharing tool.

Saavy users: Incognito gateway using AMI template based off HelioCloud + sh startup script for HC magic. Or stock Jupyer + 
YAML for 'HelioCloud lite' (avoid SunPy 'must be a sysadmin to get going' syndrome)

Maybe add DataDog to help people track usage?

## Big Data Use Cases

* Bad: user downloads raw or L0 data from non-cloud archive to process and manage locally
* Bad: user downloads curated data from cloud to laptop
* Better: users access curated cloud A data from their cloud B installation (same-arch aka AWS, or cross-arch?)
* Best: data and compute are in same cloud

Cost handling: charge users who are not in the cloud?
