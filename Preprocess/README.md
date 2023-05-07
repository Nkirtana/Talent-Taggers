# Preprocess Module to clean data and prep for training guided topic model (BERTopic).

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Contributers](#contributers)
- [Features](#features)

## Requirements

- Python

## Installation

Install all the project module requirements
```
  $ pip install -r requirements.txt
```

## Usage
Go to Talent-Tagers project path
```
  $ cd Talent-Taggers/Preprocess
```
Place the resume dataset file in preprocessing/Data path. 
Then, run the main file by running the command
```
  $ python preprocessing/main.py
```
Once the data.pkl file is ready, run the notebook BERTopic_Guided.ipynb, 
this will load the skills extracted in a csv file and place it in Data/guided_skills.csv path

Now add, a column named 'YesOrNo', stating 'Y' for Yes, if it is a skill or 'N' for No, if it is noise; as part of reinforcement.

Finally run the above command, to update the skill database

```
  $ python addGuidedSkills.py
```
 
## Contributors

Contributers for the project feature are:
- Adhitya Manoj
- Anushree Manoharrao
- Awantika Shah
- Kirtana Nambiar
- Lavanya Kumaran
- Manoj Buddha

## Features

- Update skill database using BERTopic
