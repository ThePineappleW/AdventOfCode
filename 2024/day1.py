import pandas as pd
import numpy as np

# Part 1:

def total_distances(df: pd.DataFrame) -> np.int64:
    """
    Sort the input lists and sum the distances.
    
    params:
        df: Has a column for each input list.
    """
    return df.transform(np.sort).diff(axis=1).abs().iloc[:,-1].sum()

# Part 2:

def total_similarity_score(df: pd.DataFrame) -> np.int64:
    """
    Compute the similarity scores for each item in the first column, 
    based on frequency in the second column, and return the sum.
    
    params:
        df: Has two columns, `A` and `B`.
    """
    freqs = df['B'].value_counts()
    return df['A'].apply(lambda v: v * freqs.get(v, 0)).sum()


def read_input(filepath: str) -> pd.DataFrame:
    """Helper for running the final test"""
    return pd.read_csv(filepath, sep='   ', names=['A', 'B'])
     
 # Tests
df_test = pd.DataFrame({
    'A': [3,4,2,1,3,3], 
    'B': [4,3,5,3,9,3]
})
    
def test_part_1():
    assert total_distances(df_test) == 11
    
def test_part_2():
    assert total_similarity_score(df_test) == 31