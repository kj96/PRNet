import numpy as np


orignal_vertices = "/home/kj/Data/me/OBJ_PRNET/test-1_t1head-mlab.obj"
clean_vertices = "/home/kj/Data/me/OBJ_PRNET/t1head-wo_ears-2.obj"

o_arr = []
n_arr = []

with open(orignal_vertices) as f:
    o_arr = [line.rstrip() for line in f]

with open(clean_vertices) as f:
    n_arr = [line.rstrip() for line in f]

print("# o_arr.len: ", len(o_arr))
print("# n_arr.len: ", len(n_arr))

n_o_arr = []
n_n_arr = []

for o_a in o_arr:
    if 'd ' in o_a:
        n_o_arr.append([o_a])

for n_a in n_arr:
    if 'd ' in n_a:
        n_n_arr.append([n_a])

print("# n_o_arr.len: ", len(n_o_arr))
print("# n_n_arr.len: ", len(n_n_arr))

nix = 0
rix = []

for ix in range (len(n_o_arr) - 1):
    if nix > (len(n_n_arr) - 1):
        print("Face vertices FINISH ", nix)
        break
    if n_o_arr[ix] == n_n_arr[nix]:
        nix += 1
    else:
        rix.append(ix)

print("# nix: ", nix)
print(len(rix))
# print(rix)
np.save(orignal_vertices.replace('.obj', '_face_ind.obj'), rix)


####
# aa = np.loadtxt('/home/kj/DL/MoYo/Dev/Face3D/github/PRNet/Data/uv-data/face_ind.txt')
# bb = np.load('/home/kj/Data/me/OBJ_PRNET/test-1_t1head-mlab_face_ind.npy')

# bb = bb.astype(dtype=float)

# nio = []

# for a in aa:
#     if a not in bb:
#         nio.append(a)

# nio = np.array(a)
# print(nio.shape)
# np.savetxt('/home/kj/DL/MoYo/Dev/Face3D/github/PRNet/Data/uv-data/new_triangles.txt'. nio)