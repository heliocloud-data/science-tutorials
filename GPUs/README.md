## Start at GPU Tutorials.

Steps to do:
1) Finish getting them to work on HelioCloud
2) Add a citation block at the start indicating
   a) where the originals are from (author, event, and URL), and
   b) what license they are covered under
3) Creating an index framing them for scientists to walk through ('if you want do this kind of problem, see this tutorial')

In theory we can monitor using 'nvidia-smi-l 1' to see if/when GPU is invoked.  Current testing using in-Notebook statements shows GPUs used but I'm not always seeing it in the nvidia-smi-l command, so need to improve my knowledge of GPU usage.

* Notebook | Source | uses | GPU usage?

* TF_GPU_demo tensorflow.org/guide/gpu | tensorflow | doesn't seem to actually use GPU? verify
* DST_Clustering | hapi-nn package | tensorflow keras and sklearn | fails with 'DNN library not seen'
* Boundary_Simple & Boundary_Tensorflow | PyHC SS2024 | tensorflow | 'simple' is non-tensorflow
* skip_psf_deconvolution |  AIAPy | CuPy | %pip install cupy sometimes has trouble
* HelioML_Chapter1 (CMEs) |  helioML.org | sklearn but patch to use GPUs? | Didn't use GPU?
* HelioML_Chapter2 (DEM) |
* HelioML_Chapter7 (MMS) | 

