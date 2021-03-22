# ramona

_I'd forever talk to you  
But soon my words  
Would turn into a meaningless ring_  

-- Bob Dylan, _To Ramona_

## Quickstart

*  see the file [demo_ramona.ipynb](demo_markov.ipynb)
    * presents the theory and implementation details.
* see the file [ramona/model.py](ramona/model.py) for the NLP full implementation
    * uses NLTK, which needs *punkt* installed
* run the interactive command interface [ramona.py](ramona.py)
    * clone this repo, create a venv, install the requirements then
    * `bash_prompt>  python3 ramona.py`
    * type `help` to get a list of commands
    * see the demo screencast here: [TODO]



## Theory

This software was inspired by the following video on Khan Academy:  
https://www.youtube.com/watch?v=WyAtOqfCiBw

The original implementation stored lists of trigrams in each state, with duplicates,
in order to implement the distribution.  This approach was inefficient.

The current implementation does two passes.  A first pass to count the continuation states, and 
a second pass to convert the counts into probabilities.

See the implementation section below for more details.

More theory:

Origin of Markov Chains:  
https://www.khanacademy.org/computing/computer-science/informationtheory/moderninfotheory/v/markov_chains


The original Shannon paper "A Mathmatical Theory of Communication"  
http://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf


## Implementation
* see the file [demo_ramona.ipynb](demo_markov.ipynb)
* see the file [ramona/model.py](ramona/model.py) for the NLP full implementation

## Setup and Quickstart

- clone the repo
- setup a virtual environment
- install the requirements
- run ramona.py

```
#cd to new folder
$ git clone https://github.com/jdanndc/ramona.git
$ cd ramona
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ python3 ramona.py
### see ramona commands
ramona> help
### select all amer_lit
ramona> set 26 27 28 
###ramona> set ~amer
ramona> load
ramona> talk
ramona> reset
### load poe
ramona> set 15 16 17 19 20
ramona> load
ramona> talk
```
see file [requirements.txt](requirements.txt)

### nltk
ALERT: the quickstart steps were tested and shown to work, but
the testing machine had NLTK already installed.  

More setup might be needed 
for NLTK punkt library.

TODO: document the steps

nltk used **punkt**
download to /usr/local/share/nltk_data/tokenizers/punkt


