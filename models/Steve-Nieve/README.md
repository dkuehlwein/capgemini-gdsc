#Steve Nieve - Find the references that make the difference now!

> **Naive Reference Recommendation Engine**
>
> **Created for Capgemini Global Data Science Challenge IV**
>
> **Developed by Tom Kochuyt**

#How to use

**To search for matching references, open a command shell and type**

    $>python .\GDSC_recommendation_model.py [-h] [-r 10] [-s] query

*Positional arguments:*

    query                   Search query between quotes, e.g. "This is the query"

*Optional arguments:*

    -h, --help              Show this help message and exit
    -r 10, --results 10     Number of results to return, default is 10
    -s, --single            Output matches as single line, default is False


**To train the recommendation model on a set of references**

    $>python .\GDSC_model_training.py [-h] folder

*Positional arguments:*

    folder                  Folder containing reference files, e.g. "D:\data_files"

*Optional arguments:*

    -h, --help              Show this help message and exit


#Dependencies / Third-party Libraries

- [Python >= 3.6](https://www.python.org/)
- [plac](https://pypi.python.org/pypi/plac)
- ... (more to come)
