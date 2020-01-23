## Tidy data from IMDB.com

## Packages

import pandas as pd
import numpy as np
import sys


def tidy_raw_scrap(year):
    '''
    :param filename: name of the raw_data file to tidy up
    :return: a tidy dataframe
    '''
    filename = 'movies_' + year + '.csv'
    df = pd.read_csv('./imdb/1. raw_data/' + filename)
    print(filename + ' read')

    df = df.fillna('')

    ## tidying genres list
    df['Genre'] = [x.replace('\n','').strip() for x in df['Genre']]

    ## tidying runtimes list
    df['Runtime_unit'] = [x[x.find('min'):] if x[-3:] == 'min' else x for x in df['Runtime']]
    df['Runtime'] = [x[:x.find('min')-1] if x[-3:] == 'min' else x for x in df['Runtime']]

    ## replacing comma for dot in votes list
    df['Votes'] = [x.replace(',','.') for x in df['Votes']]

    ## tidying gross list
    df['Gross_unit'] = [x[-1] if x != '' else x for x in df['Gross']]
    df['Gross'] = [x[1:(len(x)-1)] if x != '' else x for x in df['Gross']]

    ## tidying metascores
    #df['Metascore'] = [x.strip() for x in df['Metascore']]


    print(filename + ' tidied up')

    return(df)


#########################################################################

if __name__ == '__main__':
    years = sys.argv[1:]

    for year in years:
        df = tidy_raw_scrap(year)
        file = 'movies_' + year + '.csv'
        path = './imdb/2. tidy_data/tidy_' + str(file)
        df.to_csv(path, index = False)

        print('File written on ' + path)