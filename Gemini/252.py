


import numpy as np  



def grading_curve(x):
    return 1 / (1 + np.exp(-x))


def calculate_improvement(x):
    return x * (1 - x)





student_data = np.array([[0,0,1], 
                         [0,1,1], 
                         [1,0,1], 
                         [1,1,1]])

actual_results = np.array([[0], [1], [1], [0]])





np.random.seed(1)
importance_stage1 = 2 * np.random.random((3, 5)) - 1
importance_stage2 = 2 * np.random.random((5, 5)) - 1
importance_stage3 = 2 * np.random.random((5, 1)) - 1



for practice_round in range(60000):
    
    
    
    stage0 = student_data
    stage1 = grading_curve(np.dot(stage0, importance_stage1))
    stage2 = grading_curve(np.dot(stage1, importance_stage2))
    stage3 = grading_curve(np.dot(stage2, importance_stage3))

    
    error = actual_results - stage3

    
    
    
    correction3 = error * calculate_improvement(stage3)
    correction2 = correction3.dot(importance_stage3.T) * calculate_improvement(stage2)
    correction1 = correction2.dot(importance_stage2.T) * calculate_improvement(stage1)

    
    importance_stage3 += stage2.T.dot(correction3)
    importance_stage2 += stage1.T.dot(correction2)
    importance_stage1 += stage0.T.dot(correction1)




print("The computer has finished learning. Here are its final predictions:")
print(stage3)