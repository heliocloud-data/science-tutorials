"""
Run the Testing (or other notebook) in console or pipeline.

Works as-is on HelioCloud.

If not on HelioCloud i.e. from a laptop, you need to install:
   pip install nbformat
   pip install ipykernel
and also set S3 keys.
"""


import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

notebook = '01_Testing_Notebook.ipynb'

nb = nbformat.read(notebook, as_version=4)
ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
ep.kernel_kwargs = {
    "extra_arguments": [
        "--InteractiveShellApp.exec_lines=interactive=False"
        ]
    }
ep.preprocess(nb, {"metadata": {"path": "."}})

with open('output'+notebook,"w",encoding="utf-8") as fout:
    nbformat.write(nb,fout)
    

""" Sample plot capture and compare

plt.figure()
plt.plot(var_data)
plt.xlabel("Index")

def headless_plot_analysis(plt):
    testfig = plt.gcf()              # current figure
    testax = plt.gca()              # current axes
    lines = testax.get_lines()      # list of Line2D objects
    x_min, x_max = testax.get_xlim()
    y_min, y_max = testax.get_ylim()
    print('Limits ',x_min, x_max, y_min, y_max)
    print('xaxis label is ',testax.get_xlabel())
    print('# lines ',len(lines))
    #print('line 0 are',lines[0].get_ydata())
    return [len(lines), x_min, x_max, y_min, y_max, testax.get_xlabel()]

import math
def limitcheck(A, B, compare='Int'):
    print(A,B)
    if compare == 'Int':
        A=[int(x) for x in A]
        B=[int(x) for x in B]
    return [math.isclose(i, j) for i, j in zip(A, B)]
    
if headless:
    samples = headless_plot_analysis(plt)
    data = [-21.1, 443.1, -744.516, 15634.844]
    outcomes = limitcheck(samples[1:-1],data,compare='Int')
    print(outcomes)
    assert limits[0] == 16 and limits[-1] == 'Index' and outcomes
else:
    plt.show()

"""
