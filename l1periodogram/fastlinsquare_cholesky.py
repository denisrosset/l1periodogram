# Copyright 2020 Nathan Hara
import numpy as np

def fastchi2lin(A,W2,y,check_invertibility = True,
                compute_covar=True, full_chi2 = False):
    
    B = A.T.dot(W2)
    G = B.dot(A)
    set_to_zero = False
    
    if check_invertibility:
        condn = np.linalg.cond(G)
        if condn>1e13:
            set_to_zero = True 
#    try:
#
#    except:
#       set_to_zero = True 
     
    if not set_to_zero:
        b = B.dot(y)
        L = np.linalg.cholesky(G)  
        u = np.linalg.solve(L,b)  
        v = np.linalg.solve(L.T,u) 
        chi2truncated = b.dot(v)
        
        
        if compute_covar:
            invL = np.linalg.inv(L)
            Covariance = invL.T.dot(invL)
        else:
            Covariance = np.nan #G*0+np.inf
        
    else:
        chi2truncated = 0
        v = np.ones(len(G))*np.inf
        Covariance = G*0+np.inf
    
    if full_chi2:
        #print(np.dot(y, W2.dot(y)), chi2truncated)
        chi2truncated = np.dot(y, W2.dot(y)) - chi2truncated
        
    
    return(chi2truncated,v,Covariance)
    
    
    
def fastchi2lin_V(A,V,y, full_chi2 = False):
    
    condn = np.linalg.cond(V)
    
    if condn<1e13:
        Lv = np.linalg.cholesky(V)
        WA = np.linalg.solve(Lv, A)
        G = WA.T.dot(WA)
        condn = np.linalg.cond(G)
    
        if condn<1e13:
            #print('G',condn)
            b = WA.T.dot(y)
            L = np.linalg.cholesky(G)  
            u = np.linalg.solve(L,b)  
            v = np.linalg.solve(L.T,u) 
            chi2truncated = b.dot(v)
            
        else:
            chi2truncated=0 
            v = np.nan
        
        if full_chi2:
            #condn = np.linalg.cond(Lv)
            #if condn>1e-13:
            Wy = np.linalg.solve(Lv, y) 
            chi2truncated = np.dot(Wy, Wy) - chi2truncated
            #else:
            #    chi2truncated = np.nan
                
    else:
        chi2truncated = np.nan
        v = np.nan
    
    return(chi2truncated,v)
    
    
    
    
    
    
    
    
    
    
