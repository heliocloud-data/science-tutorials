# Sample Use Cases

Tackling the 'who will use HelioCloud' and 'why use HelioCloud' through likeliest use cases. By targeting known or likely use cases, we can avoid the 'design for everything' to focus on the core abilities we should finalize first.

## Science Use Cases


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
