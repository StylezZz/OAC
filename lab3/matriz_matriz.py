import numpy as np
import ctypes

if __name__ == '__main__':
    
    lib = ctypes.CDLL('./lib.so')
    lib.mat_vec.argtypes = [np.ctypeslib.ndpointer(dtype=np.int32),np.ctypeslib.ndpointer(dtype=np.int32),np.ctypeslib.ndpointer(dtype=np.int32), ctypes.c_int]
    lib.mat_vec_block.argtypes = [np.ctypeslib.ndpointer(dtype=np.int32),np.ctypeslib.ndpointer(dtype=np.int32),np.ctypeslib.ndpointer(dtype=np.int32), ctypes.c_int, ctypes.c_int]
    
    N = 
    max_val_mas_1 = 
    A = np.random.randint(max_val_mas_1-1,size =(N,N),dtype =np.int32)
    B = np.random.randint(max_val_mas_1-1,size =(N,N),dtype =np.int32)
    
    C_ref = np.dot(A,B)
    C_mat_vec = np.zeros_like(C_ref, dtype=np.int32)
    C_mat_vec_blocking = np.zeros_like(C_ref, dtype=np.int32)
    
    block = 
    
    A_array = A.flatten()
    B_array = B.flatten()
    C_mat_vec_array = C_mat_vec.flatten()
    C_mat_vec_blocking = C_mat_vec_blocking.flatten()
    
    lib.mat_vec(A_array,B_array,C_mat_vec_array, N)
    lib.mat_vec_block(A_array,B_array,C_mat_vec_blocking, N, block)

    print("Referencia")
    print(C_ref)
    print("Mat_vec")
    print(C_mat_vec_array.reshape(N,N))
    print("Mat_vec_blocking")
    print(C_mat_vec_blocking.reshape(N,N))
    print("Error 1", np.sum(C_ref.flatten()-C_mat_vec_array))
    print("Error 2",np.sum(C_ref.flatten()-C_mat_vec_blocking))
