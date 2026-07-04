import pandas as pd

df = pd.DataFrame({
    'Patient ID': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    'age': [30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40],
    'sex': ['M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F'],
    'procedure type': ['Surgery', 'Surgery', 'Surgery', 'Surgery', 'Surgery', 'Surgery', 'Surgery', 'Surgery', 'Surgery', 'Surgery', 'Surgery', 'Surgery', 'Surgery', 'Surgery', 'Surgery', 'Surgery', 'Surgery', 'Surgery', 'Surgery', 'Surgery'],
    'Hour 1': [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209],
    'Hour 2': [110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219],
    'Hour 3': [120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229],
    'Hour 4': [130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239],
    'Hour 5': [140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249],
    'Hour 6': [150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259],
    'Hour 7': [160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269],
    'Hour 8': [170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279],
    'Hour 9': [180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289],
    'Hour 10': [190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 290, 291, 292, 293, 294, 295, 296, 297, 298, 299]
})

long_df = pd.DataFrame(columns=['Patient ID', 'Time since surgery', 'age', 'sex', 'procedure type', 'value'])

for patient in df['Patient ID'].unique():
    patient_df = df[df['Patient ID'] == patient]
    for hour in range(1, 11):
        time_since_surgery = f'Hour {hour}'
        patient_df[time_since_surgery] = patient_df[f'Hour {hour}']
        long_df = long_df.append({
            'Patient ID': patient,
            'Time since surgery': time_since_surgery,
            'age': patient_df['age'].iloc[0],
            'sex': patient_df['sex'].iloc[0],
            'procedure type': patient_df['procedure type'].iloc[0],
            'value': patient_df[f'Hour {hour}']
        }, ignore_index=True)