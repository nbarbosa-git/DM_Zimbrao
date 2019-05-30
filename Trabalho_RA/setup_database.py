import pandas as pd

def remove_duplicates(ratings, movies):
    
    #lista de duplicatas
    all_duplicates =  movies.loc[movies.Movie.duplicated(keep= 'first')].sort_values('Movie')
    first_duplicates =  movies.loc[movies.Movie.duplicated(keep= 'last')].sort_values('Movie')
    
    #Criando uma tabela com o Id_Original X Id_Duplcated
    duplicated_id = first_duplicates.merge(all_duplicates, on='Movie')
    duplicated_id = duplicated_id.loc[:,['Movie_Id_x', 'Movie_Id_y']]
    duplicated_id.columns = ['Original', 'Duplicated']
    #print(duplicated_id)

    #trocando o valor duplicado pelo original nas duas tabelas
    for original, duplicated in zip(duplicated_id.Original , duplicated_id.Duplicated):
        
        
        movies.Movie_Id.loc[movies.Movie_Id==duplicated]=original
        ratings.Movie_Id.loc[ratings.Movie_Id==duplicated]=original
        
    #removendo duplicatas na tabela movies    
    movies = movies.drop_duplicates(keep='first')


    return ratings, movies


# funcão para limpar os datasets
def setup_BD(ratings, movies):
    # retira a coluna 3 da tabela rating e renomeia
    ratings.drop([3], axis=1, inplace=True)
    ratings.columns = ['User_Id','Movie_Id', 'Rating']

    # seleciona apenas as colunas 0 e 1 da tabela movies e renomeia
    movies = movies.loc[:, [0, 1]]
    movies.columns = ['Movie_Id', 'Movie']

    ratings, movies = remove_duplicates(ratings, movies)

    # Criando um merge dos 2 datasets
    ratings = ratings.merge(movies, on='Movie_Id')
    ratings = ratings.loc[:, [ 'User_Id', 'Movie_Id', 'Rating']]
    index = ratings.loc[:, [ 'User_Id', 'Movie_Id']].drop_duplicates(keep='first').index
    ratings = ratings.loc[index, :]
    return ratings, movies

def setup_results(movies, rat, ratings, pca):
    
    #colunas Movie_Id, Nome
    results_df = movies
    

    #coluna rating mean
    mean = pd.DataFrame(ratings.T.mean())
    mean.columns = ['Rating']
    results_df = results_df.merge(mean, on='Movie_Id')


    #coluna views
    views = rat.groupby('Movie_Id').Rating.agg(['count'])
    results_df = results_df.merge(views, on='Movie_Id')
    results_df.rename(columns={'count':'Views'}, inplace=True)
    
    #colunas pca e labels
    results_df = pd.concat([results_df, pca], axis=1)
    

    
    return results_df

#funciona apenas no dataset 100k
def get_genre(original, results):
    
    
    original.columns = ['Movie_Id','movie_title', 'release_date', 'video release date', 'IMDb URL', 'unknown', 'Action', 'Adventure', 'Animation', 'Children\'s','Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir','Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War','Western'] 

    orig = original[:]
    original.drop(['movie_title', 'release_date', 'video release date', 'IMDb URL',], axis=1, inplace=True)
    original = original.T


    original.columns = orig["Movie_Id"]
    original.drop(['Movie_Id'], axis=0, inplace=True)
    
    genre = []
    for cols in original.columns:
        genre.append(original[cols].loc[original[cols]==1].index)
    
    genre = pd.DataFrame(genre)
    genre = genre.loc[:, [0, 1]]
    genre.columns = ['genre 1', 'genre2']
    
    results = pd.concat([results, genre], axis=1)
    
    results = results.loc[:, ['Movie_Id','Movie','genre 1', 'genre2', 'Rating', 'Views', 'labels']]

    
    return results
    




    
