# Where Cosine Similarity is Used in This Project

## Overview
Cosine similarity is the **core algorithm** that powers the movie recommendation system. It's used in **two main places**:

---

## 1. **CALCULATION PHASE** (In the Notebook)
**Location:** `notebook86c26b4f17.ipynb` - Cell 32-33

### Step-by-Step Process:

#### Step 1: Import the Function
```python
from sklearn.metrics.pairwise import cosine_similarity
```

#### Step 2: Calculate Similarity Matrix
```python
similarity = cosine_similarity(vector)
```

**What happens here:**
- `vector` is a **4806 x 5000** matrix (4806 movies, 5000 features)
- Each movie is represented as a vector of features (genres, keywords, cast, crew, overview)
- `cosine_similarity()` calculates similarity between **every pair of movies**
- Result: A **4806 x 4806** similarity matrix
  - Each cell `[i][j]` contains similarity score between movie `i` and movie `j`
  - Values range from **0 to 1**:
    - **1.0** = Identical movies (same features)
    - **0.0** = Completely different movies
    - **0.5-0.9** = Similar movies

#### Step 3: Save the Result
```python
pickle.dump(similarity, open('similarity.pkl', 'wb'))
```
- The similarity matrix is saved to `similarity.pkl`
- This is a **one-time calculation** (takes time, so it's pre-computed)

---

## 2. **USAGE PHASE** (In the App)
**Location:** `app.py` - Lines 29-31, 48

### Step 1: Load Pre-calculated Similarity
```python
similarity = pickle.load(open('similarity.pkl','rb'))
```
- Loads the pre-calculated similarity matrix (fast!)

### Step 2: Use in Recommendation Function
```python
def recommend(movie):
    # Find the index of the selected movie
    index = movies[movies['title'] == movie].index[0]
    
    # Get similarity scores for this movie with all other movies
    distances = sorted(list(enumerate(similarity[index])), 
                      reverse=True, key=lambda x: x[1])
    
    # Get top 5 most similar movies (skip index 0, which is the movie itself)
    for i in distances[1:6]:
        # Get recommended movie details
        ...
```

**What happens here:**
1. **Find movie index**: Gets the row number of the selected movie
2. **Extract similarity row**: `similarity[index]` gives similarity scores with all 4806 movies
3. **Sort by similarity**: Sorts from highest to lowest similarity
4. **Get top 5**: Takes movies at positions 1-5 (skips position 0, which is the movie itself with similarity = 1.0)

---

## Visual Explanation

### During Calculation (Notebook):
```
Movie Vectors (4806 movies × 5000 features)
         ↓
cosine_similarity(vector)
         ↓
Similarity Matrix (4806 × 4806)
    Movie1  Movie2  Movie3  ...
Movie1  1.0    0.65   0.42   ...
Movie2  0.65   1.0    0.78   ...
Movie3  0.42   0.78   1.0    ...
...
         ↓
Saved to similarity.pkl
```

### During Usage (App):
```
User selects: "The Dark Knight"
         ↓
Find index: 744
         ↓
Get row 744 from similarity matrix
         ↓
Sort by similarity scores
         ↓
Top 5 similar movies:
1. Batman Begins (0.89)
2. The Dark Knight Rises (0.87)
3. Inception (0.72)
4. Interstellar (0.68)
5. The Prestige (0.65)
```

---

## Why Cosine Similarity?

### Advantages:
1. **Measures angle, not distance**: Good for high-dimensional data
2. **Normalized**: Values between 0 and 1 (easy to interpret)
3. **Works with sparse data**: Handles movies with different numbers of features
4. **Content-based**: Finds movies with similar content, not just popular ones

### How It Works:
```
Cosine Similarity = (A · B) / (||A|| × ||B||)

Where:
- A · B = Dot product of movie vectors
- ||A|| = Magnitude of movie A's vector
- ||B|| = Magnitude of movie B's vector

Result: Angle between two vectors (0° = identical, 90° = different)
```

---

## Code Locations Summary

| Phase | File | Line/Cell | What It Does |
|-------|------|-----------|--------------|
| **Import** | `notebook86c26b4f17.ipynb` | Cell 32 | Imports cosine_similarity function |
| **Calculate** | `notebook86c26b4f17.ipynb` | Cell 33 | Calculates similarity matrix |
| **Save** | `notebook86c26b4f17.ipynb` | Cell 39 | Saves to similarity.pkl |
| **Load** | `app.py` | Line 48 | Loads pre-calculated matrix |
| **Use** | `app.py` | Line 31 | Uses similarity scores for recommendations |

---

## Example Flow

**User selects "Gandhi" (index 123):**

1. **Load similarity matrix** → `similarity[123]` gives array of 4806 similarity scores
2. **Sort scores** → Highest similarity first
3. **Get top 5** → Movies with highest similarity to "Gandhi"
4. **Result** → Shows: "Gandhi, My Father", "The Wind That Shakes the Barley", etc.

---

## Key Points

✅ **Calculated once** in the notebook (saves time)
✅ **Used every time** a user requests recommendations
✅ **Pre-computed** similarity matrix is loaded instantly
✅ **4806 × 4806 matrix** = ~23 million similarity scores pre-calculated
✅ **Fast recommendations** because similarity is already calculated

---

## Summary

**Cosine Similarity is used:**
1. **Once** - To calculate similarity between all movie pairs (in notebook)
2. **Every time** - To find similar movies when user clicks "Show Recommendation" (in app)

The similarity matrix is the **brain** of the recommendation system! 🧠

