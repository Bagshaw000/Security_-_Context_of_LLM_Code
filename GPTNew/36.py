def generate_shapes(n):
    if n == 1:
        return [((0, 0),)]
    elif n == 2:
        return [((0, 0), (1, 0))]
    elif n == 3:
        return [((0, 0), (1, 0), (2, 0)), ((0, 0), (1, 0), (1, 1))]
    elif n == 4:
        return [((0, 0), (1, 0), (2, 0), (3, 0)), 
                ((0, 0), (1, 0), (1, 1), (1, 2)), 
                ((0, 0), (1, 0), (0, 1), (1, 1))]
    elif n == 5:
        return [((0, 0), (1, 0), (2, 0), (3, 0), (4, 0)), 
                ((0, 0), (1, 0), (1, 1), (1, 2), (2, 2)), 
                ((0, 0), (1, 0), (0, 1), (1, 1), (1, 2))]
    return []

def rotate(shape):
    return tuple((y, -x) for x, y in shape)

def flip(shape):
    return tuple((-x, y) for x, y in shape)

def unique_shapes(shapes):
    unique = set()
    for shape in shapes:
        transformations = {shape}
        for _ in range(3):
            shape = rotate(shape)
            transformations.add(shape)
            transformations.add(flip(shape))
        unique.update(transformations)
    return unique

def count_unique_shapes(n):
    all_shapes = generate_shapes(n)
    unique = unique_shapes(all_shapes)
    return len(unique)

def main():
    try:
        n = int(input("Enter the number of squares (1-5): "))
        if n < 1 or n > 5:
            raise ValueError("Input must be between 1 and 5.")
        unique_count = count_unique_shapes(n)
        print(f"Number of unique {n}-square pieces: {unique_count}")
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()