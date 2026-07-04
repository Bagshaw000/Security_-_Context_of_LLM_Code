import numpy as np

def get_ridges(facet):
    
    f = list(facet)
    return [tuple(sorted(f[:i] + f[i+1:])) for i in range(len(f))]

def is_visible(points, facet_indices, test_point, internal_point):
    
    facet_pts = points[list(facet_indices)]
    
    
    mat_base = np.ones((5, 5))
    mat_base[:4, :4] = facet_pts
    
    
    mat_test = np.copy(mat_base)
    mat_test[4, :4] = test_point
    det_test = np.linalg.det(mat_test)
    
    
    mat_internal = np.copy(mat_base)
    mat_internal[4, :4] = internal_point
    det_internal = np.linalg.det(mat_internal)
    
    
    return det_test * det_internal < -1e-9

def get_initial_simplex(points):
    
    n = points.shape[0]
    if n < 5:
        raise ValueError("At least 5 points are required for a 4D convex hull.")
    
    for i in range(n - 4):
        for j in range(i + 1, n - 3):
            for k in range(j + 1, n - 2):
                for l in range(k + 1, n - 1):
                    for m in range(l + 1, n):
                        indices = [i, j, k, l, m]
                        mat = np.ones((5, 5))
                        mat[:, :4] = points[indices]
                        if abs(np.linalg.det(mat)) > 1e-9:
                            return indices
    raise ValueError("No non-degenerate 4-simplex found. Points might be coplanar.")

def convex_hull_4d(points):
    
    points = np.array(points)
    n_points, dim = points.shape
    if dim != 4:
        raise ValueError("Input points must be 4D.")

    
    simplex_indices = get_initial_simplex(points)
    
    
    facets = set()
    for i in range(5):
        facet = tuple(sorted([simplex_indices[j] for j in range(5) if j != i]))
        facets.add(facet)
    
    
    internal_point = np.mean(points[simplex_indices], axis=0)
    
    
    processed_indices = set(simplex_indices)
    for i in range(n_points):
        if i in processed_indices:
            continue
            
        p = points[i]
        
        
        visible_facets = []
        for facet in facets:
            if is_visible(points, facet, p, internal_point):
                visible_facets.append(facet)
        
        if not visible_facets:
            continue
            
        
        ridge_counts = {}
        for facet in visible_facets:
            for ridge in get_ridges(facet):
                ridge_counts[ridge] = ridge_counts.get(ridge, 0) + 1
        
        horizon_ridges = [ridge for ridge, count in ridge_counts.items() if count == 1]
        
        
        for facet in visible_facets:
            facets.remove(facet)
            
        
        for ridge in horizon_ridges:
            new_facet = tuple(sorted(list(ridge) + [i]))
            facets.add(new_facet)
            
        
        processed_indices.add(i)

    return list(facets)

def test_hull():
    
    
    from itertools import product
    tesseract_vertices = np.array(list(product([-1, 1], repeat=4)))
    
    
    points = np.vstack([tesseract_vertices, [0, 0, 0, 0]])
    
    try:
        facets = convex_hull_4d(points)
        print(f"Successfully computed 4D hull with {len(facets)} facets.")
        
        
        
        
        
        assert len(facets) > 0
        
        
        for facet in facets:
            assert 16 not in facet
        print("Test passed: Interior point excluded and facets generated.")
        
    except Exception as e:
        print(f"Test failed: {e}")

if __name__ == "__main__":
    
    
    np.random.seed(42)
    random_points = np.random.rand(20, 