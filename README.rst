pl-cni_challenge
================================

.. image:: https://badge.fury.io/py/cni_challenge.svg
    :target: https://badge.fury.io/py/cni_challenge

.. image:: https://travis-ci.org/FNNDSC/cni_challenge.svg?branch=master
    :target: https://travis-ci.org/FNNDSC/cni_challenge

.. image:: https://img.shields.io/badge/python-3.5%2B-blue.svg
    :target: https://badge.fury.io/py/pl-cni_challenge

.. contents:: Table of Contents


Abstract
--------

This app was created for submissions to the MICCAI CNI 2019 Challenge: http://www.brainconnectivity.net/challenge.html

Submissions are accepted as containerised Docker images. This allows you to submit your Challenge solution in your choice of open-source language and version. And it enables us to easily run your solution without having to install multiple programs required for execution.

The ``cni_challenge.py`` app is a wrapper for you to add your code/package which is then containerised by Docker.
While this is coded in Python and currently contains a bare bones example also in Python, other languages are possible.

NB: This current repo does not have a working demonstration in C yet. More to come on that.

For further information on how to submit your solution, see here http://www.brainconnectivity.net/challenge_subm.html

``cni_challenge.py`` is a ChRIS-based application: https://github.com/FNNDSC/CHRIS_docs, for more information on the original ChRIS-app: https://github.com/FNNDSC/cookiecutter-chrisapp.


Synopsis
--------

This bare bones example demonstrates a python program which performs a rotation on a list of vectors. It will demonstrate how to pass in string inputs, read in and output to respective, mandatory directories, and how to incorporate python code and packages for the app to retrieve and for DockerHub to containerize.

.. code::

    python cni_challenge.py                                         \
        [-v <level>] [--verbosity <level>]                          \
        [--version]                                                 \
        [--man]                                                     \
        [--meta]                                                    \
        <inputDir>                                                  \
        <outputDir>                                                 \
        [--run_option < python || C >]                              \
        [--rot <matrix_file.txt>]                                   \

Installation Requirements and Quick Setup
----------------------------

1. Install ``Python`` (3.5+) and ``pip`` (which is usually installed with Python)
2. Create a GitHub account on https://github.com/ if you don't already have one, and install on machine.
3. Create a DockerHub account on https://hub.docker.com/ if you don't already have one.
4. Install latest ``Docker`` (17.04.0+) if you want to test your plugin's docker image and containers on your local machine. 
   To install on Ubuntu 18.04:      
      
.. code:: bash

            apt-get remove docker docker-engine docker.io 
            apt install docker.io  
    
Otherwise, visit https://docs.docker.com/install/ for installation directions

5. Fork this pl-cni_challenge repository to your GitHub.
6. Log onto your DockerHub account and create a new repository with automated build.
   In 'Account Settings' -> 'Linked Accounts', connect your GitHub account to DockerHub.

   Then back in your DockerHub home, click the ``Create Repository +``  button. The website page will walk you through setting up the automated build. When prompted for the GitHub repository that you’d like to use for the automated build select the pl-cni_challenge repository that you just forked/cloned. Name the Docker repository ${cni_challenge_DockerRepo} and make it Public.

   **It is extremely important that you tag your automatically built docker image with an appropriate version number based on your GitHub tags**.
   Create a new build rule by clicking the ``BUILD RULES +``  button. A good rule good be **Source type:** ``Tag``,
   **Source:** ``/^[0-9.]+$/`` and **Docker Tag:** ``version-{sourceref}``.

   Do not delete the default build rule that is already in place, this handles the 'latest' tag for pulling the most recent Docker image.

   Click ``Create && Build``  button to finish the setup and trigger the automated build.
   For more information on Automated Builds, please visit https://docs.docker.com/docker-hub/builds/. 

   After the build has completed, the ``cni_challenge`` bare bones example is now available as a Docker image to be pulled from your DockerHub. The link to it will be ${your_Docker_account name}/${cni_challenge_DockerRepo}.

Arguments
---------

.. code::

    <inputDir> 
    Mandatory. A directory which contains all necessary input files.
        
    <outputDir>
    Mandatory. A directory where output will be saved. Must be universally writable to.
        
    [--run_option < python || C >
    Mandatory for bare bones example. C example still to come!
        
    [--rot <matrix_file.txt>]
    Mandatory for bare bones example. String of file containing rotation matrices.

    [-v <level>] [--verbosity <level>]
    Verbosity level for app. Not used currently.

    [--version]
    If specified, print version number. 
    
    [--man]
    If specified, print (this) man page.

    [--meta]
    If specified, print plugin meta data.


Run
----

This ``plugin`` can be run in two modes: natively as a python package or as a containerised Docker image.

Run locally
~~~~~~~~~~~~

.. code:: bash

    cni_challenge.py --man

to get inline help. And the following to run the bare-bones example:

.. code:: bash

    cni_challenge.py --run_option python --rot rotation_matrices.txt /destination/to/inputdir /destination/to/outputdir


Using ``docker run``
~~~~~~~~~~~~~~~~~~~~

Pull the latest ``cni_challenge`` image to your machine:

.. code:: bash

    docker pull ${your_Docker_account name}/${cni_challenge_DockerRepo}

To run using ``docker``, be sure to assign the input directory to ``/incoming`` and the output directory to ``/outgoing``. *Make sure that the* ``$(pwd)/outputdir`` *directory is world writable!* These directories must be named ``inputdir`` and ``outputdir``. 
For the bare bones example, copy the expected input files (``rotation_matrices.txt`` and  ``vectors.txt``) from the GitHub repo and place it in ``inputdir``.

.. code:: bash

    mkdir inputdir outputdir && chmod 777 outputdir
    cp ${cni_challenge_github_repo}/inputdir/* $(pwd)/inputdir

Now, prefix all calls with 

.. code:: bash

    sudo docker run --rm -v $(pwd)/inputdir:/incoming -v $(pwd)/outputdir:/outgoing ${your_Docker_account name}/${cni_challenge_DockerRepo} cni_challenge.py  --run_option python --rot rotation_matrices.txt /incoming /outgoing

The output file of rotated vectors,  ``classifications.txt``, will be in  ``outputdir``.

Our barebones Docker image can be retrieved (from DockerHug 'aiwc') and executed (calling 'man') on your machine as follows (with directories 'inputdir' and 'outputdir' as specified above):

.. code:: bash

    docker pull aiwc/pl-cni_challenge
    sudo docker run --rm -v $(pwd)/inputdir:/incoming -v $(pwd)/outputdir:/outgoing      \
                 aiwc/pl-cni_challenge cni_challenge.py                                  \
                 --man                                                                   \
                 /incoming /outgoing


App and Challenge Requirements, Rules
-------------------------------------

* Python packages that are required should be listed in ``requirements.txt`` which will be pip installed and included in the Docker container.
* For implementations in C or C++, the executable pl-cni_challenge wrapper will create the executable before being passed into DockerHub. This means that make instructions (``makefile``) should be included in ``Dockerfile`` (an example of this is to come).

These requirements are to help us systematically execute and assess Challenge solutions:

* We expect to be able to run your Docker image on the test data with the following command:

.. code:: bash

    sudo docker run --rm -v $(pwd)/inputdir:/incoming -v $(pwd)/outputdir:/outgoing ${your_Docker_account name}/${cni_challenge_DockerRepo} cni_challenge.py /incoming /outgoing

So please remove the mandatory arguments/assignments that were included as examples in the barebones repo to help you (``--rot`` and ``--run_option``)

* Input and output directories are named ``inputdir`` and ``outputdir``, respectively. Your code should expect to read in data from ``inputdir`` as is structured in the ``pl-cni_challenge`` repo as this is how our test data will be structured.
* Output should be a text file in ``outputdir`` called ``classification.txt``. ``classification.txt`` should contain the classification label for each subject with one subject per row (a single column of values). Labels should be 0 = Control, and 1 = Patient. 
* The code to evaluate the performance of your submission is pl-cni_challenge/cni_challenge/evaluation/classification_metrics.py, which will be executed as: 

.. code:: bash

    classification_metrics.py -p classification.txt -g ${goundtruth_file} -o ${output_file}

For information on our performance evaluation criterias, see: http://miccai.brainconnectivity.net/challenge_eval.html

Rules
~~~~~~
* To be considered for a prize, at least one author of a Challenge submission must register for the CNI Challenge at MICCAI 2019.




