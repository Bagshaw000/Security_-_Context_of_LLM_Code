import numpy as np
from typing import List, Tuple, Set

class Facet4D:
    
    def __init__(self, vertex_indices: Tuple[int, int, int, int]):
        
        self.vertices = tuple(sorted(vertex_indices))
        
        self.ridges = [
            tuple(sorted((self.vertices[0], self.vertices[1], self.vertices[2]))),
            tuple(sorted((self.vertices[0], self.vertices[1], self.vertices[3]))),
            tuple(sorted((self.vertices[0], self.vertices[2], self.vertices[3]))),
            tuple(sorted((self.vertices[1], self.vertices[2], self.vertices[3])))
        ]

class ConvexHull4D:
    
    def __init__(self, points: np.ndarray):
        if points.shape[1] != 4:
            raise ValueError("Points must be 4-dimensional.")
        self.points = points
        self.num_points = len(points)
        self.facets: List[Facet4D] = []

    def _get_signed_dist(self, facet_indices: Tuple[int, int, int, int], p_idx: int) -> float:
        
        indices = list(facet_indices) + [p_idx]
        matrix = np.column_stack((self.points[indices], np.ones(5)))
        return np.linalg.det(matrix)

    def _find_initial_simplex(self) -> List[int]:
        
        if self.num_points < 5:
            raise ValueError("Need at least 5 points for a 4D hull.")
        
        indices = [0, 1, 2, 3]
        for i in range(4, self.num_points):
            test_indices = indices + [i]
            if abs(self._get_determinant(test_indices)) > 1e-9:
                return test_indices
        raise ValueError("Points are coplanar in a 3D subspace.")

    def _get_determinant(self, indices: List[int]) -> float:
        matrix = np.column_stack((self.points[indices], np.ones(5)))
        return np.linalg.det(matrix)

    def compute(self) -> List[Tuple[int, int, int, int]]:
        
        initial_indices = self._find_initial_simplex()
        used_points = set(initial_indices)

        
        for i in range(5):
            facet_verts = tuple(initial_indices[:i] + initial_indices[i+1:])
            
            other_point = initial_indices[i]
            if self._get_signed_dist(facet_verts, other_point) > 0:
                
                facet_verts = (facet_verts[1], facet_verts[0], facet_verts[2], facet_verts[3])
            self.facets.append(Facet4D(facet_verts))

        
        for i in range(self.num_points):
            if i in used_points:
                continue
            
            visible_facets = []
            for facet in self.facets:
                
                if self._get_signed_dist(facet.vertices, i) > 1e-9:
                    visible_facets.append(facet)

            if not visible_facets:
                continue

            
            ridge_counts = {}
            for f in visible_facets:
                for ridge in f.ridges:
                    ridge_counts[ridge] = ridge_counts.get(ridge, 0) + 1

            horizon_ridges = [ridge for ridge, count in ridge_counts.items() if count == 1]

            
            self.facets = [f for f in self.facets if f not in visible_facets]

            
            for ridge in horizon_ridges:
                new_facet_indices = ridge + (i,)
                
                
                
                self.facets.append(Facet4D(new_facet_indices))

        return [f.vertices for f in self.facets]

def main():
    
    
    np.random.seed(42)
    points = np.random.rand(15, 4)

    hull_engine = ConvexHull4D(points)
    try:
        hull_facets = hull_engine.compute()
        print(f"Successfully computed 4D Convex Hull.")
        print(f"Number of facets: {len(hull_facets)}")
        for idx, facet in enumerate(hull_facets):
            print(f"Facet {idx}: Indices {facet}")
    except ValueError as e:
        print(f"Error computing hull: {e}")

if __name__ == "__main__":
    main()