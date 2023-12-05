import numpy as np

from utils import get_faces, split_train_test


faces = get_faces(zipfile_path="./Dataset.zip")
training_set, testing_set = split_train_test(zipfilepath="./Dataset.zip")

img_array =list (training_set.values())[0]


num_persons = 41
trn_pic_num = 8
tst_pic_num = 2
num_trn = num_persons*trn_pic_num
num_tst = num_persons*tst_pic_num


imagetst = testing_set.values()


facematrix = []
facelabel = []
for key, val in training_set.items():
    facematrix.append(val.flatten())
    facelabel.append(key.split("/")[0])
facematrix = np.array(facematrix)

degree = 2
K = (np.dot(facematrix, facematrix.T)/num_trn+1)**degree  



one_N_trn = np.ones([num_trn, num_trn])/num_trn
K = K - np.dot(one_N_trn, K) - np.dot(K, one_N_trn) + \
    np.dot(one_N_trn, np.dot(K, one_N_trn))

eigen_values, eigen_vectors = np.linalg.eig(K)


for col in range(eigen_vectors.shape[1]):
    eigen_vectors[:, col] = eigen_vectors[:, col]/np.sqrt(eigen_values[col])

n = 50
eigfaces = eigen_vectors[:,0:n]
print(eigfaces.shape, eigen_vectors.shape)

W = np.dot(K.T, eigfaces)



for img in testing_set:
    query = faces[img].reshape(1, -1)

    one_N_tst = np.ones([num_tst, num_trn])/num_trn
    Ktest = (np.dot(query, facematrix.T)/num_trn+1)**degree
    Ktest = Ktest - np.dot(one_N_tst, K) - np.dot(Ktest, one_N_trn) + \
        np.dot(one_N_tst, np.dot(K, one_N_trn))
    W_tst = np.dot(Ktest, eigfaces)
    print(W_tst.shape, W.shape)
    


    euclidean_distance = np.linalg.norm(W - W_tst, axis=0)
    best_match = np.argmin(euclidean_distance)
    print(best_match)
