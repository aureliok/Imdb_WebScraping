## WebScraping from IMDB.com

## This script extracts informations of movies released on a given period of time from IMDB.com

# Packages
import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys


def get_movies(year):
    '''
    :param year: release year to scrape movies from imdb.com.
    :return: a pandas dataframe containing information of each movie's title,
             year, genre, runtime, gross, rating and number of votes.
    '''

    ## Getting the url
    url = ('https://www.imdb.com/search/title/?title_type=feature&release_date=' + year + '-01-01,' +
           year + '-12-31&count=250')
    website = requests.get(url)

    soup = BeautifulSoup(website.content, 'html.parser')

    ## Getting the number of movies released on the chosen year
    total_movies = soup.find('div',class_='desc').find('span').text
    total_movies = total_movies[total_movies.find('of') + 3:total_movies.find('titles') - 1]
    total_movies = total_movies.replace(',','.')


    ## Filtering only movies list
    movies = soup.find_all('div', class_ = 'lister-item mode-advanced')

    names, years, runtimes, genres, ratings, votes, gross, metascores = ([] for i in range(8))

    total_movies = int(total_movies.replace('.',''))

    ## Capturing the information

    total_pages = total_movies//250
    if(total_movies%250 > 0):
        total_pages += 1

    for page in range(1,total_pages+1):
        if(page == 1):
            url_original = 'https://www.imdb.com'
        else:
            if(soup.find('a',class_='lister-page-next next-page') is not None):
                url_next = soup.find('a',class_='lister-page-next next-page')['href']
                url = url_original + url_next

                website = requests.get(url)

                soup = BeautifulSoup(website.content, 'html.parser')
                movies = soup.find_all('div', class_='lister-item mode-advanced')


        for i in range(len(movies)):

            if(movies[i].h3.a is not None):
                names.append(movies[i].h3.a.text)
            else:
                names.append('')
                #print('Name not found for movie ' + str(i+1))

            if(movies[i].h3.find('span',class_='lister-item-year text-muted unbold') is not None):
                years.append(movies[i].h3.find('span',class_='lister-item-year text-muted unbold').text)
            else:
                years.append('')
                #print('Release year not found for movie ' + str(i+1))

            if(movies[i].p.find('span',class_='runtime') is not None):
                runtimes.append(movies[i].p.find('span',class_='runtime').text)
            else:
                runtimes.append('')
                #print('Runtime not found for movie ' + str(i+1))

            if(movies[i].p.find('span',class_='genre') is not None):
                genres.append(movies[i].p.find('span',class_='genre').text)
            else:
                genres.append('')
                #print('Genre not found for movie ' + str(i+1))

            if(movies[i].find('div',class_='inline-block ratings-imdb-rating') is not None):
                ratings.append(movies[i].find('div',class_='inline-block ratings-imdb-rating').strong.text)
            else:
                ratings.append('')
                #print('Rating not found for movie ' + str(i+1))

            if(movies[i].find('span',text='Votes:') is not None):
                votes.append(movies[i].find('span',text='Votes:').find_next('span').text)
            else:
                votes.append('')
                #print('Votes not found for movie ' + str(i+1))

            if(movies[i].find('span',text='Gross:') is not None):
                gross.append(movies[i].find('span',text='Gross:').find_next('span').text)
            else:
                gross.append('')
                #print('Gross not found for movie ' + str(i+1))

            if (movies[i].find('div', class_='inline-block ratings-metascore') is not None):
                metascores.append(movies[i].find('div', class_='inline-block ratings-metascore').find_next('span').text)
            else:
                metascores.append('')
                # print('Metascore not found for movie ' + str(i+1))

        print('Page: ' + str(page) + '/' + str(total_pages) + ' ' + url)


    movie_df = pd.DataFrame({'Title'   : names,
                             'Year'    : years,
                             'Genre'   : genres,
                             'Runtime' : runtimes,
                             'Rating'  : ratings,
                             'Gross'   : gross,
                             'Votes'   : votes,
                             'Metascore': metascores})

    print("Extracted " + str(total_movies) + " movies released on " + str(year) + " from imdb.com.")

    return(movie_df)

####################################################################

if __name__ == '__main__':
    years = sys.argv[1:]

    for year in years:
        print('Extracting movies from ' + str(year))
        path = './imdb/1. raw_data/movies_' + year + '.csv'
        df = get_movies(year)
        df.to_csv(path, index = False)
        print('csv file written on ' + path)

    print('Done!')





