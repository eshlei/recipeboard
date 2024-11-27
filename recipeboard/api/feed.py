import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import os
from sklearn.metrics.pairwise import cosine_similarity
from typing import List
import random

from .models import User, Recipe

def load_recipes(directory='../data/allrecipes/recipes'):
    '''
    Add .txt files to `Recipe` table
    '''
    for file_name in os.listdir(directory):
        if not file_name.endswith('.txt') or Recipe.objects.filter(file_name=file_name).exists():
            continue
        with open(os.path.join(directory, file_name), 'r', encoding='utf-8') as f:
            content = f.read()
            if len(content.splitlines()) != 4:
                continue
            title, url, directions, reviews = content.splitlines()
            recipe = Recipe(file_name=file_name, title=title, url=url, directions=directions, reviews=reviews)
            recipe.save()

load_recipes()
recipes = [recipe.get_text() for recipe in Recipe.objects.all()]
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(recipes)
scores = cosine_similarity(tfidf_matrix)

def vsm_get_docs(user: User, relevant=True, n=10) -> List[Recipe]:
    # `user_likes` and `user_dislikes` are `Recipe` instances. See .model.py
    user_likes = [recipe for recipe in user.likes.all()]
    user_dislikes = [recipe for recipe in user.dislikes.all()]
    
    # `similarity_scores` is an 1D numpy array
    if user_likes:
        doc_indices = [recipe.id for recipe in user_likes]
        similarity_scores = np.mean(scores[doc_indices], axis=0)
    else:
        similarity_scores = np.mean(scores, axis=0)
    
    relevant_docs = [Recipe.objects.get(id=idx+1) for idx in np.argsort(similarity_scores)[::-1]]
    if relevant:
        return relevant_docs[:n]
    else:
        return relevant_docs[:n:-1]
    
def apply_feedback(user: User, doc: Recipe, like=True):
    if like:
        user.likes.add(doc)
    else:
        user.dislikes.add(doc)

def get_cuisine_docs(cuisine_type: str, n=5) -> List[Recipe]:
    relevant_docs = []
    for recipe in Recipe.objects.all():
        if cuisine_type.lower() in recipe.get_text().lower():
            relevant_docs.append(recipe)
    return random.sample(relevant_docs, k=n)

'''
if not User.objects.filter(id=1).exists():
    user = User()
    user.save()
else:
    user = User.objects.get(id=1)
doc_1 = Recipe.objects.get(file_name="6687.txt")
doc_2 = Recipe.objects.get(file_name="6697.txt")
doc_3 = Recipe.objects.get(file_name="6732.txt")
apply_feedback(user, doc_1, like=True)
print("Recommended docs:", [recipe.title for recipe in vsm_get_docs(user)])
apply_feedback(user, doc_2, like=True)
print("Recommended docs:", [recipe.title for recipe in vsm_get_docs(user)])
apply_feedback(user, doc_3, like=True)
print("Recommended docs:", [recipe.title for recipe in vsm_get_docs(user)])
print("Cuisine-specific docs:", [recipe.title for recipe in get_cuisine_docs("Italian")])
'''