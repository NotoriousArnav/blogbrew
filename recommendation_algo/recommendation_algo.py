from typing import List, Dict, Any
import math
import ollama
import json
from concurrent.futures import ThreadPoolExecutor
import time

class CosineSimilarity:
    """A class for computing the cosine similarity between two vector embeddings."""

    @staticmethod
    def find_vector_magnitude(vec: List[float]) -> float:
        """
        Calculate the magnitude (Euclidean norm) of a vector.
        Args:
            vec (List[float]): The vector.
        Returns:
            float: The magnitude of the vector.
        """
        return math.sqrt(sum(component ** 2 for component in vec))

    @staticmethod
    def vector_dot_product(vec1: List[float], vec2: List[float]) -> float:
        """
        Calculate the dot product of two vectors.
        Args:
            vec1 (List[float]): The first vector.
            vec2 (List[float]): The second vector.
        Returns:
            float: The dot product of the two vectors.
        """
        if len(vec1) != len(vec2):
            raise ValueError("Both vectors must have the same length")
        return sum(x * y for x, y in zip(vec1, vec2))

    @staticmethod
    def calculate(vec1: List[float], vec2: List[float]) -> float:
        """
        Calculate the cosine similarity between two vectors.
        Args:
            vec1 (List[float]): The first vector.
            vec2 (List[float]): The second vector.
        Returns:
            float: The cosine similarity between the two vectors.
        """
        dot_product = CosineSimilarity.vector_dot_product(vec1, vec2)
        magnitude_product = (CosineSimilarity.find_vector_magnitude(vec1) * CosineSimilarity.find_vector_magnitude(vec2))
        if magnitude_product == 0:
            raise ValueError("Magnitude of one or both vectors is zero, cannot compute cosine similarity")
        return dot_product / magnitude_product


class FindSimilarity():
    # Precompute embeddings and save to JSON (run this once)
    @staticmethod
    def precompute_embeddings(tags: List[str], filename: str) -> None:
        embeddings = {}

        for tag in tags:
            response = ollama.embeddings(model="nomic-embed-text", prompt=tag)
            embeddings[tag] = response["embedding"]
        
        # Save to JSON
        with open(filename, "w") as file:
            json.dump(embeddings, file, indent=4)


    # Load embeddings from JSON
    @staticmethod
    def load_embeddings(filename: str) -> Dict[str, List[float]]:
        with open(filename, "r") as file:
            return json.load(file)


    # Parallel cosine similarity calculation
    @staticmethod
    def find_similar_tags(input_embedding: List[float], stored_embeddings: Dict[str, List[float]]) -> list[tuple[Any, float]]:
        def compute_similarity(tag_embedding):
            tag, embedding = tag_embedding
            score = CosineSimilarity.calculate(input_embedding, embedding)
            return tag, score
        
        # Parallel computation
        with ThreadPoolExecutor() as executor:
            results = list(executor.map(compute_similarity, stored_embeddings.items()))
        
        # Sort results by similarity
        return sorted(results, key=lambda x: x[1], reverse=True)



# Your tag list
input_tag = "Python Coding"
tags_list = ["Tech", "Engineering", "Artifical Intelligence", "Computer Science", "Electronics"]

print("Available tags: ", tags_list)

## Main computation starts here

start_time = time.time()

FindSimilarity.precompute_embeddings(tags_list, "./vec_db.json")


response = ollama.embeddings(model="nomic-embed-text", prompt=input_tag)
input_tag_embedding = response["embedding"]


# Load precomputed embeddings
stored_embeddings = FindSimilarity.load_embeddings("./vec_db.json")

print(f"Current tag: {input_tag}")

# Find similar tags
similar_tags = FindSimilarity.find_similar_tags(input_tag_embedding, stored_embeddings)
recommended_tags_list = []

# Sort through the list to find the most relevant tags. Using a threshold marker of 0.65
for embedding_data in similar_tags:
    if embedding_data[1] >= 0.65:
        recommended_tags_list.append(embedding_data[0])

print("Most Recommended tags: ")
for recommended_tag in recommended_tags_list:
    print(recommended_tag + " " , end="")

print("\n")
print("Other recommended tags: ")

for tag in similar_tags:
    if(tag[0] in recommended_tags_list):
        pass
    else:
        print(tag[0]+f"(score: {tag[1]:2f})" + ", ", end="")

print("\n")
print("--- Program took %s seconds ---" % (time.time() - start_time))