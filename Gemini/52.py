import numpy as np
from itertools import combinations

class ConvexHull4D:
    

    def __init__(self, points):
        
        self.points = np.asanyarray(points)
        if self.points.shape[1] != 4:
            raise ValueError("ConvexHull4D requires points in 4-dimensional space.")
        self.num_points = self.points.shape[0]
        self.facets = []  

    def _get_signed_volume(self, facet_indices, point_idx):
        
        pts = self.points[list(facet_indices)]
        test_pt = self.points[point_idx]
        
        
        matrix = np.ones((5, 5))
        matrix[0:4, 0:4] = pts
        matrix[4, 0:4] = test_pt
        
        return np.linalg.det(matrix)

    def _find_initial_simplex(self):
        
        for indices in combinations(range(self.num_points), 5):
            
            matrix = np.ones((5, 5))
            matrix[:, 0:4] = self.points[list(indices)]
            if abs(np.linalg.det(matrix)) > 1e-9:
                return list(indices)
        raise ValueError("Degenerate data: No non-degenerate 4-simplex found.")

    def compute(self):
        
        if self.num_points < 5:
            raise ValueError("At least 5 points are required for a 4D convex hull.")

        initial_indices = self._find_initial_simplex()
        point_mask = np.ones(self.num_points, dtype=bool)
        point_mask[initial_indices] = False

        
        
        centroid = np.mean(self.points[initial_indices], axis=0)
        self.points = np.vstack([self.points, centroid])
        centroid_idx = self.num_points
        
        for i in range(5):
            facet = [initial_indices[j] for j in range(5) if j != i]
            
            if self._get_signed_volume(facet, centroid_idx) > 0:
                facet[0], facet[1] = facet[1], facet[0]
            self.facets.append(tuple(facet))

        
        for i in range(self.num_points):
            if not point_mask[i]:
                continue

            visible_facets = []
            for facet in self.facets:
                if self._get_signed_volume(facet, i) > 1e-9:
                    visible_facets.append(facet)

            if not visible_facets:
                continue

            
            ridge_counts = {}
            for facet in visible_facets:
                
                for ridge in combinations(facet, 3):
                    
                    r_key = tuple(sorted(ridge))
                    ridge_counts[r_key] = ridge_counts.get(r_key, 0) + 1

            horizon_ridges = [ridge for ridge, count in ridge_counts.items() if count == 1]

            
            self.facets = [f for f in self.facets if f not in visible_facets]

            
            for ridge in horizon_ridges:
                new_facet = list(ridge) + [i]
                
                if self._get_signed_volume(new_facet, centroid_idx) > 0:
                    new_facet[0], new_facet[1] = new_facet[1], new_facet[0]
                self.facets.append(tuple(new_facet))

        
        self.points = self.points[:-1]
        return self.facets

def main():
    
    np.random.seed(42)
    sample_points = np.random.rand(15, 4)
    
    hull_solver = ConvexHull4D(sample_points)
    facets = hull_solver.compute()
    
    print(f"Computed Convex Hull with {len(facets)} facets.")
    for idx, facet in enumerate(facets):
        print(f"Facet {idx}: Indices {facet}")

if __name__ == "__main__":
    main()