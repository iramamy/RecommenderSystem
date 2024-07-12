import pickle
import numpy as np

# with open('movie_matrix.pkl', 'rb') as f:
#     movie_matrix = pickle.load(f)

# with open('movie_bias.pkl', 'rb') as f:
#     movie_bias = pickle.load(f)

def recommend_movies_for_user(
        user_movie_ids,
        movie_matrix,
        movie_biases,
        num_recommendations=12,
        regularization_factor=0.9
        ):

    # Aggregate user preferences across all watched movies
    user_preference_vector = np.zeros_like(movie_matrix[0])
    for movie_id in user_movie_ids:
        user_preference_vector += movie_matrix[movie_id]

    # Normalize preference vector
    user_preference_vector /= len(user_movie_ids)

    _recommended_movies = []
    
    # Calculate preference scores for each movie
    for movie_id in range(len(movie_matrix)):
        preference_score = np.dot(
            user_preference_vector,
            movie_matrix[movie_id, :]
            ) + regularization_factor * movie_biases[movie_id]

        _recommended_movies.append((movie_id, preference_score))

    # Sort movies by preference score in descending order
    _recommended_movies = sorted(_recommended_movies, key=lambda x: x[1], reverse=True)

    rec = []
    for movie in _recommended_movies:
        if movie[0] not in user_movie_ids:
            rec.append(movie[0])

    topN_movie_id = rec[:num_recommendations]

    return topN_movie_id

