import numpy as np

class Facet4D:
    
    def __init__(self, vertex_indices, points, internal_point):
        self.indices = list(vertex_indices)
        self.points = points
        
        self.normal, self.offset = self._compute_hyperplane(internal_point)

    def _compute_hyperplane(self, internal_point):
        
        
        v1 = self.points[self.indices[1]] - self.points[self.indices[0]]
        v2 = self.points[self.indices[2]] - self.points[self.indices[0]]
        v3 = self.points[self.indices[3]] - self.points[self.indices[0]]
        
        
        mat = np.vstack([v1, v2, v3])
        normal = np.zeros(4)
        for i in range(4):
            
            minor = np.delete(mat, i, axis=1)
            normal[i] = ((-1)**i) * np.linalg.det(minor)
        
        
        norm = np.linalg.norm(normal)
        if norm > 1e-12:
            normal /= norm
            
        offset = np.dot(normal, self.points[self.indices[0]])
        
        
        
        if np.dot(normal, internal_point) - offset > 0:
            normal = -normal
            offset = -offset
            
        return normal, offset

    def can_see(self, point):
        
        return np.dot(self.normal, point) - self.offset > 1e-9

class ConvexHull4D:
    
    def __init__(self, points):
        self.points = np.asarray(points)
        self.facets = []

    def _find_initial_simplex(self):
        
        n_points = self.points.shape[0]
        if n_points < 5:
            raise ValueError("4D Convex Hull requires at least 5 points.")
        
        indices = [0]
        
        for i in range(1, n_points):
            current_dim = len(indices)
            base_pt = self.points[indices[0]]
            vectors = [self.points[idx] - base_pt for idx in indices[1:]]
            vectors.append(self.points[i] - base_pt)
            
            if np.linalg.matrix_rank(vectors) == current_dim:
                indices.append(i)
            
            if len(indices) == 5:
                return indices
        
        raise ValueError("Point set is degenerate (lies in a subspace of dimension < 4).")

    def compute(self):
        
        simplex_indices = self._find_initial_simplex()
        
        internal_point = np.mean(self.points[simplex_indices], axis=0)
        
        
        for i in range(5):
            facet_verts = [simplex_indices[j] for j in range(5) if j != i]
            self.facets.append(Facet4D(facet_verts, self.points, internal_point))
            
        processed_indices = set(simplex_indices)
        
        for i in range(self.points.shape[0]):
            if i in processed_indices:
                continue
            
            p = self.points[i]
            
            visible_facets = [f for f in self.facets if f.can_see(p)]
            
            if not visible_facets:
                