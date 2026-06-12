"""
PROJECT 3: AI RECOMMENDATION LOGIC
Tech Stack Recommender System
Powered by DecodeLabs

This system implements content-based filtering using TF-IDF weighting 
and Cosine Similarity to recommend career paths based on user skills.
"""

import math
from collections import defaultdict
import json

# ============================================================================
# STEP 1: DATASET - Job Roles with Associated Skills
# ============================================================================

JOB_ROLES = {
    "Data Scientist": {
        "skills": ["Python", "SQL", "Machine Learning", "Data Analysis", "TensorFlow", "Statistical Analysis"],
        "description": "Analyzes complex datasets and builds predictive models"
    },
    "DevOps Engineer": {
        "skills": ["Docker", "Kubernetes", "AWS", "CI/CD", "Jenkins", "Cloud Computing"],
        "description": "Manages infrastructure and deployment pipelines"
    },
    "Backend Developer": {
        "skills": ["Java", "Python", "SQL", "APIs", "Microservices", "Database Design"],
        "description": "Builds server-side applications and systems"
    },
    "Cloud Architect": {
        "skills": ["AWS", "Cloud Computing", "Database Design", "Kubernetes", "DevOps", "Automation"],
        "description": "Designs scalable cloud infrastructure solutions"
    },
    "ML Engineer": {
        "skills": ["Python", "Machine Learning", "TensorFlow", "Deep Learning", "Statistical Analysis", "Data Analysis"],
        "description": "Develops and deploys machine learning models"
    }
}


# ============================================================================
# STEP 2: TF-IDF VECTORIZATION
# ============================================================================

class TFIDFVectorizer:
    """Converts text/skills into weighted numerical vectors"""
    
    def __init__(self):
        self.vocabulary = set()
        self.document_frequency = defaultdict(int)
        self.total_documents = 0
    
    def fit(self, documents):
        """Build vocabulary and IDF values from documents"""
        self.total_documents = len(documents)
        
        # Count document frequency for each term
        for doc in documents:
            unique_terms = set(doc)
            for term in unique_terms:
                self.document_frequency[term] += 1
            self.vocabulary.update(doc)
    
    def get_tf(self, document):
        """Calculate Term Frequency"""
        tf = defaultdict(float)
        total_terms = len(document)
        
        for term in document:
            tf[term] += 1
        
        # Normalize by total terms
        for term in tf:
            tf[term] /= total_terms
        
        return tf
    
    def get_idf(self, term):
        """Calculate Inverse Document Frequency with logarithmic dampening"""
        if term not in self.document_frequency:
            return 0
        
        idf = math.log(self.total_documents / self.document_frequency[term])
        return idf
    
    def vectorize(self, document):
        """Create TF-IDF weighted vector for a document"""
        tf = self.get_tf(document)
        vector = {}
        
        for term in self.vocabulary:
            tf_value = tf.get(term, 0)
            idf_value = self.get_idf(term)
            tfidf = tf_value * idf_value
            
            if tfidf > 0:
                vector[term] = tfidf
        
        return vector


# ============================================================================
# STEP 3: COSINE SIMILARITY CALCULATION
# ============================================================================

def cosine_similarity(vector1, vector2):
    """
    Measures the angular alignment between two vectors.
    Returns score between 0 (orthogonal) and 1 (perfectly aligned).
    """
    
    # Calculate dot product
    dot_product = 0
    for term in vector1:
        if term in vector2:
            dot_product += vector1[term] * vector2[term]
    
    # Calculate magnitudes
    magnitude1 = math.sqrt(sum(val ** 2 for val in vector1.values()))
    magnitude2 = math.sqrt(sum(val ** 2 for val in vector2.values()))
    
    # Avoid division by zero
    if magnitude1 == 0 or magnitude2 == 0:
        return 0
    
    # Cosine similarity formula
    similarity = dot_product / (magnitude1 * magnitude2)
    return similarity


# ============================================================================
# STEP 4: 4-STEP RECOMMENDATION PIPELINE
# ============================================================================

class RecommendationEngine:
    """
    4-Step Pipeline:
    1. Ingestion: Capture user profile
    2. Scoring: Calculate similarity scores
    3. Sorting: Rank by relevance
    4. Filtering: Return Top-N results
    """
    
    def __init__(self):
        self.vectorizer = TFIDFVectorizer()
        self._train_vectorizer()
    
    def _train_vectorizer(self):
        """Train TF-IDF vectorizer on all job role skills"""
        all_skills = [role["skills"] for role in JOB_ROLES.values()]
        self.vectorizer.fit(all_skills)
    
    def recommend(self, user_skills, top_n=3):
        """
        Main recommendation function implementing the complete pipeline.
        
        Args:
            user_skills: List of user's skills (minimum 3)
            top_n: Number of top recommendations to return
        
        Returns:
            List of tuples (job_role, similarity_score, description)
        """
        
        # Validate input
        if len(user_skills) < 3:
            return {"error": "Please provide at least 3 skills", "recommendations": []}
        
        # STEP 1: INGESTION - Create user profile vector
        print("\n" + "="*70)
        print("STEP 1: INGESTION (User Profile)")
        print("="*70)
        print(f"User Skills: {user_skills}")
        user_vector = self.vectorizer.vectorize(user_skills)
        print(f"✓ User profile vectorized with {len(user_vector)} dimensions")
        
        # STEP 2: SCORING - Calculate similarity with each job role
        print("\n" + "="*70)
        print("STEP 2: SCORING (Cosine Similarity)")
        print("="*70)
        
        scores = []
        for job_role, role_data in JOB_ROLES.items():
            role_vector = self.vectorizer.vectorize(role_data["skills"])
            similarity = cosine_similarity(user_vector, role_vector)
            scores.append({
                "role": job_role,
                "score": similarity,
                "description": role_data["description"],
                "skills": role_data["skills"]
            })
            print(f"{job_role:.<35} {similarity:.4f} (score)")
        
        # STEP 3: SORTING - Sort by similarity score (descending)
        print("\n" + "="*70)
        print("STEP 3: SORTING (Descending Order)")
        print("="*70)
        
        sorted_scores = sorted(scores, key=lambda x: x["score"], reverse=True)
        for i, item in enumerate(sorted_scores, 1):
            print(f"{i}. {item['role']:.<35} {item['score']:.4f}")
        
        # STEP 4: FILTERING - Return only top N results
        print("\n" + "="*70)
        print(f"STEP 4: FILTERING (Top-{top_n})")
        print("="*70)
        
        top_recommendations = sorted_scores[:top_n]
        
        return {
            "user_skills": user_skills,
            "recommendations": [
                {
                    "rank": i + 1,
                    "role": item["role"],
                    "match_score": round(item["score"] * 100, 2),
                    "description": item["description"],
                    "relevant_skills": item["skills"]
                }
                for i, item in enumerate(top_recommendations)
            ]
        }


# ============================================================================
# STEP 5: COLD START PROBLEM SOLUTIONS
# ============================================================================

def get_trending_roles():
    """Fallback: Return globally trending job roles"""
    return ["Data Scientist", "DevOps Engineer", "Cloud Architect"]


def get_metadata_inference(user_skills):
    """Infer initial feature weightings from skill keywords"""
    inference = {}
    
    cloud_keywords = ["AWS", "Cloud", "Kubernetes", "Docker"]
    ml_keywords = ["Machine Learning", "Python", "TensorFlow", "Deep Learning"]
    backend_keywords = ["Java", "APIs", "Microservices", "Database"]
    
    if any(skill in user_skills for skill in cloud_keywords):
        inference["cloud_affinity"] = True
    if any(skill in user_skills for skill in ml_keywords):
        inference["ml_affinity"] = True
    if any(skill in user_skills for skill in backend_keywords):
        inference["backend_affinity"] = True
    
    return inference


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Run the Tech Stack Recommender with example user input"""
    
    print("\n")
    print("╔" + "═"*68 + "╗")
    print("║" + " "*15 + "TECH STACK RECOMMENDER SYSTEM" + " "*24 + "║")
    print("║" + " "*12 + "Project 3: AI Recommendation Logic" + " "*21 + "║")
    print("║" + " "*26 + "Powered by DecodeLabs" + " "*21 + "║")
    print("╚" + "═"*68 + "╝")
    
    # Initialize engine
    engine = RecommendationEngine()
    
    # Example 1: User with Cloud & DevOps skills
    print("\n\n" + "▼"*70)
    print("EXAMPLE 1: Cloud & DevOps Skills")
    print("▼"*70)
    user_skills_1 = ["Python", "Cloud Computing", "Docker"]
    result_1 = engine.recommend(user_skills_1, top_n=3)
    
    print("\n" + "─"*70)
    print("📊 FINAL RECOMMENDATIONS")
    print("─"*70)
    for rec in result_1["recommendations"]:
        print(f"\n#{rec['rank']} 🎯 {rec['role']}")
        print(f"   Match Score: {rec['match_score']}%")
        print(f"   Description: {rec['description']}")
        print(f"   Key Skills: {', '.join(rec['relevant_skills'][:3])}...")
    
    # Example 2: User with ML & Data Analysis skills
    print("\n\n" + "▼"*70)
    print("EXAMPLE 2: Machine Learning & Data Skills")
    print("▼"*70)
    user_skills_2 = ["Python", "Machine Learning", "Data Analysis"]
    result_2 = engine.recommend(user_skills_2, top_n=3)
    
    print("\n" + "─"*70)
    print("📊 FINAL RECOMMENDATIONS")
    print("─"*70)
    for rec in result_2["recommendations"]:
        print(f"\n#{rec['rank']} 🎯 {rec['role']}")
        print(f"   Match Score: {rec['match_score']}%")
        print(f"   Description: {rec['description']}")
        print(f"   Key Skills: {', '.join(rec['relevant_skills'][:3])}...")
    
    # Example 3: User with Backend Development skills
    print("\n\n" + "▼"*70)
    print("EXAMPLE 3: Backend Development Skills")
    print("▼"*70)
    user_skills_3 = ["Java", "SQL", "APIs"]
    result_3 = engine.recommend(user_skills_3, top_n=3)
    
    print("\n" + "─"*70)
    print("📊 FINAL RECOMMENDATIONS")
    print("─"*70)
    for rec in result_3["recommendations"]:
        print(f"\n#{rec['rank']} 🎯 {rec['role']}")
        print(f"   Match Score: {rec['match_score']}%")
        print(f"   Description: {rec['description']}")
        print(f"   Key Skills: {', '.join(rec['relevant_skills'][:3])}...")
    
    # Cold Start Problem Demo
    print("\n\n" + "▼"*70)
    print("COLD START PROBLEM - Solutions")
    print("▼"*70)
    print(f"\n🔄 Trending Fallback: {get_trending_roles()}")
    print(f"📍 Metadata Inference: {get_metadata_inference(user_skills_2)}")
    
    print("\n" + "="*70)
    print("✓ Recommendation pipeline completed successfully!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
