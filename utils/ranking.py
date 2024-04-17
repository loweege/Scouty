import ast
import numpy as np
import math
from collections import Counter, OrderedDict
from codeparser import parser
from utils import invertedindex
from utils import dataset


def norm(vector):
    """
    Calculate the Euclidean norm (also known as the Euclidean length or L2 norm) of a vector.

    Parameters:
    vector (list of float or int): A list of numbers representing the vector.

    Returns:
    float: The Euclidean norm of the vector.

    Example:
    >>> norm([3, 4])
    5.0
    """
    x = 0
    for i in range(len(vector)):
        x = x + (vector[i] * vector[i])
    
    return math.sqrt(x)

def query_term_frequency(vector, term):
    """
    Calculate the frequency of a given term in a list (vector).

    This function counts the occurrences of a specific term in a provided list and returns its frequency.

    Parameters:
    vector (list): A list of elements (can be of any data type) in which to count the term.
    term (any type): The term to search for in the vector. The type of 'term' should match the elements in the vector.

    Returns:
    int: The frequency of the term in the vector.

    Example:
    >>> query_term_frequency(["apple", "banana", "apple", "cherry"], "apple")
    2
    """
    element_counts = Counter(vector)
    term_frequency = element_counts[term]
    return term_frequency



def get_tokens_from_vectorized_document(vectorized_doc):
    """
    Extracts and returns tokens from a vectorized document that is provided as a string representation of a list.

    This function attempts to parse a string which is expected to be in the format of a Python list representation. 
    It's primarily used to convert a stringified version of a tokenized document back into a list of tokens. 
    If the string cannot be parsed due to formatting issues, the function will handle the error and return an empty list.

    Parameters:
    vectorized_doc (str): A string representation of a vectorized document. 
                          It should be in the format of a Python list. For example, "['token1', 'token2', 'token3']".

    Returns:
    list: A list of tokens if the conversion is successful, or an empty list in case of a parsing error.

    Raises:
    ValueError, SyntaxError: If there is an error in converting the string to a list.

    Example:
    >>> get_tokens_from_vectorized_document("['hello', 'world']")
    ['hello', 'world']
    """
    try:
        tokens = ast.literal_eval(vectorized_doc)
        return tokens
    except (ValueError, SyntaxError) as e:
        print(f"Error while parsing document: {e}")
        return []


def transform_to_non_normalized_tfidf(document_link):
    """
    Transform a document into its non-normalized TF-IDF vector representation.

    This function computes the Term Frequency-Inverse Document Frequency (TF-IDF) 
    vector for a given document. 

    Parameters:
    document_link (str): A link to the document for which the TF-IDF vector is to be computed.

    Returns:
    list: A list of TF-IDF scores, one for each term in the document.

    The function iterates over each token in the document. For each token, it calculates:
    - Term Frequency (TF): The number of times the token appears in the document.
    - Document Frequency (DF): The number of documents in which the token appears.
    - Inverse Document Frequency (IDF): A measure of how much information the word provides.
    
    These values are used to calculate the TF-IDF score for each term. The function
    returns a list of these scores, representing the non-normalized TF-IDF vector 
    of the document.

    Note:
    This function relies on a global `invertedindex` object with a specific structure and methods.
    Ensure that `invertedindex.inverted_index.inverted_index`, `invertedindex.inverted_index.get_term_frequency`,
    `invertedindex.inverted_index.get_document_frequency`, and `invertedindex.inverted_index.get_total_documents`
    are defined and accessible.
    """
    
    tdfidf_vector = []

    for token in dataset.documents[document_link]:
        tf = invertedindex.inverted_index.get_term_frequency(document_link, token)
        df = invertedindex.inverted_index.get_document_frequency(token)
        N = invertedindex.inverted_index.get_total_documents()
       
        if ((tf == 0) or (df ==0) or ((N/df) == 0)):
            tdfidf_vector.append(0)
        else:
            weighted_tf = 1 + np.log(tf)
            idf = np.log(N/df)
            
            tdfidf_vector.append(weighted_tf * idf)
    
    return tdfidf_vector
    
    

def transform_to_normalized_tfidf(document_link):
    """
    Transform a document into its normalized TF-IDF vector representation.

    This function first computes the non-normalized TF-IDF vector for a given document 
    using the `transform_to_non_normalized_tfidf` function. It then normalizes this 
    vector to have a unit length, which makes it suitable for various applications 
    like cosine similarity computation in information retrieval.

    Parameters:
    document_link (str): A link to the document for which the normalized TF-IDF 
                         vector is to be computed.

    Returns:
    list: A list of normalized TF-IDF scores, one for each term in the inverted index.

    The normalization process involves dividing each term's TF-IDF score by the Euclidean 
    norm (L2 norm) of the entire vector. This results in a vector where the sum of the 
    squares of the values is 1, often considered as 'unit length' in vector space.

    This function depends on `transform_to_non_normalized_tfidf` for the initial 
    TF-IDF vector computation. Ensure that this dependency is correctly resolved in your
    implementation environment.

    Note:
    - The function assumes that the document_link provided is valid and that the
      `transform_to_non_normalized_tfidf` function returns a non-empty vector.
    - Ensure that the numpy library is installed and imported for the norm calculation.
    """
    tfidf_vector = transform_to_non_normalized_tfidf(document_link)
    vector_norm = norm(tfidf_vector)

    if vector_norm != 0:
        tfidf_vector = [tfidf_score / vector_norm for tfidf_score in tfidf_vector]
    
    return tfidf_vector
                

def rough_query_to_non_normalized_tfidf(query):
    """
    Compute the non-normalized TF-IDF vector for a given query.

    This function calculates the TF-IDF vector for each term in the query. 
    It's similar to transforming a document into its TF-IDF representation, 
    but this function is specifically tailored for queries.

    Parameters:
    query: vectorized document.

    Returns:
    list: A list of TF-IDF scores, one for each term in the query.

    For each term in the query, the function computes:
    - Term Frequency (TF): The frequency of the term in the query.
    - Document Frequency (DF): The number of documents in the corpus containing the term.
    - Inverse Document Frequency (IDF): A measure of how much information the term provides.
    
    The function returns a list of TF-IDF scores for the terms in the query.
    Note: The function relies on `query_term_frequency` and methods from `invertedindex.inverted_index`.
    """
    tdfidf_vector = []

    for term in query:
        tf = query_term_frequency(query, term)
        df = invertedindex.inverted_index.get_document_frequency(term)
        N = invertedindex.inverted_index.get_total_documents()

        if ((tf == 0) or (df == 0) or ((N/df) == 0)):
            tdfidf_vector.append(0)
        else:
            weighted_tf = 1 + np.log(tf)
            idf = np.log(N/df)
            
            tdfidf_vector.append(weighted_tf * idf)
    
    return tdfidf_vector

def scoring(query, normq, normd, document_link):
    """
    Calculate the relevance score of a document with respect to a query.

    This function computes a score indicating how relevant a document is 
    to a given query. It uses the TF-IDF weights of terms in the query and 
    the document, normalized by their respective vector norms.

    Parameters:
    query (list of str): vectorized document.
    normq (float): The norm of the query's TF-IDF vector.
    normalized_document (float): The norm of the document's TF-IDF vector.
    document_link (str): A link to the document being scored.

    Returns:
    float: A score representing the relevance of the document to the query.

    The function computes the weighted term frequency for each term in the query and the document,
    multiplies it with the term's IDF, and normalizes the score by the corresponding vector norms.
    It sums up these values to get the final relevance score.

    Note: The function relies on `query_term_frequency` and methods from `invertedindex.inverted_index`.
    """
    N = invertedindex.inverted_index.get_total_documents()
    result = 0

    for term in query:
        tfq = query_term_frequency(query, term)
        tfd = invertedindex.inverted_index.get_term_frequency(document_link, term)
        df = invertedindex.inverted_index.get_document_frequency(term)

        if df != 0 and tfd != 0 and tfq != 0:
            weighted_tfd = 1 + np.log(tfd)
            weighted_tfq = 1 + np.log(tfq)
            idf = np.log(N/df)
        else:
            weighted_tfd = 0
            weighted_tfq = 0
            idf = 0
            
        try:
            result += ((weighted_tfq * idf)/normq) + ((weighted_tfd * idf)/normd)
        except ZeroDivisionError:
            result += 0

    return result

