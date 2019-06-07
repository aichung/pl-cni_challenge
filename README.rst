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

Submissions are accepted as containerised Docker images. This allows you to be able to submit your solution in any open-source language and version. And it enables us to easily run your solution without having to install multiple programs required for execution.

The ``cni_challenge.py`` app is a wrapper for you to add your code/package which is then be containerised by Docker.
While this is coded in Python and currently contains a bare bones example also in Python, other languages are possible.

NB: This current repo does not have a working demonstration in C yet.

``cni_challenge.py`` is a ChRIS-based application: https://github.com/FNNDSC/CHRIS_docs


Synopsis
--------

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

Requirements and Quick Setup
----------------------------

1. Install ``Python`` (3.6.7+) and ``pip`` (which is usually installed with Python)
2. Create a GitHub account on https://github.com/ if you don't already have one, and install on machine.
3. Create a Docker account on https://hub.docker.com/ if you don't already have one.
4. Install latest ``Docker`` (17.04.0+) if you want to test your plugin's docker image and containers on your local machine. 
      To install on ubuntu 18.04:      
      
.. code:: bash

            apt-get remove docker docker-engine docker.io 
            apt install docker.io  
    
Otherwise, visit https://docs.docker.com/install/ for installation directions

5. Fork or clone this pl-cni_challenge repository to your GitHub.
6. Log onto your Docker Hub account and create a new repository with automated build.
   In 'Account Settings' -> 'Linked Accounts', connect your GitHub account to Docker.

   Then back in your DockerHub home, click the ``Create Repository +``  button. The website page will walk you through setting up the automated build. When prompted for the GitHub repository that you’d like to use for the automated build select the pl-cni_challenge repository that you just forked/cloned. Make the Docker repository Public.

   **It is extremely important that you tag your automatically built docker image with an appropriate version number based on your GitHub tags**.
   Create a new build rule by clicking the ``BUILD RULES +``  button. A good rule good be **Source type:** ``Tag``,
   **Source:** ``/^[0-9.]+$/`` and **Docker Tag:** ``version-{sourceref}``.

   Click ``Create && Build``  button to finish the setup and trigger the automated build.
   For more information on Automated Builds, please visit https://docs.docker.com/docker-hub/builds/. 


Arguments
---------

.. code::

    <inputDir> 
    Mandatory. A directory which contains all necessary input files.
        
    <outputDir>
    Mandatory. A directory where output will be saved to. Must be universally writable to.
        
    [--run_option < python || C >]
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

Run locally:
~~~~~~~~~~~~

.. code:: bash

    cni_challenge.py --man

to get inline help.

.. code:: bash

    cni_challenge.py /some/inputdir /destination/to/outputdir --run_option python --rot rotation_matrices.txt


Using ``docker run``
~~~~~~~~~~~~~~~~~~~~

To run using ``docker``, be sure to assign an "input" directory to ``/incoming`` and an output directory to ``/outgoing``. *Make sure that the* ``$(pwd)/out`` *directory is world writable!*

Now, prefix all calls with 

.. code:: bash

    docker run --rm -v $(pwd)/inining (pwd)/out:/outgoing pl-cni_challenge cni_challenge.py

Thus, getting inline help is:

.. code:: bash

    mkdir in out && chmod 777 out
    docker run --rm -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing      \
            pl-cni_challenge cni_challenge.py                        \
            --man                                                       \
            /incoming /outgoing

Examples
--------





