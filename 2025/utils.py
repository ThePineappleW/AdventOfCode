class Window:
  
  @staticmethod
  def slide_centered(arr, shape):
    """
    Yields a sliding window centered on each element of the array.
    The window will have maximum size equal to self.shape,
    but the size will be smaller around the edges. 
    """
    assert shape[0] % 2 != 0
    assert shape[1] % 2 != 0
    
    row_offset = shape[0] // 2
    col_offset = shape[1] // 2
    n = len(arr)
    m = len(arr[0])
    for i in range(n):
      upper_row = max(0, i - row_offset)
      lower_row = min(n, i + row_offset)
      rows = arr[upper_row : lower_row + 1]
      for j in range(m):
        left_col = max(0, j - col_offset)
        right_col = min(m, j + col_offset)
        
        yield [row[left_col : right_col + 1] for row in rows]
