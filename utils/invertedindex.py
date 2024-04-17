import ast

class InvertedIndex:
    def __init__(self):
        self.inverted_index = {}
        self.document_lengths = {}  # Store the length of each document for normalization

    def update_index(self, link, tokens):
        """
        Update the inverted index with a single document.

        :param document: A tuple (link, tokens) representing the document
        """

        document_length = 0  # Track the length of the document for normalization

        for token in tokens:
            if token not in self.inverted_index:
                # Initialize the dictionary for this token
                self.inverted_index[token] = {'documents': {link: 1}, 'document_frequency': 1}
            else:
                # Update term frequency and document frequency
                if link not in self.inverted_index[token]['documents']:
                    self.inverted_index[token]['documents'][link] = 1
                    self.inverted_index[token]['document_frequency'] += 1
                else:
                    self.inverted_index[token]['documents'][link] += 1

                # Update document length
                document_length += 1

        # Store the document length for normalization
        self.document_lengths[link] = document_length

    def get_documents(self, token):
        """
        Retrieve documents containing a specific token.

        :param token: The token to query in the index
        :return: Dictionary with document links and corresponding term frequencies
        """
        return self.inverted_index.get(token, {}).get('documents', {})

    def get_document_frequency(self, token): #NUMBER OF DOCUMENTS IN THE COLLECTION THAT CONTAINS TERM T
        """
        Retrieve the document frequency of a specific token.

        :param token: The token to query in the index
        :return: Document frequency of the token
        """
        return self.inverted_index.get(token, {}).get('document_frequency', 0)

    def get_term_frequencies(self, document_link):
        """
        Retrieve term frequencies for all tokens in a specific document.

        :param document_link: The link of the document to query
        :return: Dictionary of term frequencies for the document
        """
        term_frequencies = {}
        for token, info in self.inverted_index.items():
            if document_link in info['documents']:
                term_frequencies[token] = info['documents'][document_link]

        return term_frequencies

    def get_term_frequency(self, document_link, token):
        """
        Retrieve the term frequency for a specific token in a given document.

        :param document_link: The link of the document to query
        :param token: The token for which to retrieve the term frequency
        :return: The term frequency for the specified token in the document (0 if not found)
        """
        if token in self.inverted_index:
            info = self.inverted_index[token]
            return info['documents'].get(document_link, 0)
        else:
            return 0

    def get_total_documents(self):
            """
            Get the total number of documents in the inverted index.

            :return: Total number of documents
            """
            return len(self.document_lengths)

    
inverted_index = InvertedIndex()
