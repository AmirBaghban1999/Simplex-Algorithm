# -*- coding: utf-8 -*-
"""
Created on Sun Dec  6 21:42:42 2020

@author: Amir
"""

"""Note: this program works only when we are sure about the existence of bounded solution"""

"""Suppose we are given the linear problem and the intial solution of the problem"""


"""
IB is the set of basis indices

B is the set of bases columns

AX=b is the constraints

IB is the index of basis columns in A

IN is the index of non-basis column in A

C is the cost function's coefficients

A is the constraints coefficients

b is the right hand side

"""

import numpy as np
from inverseMatrix import inversematrix
np.set_printoptions(suppress=True)



                      

def simplex(A,C,b,IB,IN):
    n=len(IB)
    m=len(A[0,:])
    B=np.zeros((n,n))
    N=np.zeros((n,n))
    for i in range(n):
        B[:,i]=A[:,IB[i]]
    Binverse=inversematrix(B)
    CN=[]
    CB=[]
    for i in range(m-n):
        CN.append(C[IN[i]])
    for i in range(n):
        CB.append(C[IB[i]])
    for i in range(m-n):
        N[:,i]=A[:,IN[i]]
    CN=np.transpose(CN)-np.transpose(CB).dot(Binverse.dot(N)) 
    for i in range(m):
        if i in IB:
            C[i]=0
        else:
            C[i]=CN[IN.index(i)]
    
    
    negative=[]
    for i in range(m):
        if C[i]<0:
            negative.append(C[i])
    A=Binverse.dot(A)
    b=Binverse.dot(b)
    if len(negative)==0:
        return IB , b
    else:
        while len(negative)>0: 
            
            

            enter=C.index(negative[0])
            entercolumn=A[:,enter]
            if all(entercolumn[i]<=0 for i in range(n)):
                return "The problem is unbounded"
            else:
                minselectingvector=[]
                for i,j in zip(b,entercolumn):
                    if j>0:
                        minselectingvector.append(i/j )
                        
                minvalue=min(minselectingvector)
                b=list(b)
                for i,j in zip(b,entercolumn):
                    if i==j*minvalue:
                        exitindex=b.index(i)
                        break
                
                s=IB[exitindex]
                IB[exitindex]=enter
                r=IN.index(enter)
                IN[r]=s
                for i in range(n):
                    CB[i]=C[IB[i]]
                for i in range(m-n):
                    CN[i]=C[IN[i]] 
                for i in range(n):
                    B[:,i]=A[:,IB[i]]
                for i in range(m-n):
                    N[:,i]=A[:,IN[i]]
                Binverse=inversematrix(B)
                A=Binverse.dot(A)
                b=Binverse.dot(b)
                CN=np.transpose(CN)-np.transpose(CB).dot(Binverse.dot(N))
                for i in range(m):
                    if i in IB:
                        C[i]=0
                    else:
                        C[i]=CN[IN.index(i)]
                negative=[]
                for i in range(m):
                    if C[i]<0:
                        negative.append(C[i])
                
        return IB, b     
                        
                        
                



"""Example:"""


A=np.array([[2, 3,1,0],[2, 1,0,1]])

"""
C contains the objective functions coeficients. If the objective function is of the form o=c1x1+c2x2 the C=[-c1,-c2]

The problems constraint should be equalities
"""
C=[-3,-2,0,0]  
b=[12,8]
IB=[2,3]
IN=[0, 1]
F=simplex(A,C,b,IB,IN)

print(F)

  




