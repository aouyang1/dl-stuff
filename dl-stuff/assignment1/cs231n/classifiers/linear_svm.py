import numpy as np
from random import shuffle

def svm_loss_naive(W, X, y, reg):
    """
    Structured SVM loss function, naive implementation (with loops).

    Inputs have dimension D, there are C classes, and we operate on minibatches
    of N examples.

    Inputs:
    - W: A numpy array of shape (D, C) containing weights.
    - X: A numpy array of shape (N, D) containing a minibatch of data.
    - y: A numpy array of shape (N,) containing training labels; y[i] = c means
      that X[i] has label c, where 0 <= c < C.
    - reg: (float) regularization strength

    Returns a tuple of:
    - loss as single float
    - gradient with respect to weights W; an array of same shape as W
    """
    dW = np.zeros(W.shape)  # initialize the gradient as zero

    # compute the loss and the gradient
    num_classes = W.shape[1]
    num_train = X.shape[0]
    loss = 0.0
    d_loss = np.zeros(W.shape)
    d_reg = np.zeros(W.shape)
    
    h = 1e-5
    
    for i in xrange(num_train):
            
        scores = X[i].dot(W)
        
        correct_class_score = scores[y[i]]
        for j in xrange(num_classes):
            if j == y[i]:
                continue
                
            margin = scores[j] - correct_class_score + 1  # note delta = 1
            if margin > 0:
                loss += margin
                
        for f in xrange(W.shape[0]):
            for c in xrange(W.shape[1]):
                old_w = W[f,c]
                W[f,c] += h
                
                d_scores = X[i].dot(W)
                
                correct_class_score = d_scores[y[i]]
                for j in xrange(num_classes):
                    if j == y[i]:
                        continue
                        
                    margin = d_scores[j] - correct_class_score + 1
                    if margin > 0:
                        d_loss[f,c] += margin
                
                # do only once
                if i == 0:
                    d_reg[f,c] = np.sum(W * W)
                
                W[f,c] = old_w
        

    # Right now the loss is a sum over all training examples, but we want it
    # to be an average instead so we divide by num_train.
    loss /= num_train
    
    # Add regularization to the loss.
    loss += 0.5 * reg * np.sum(W * W)
    
    d_loss /= num_train
    d_loss += 0.5 * reg * d_reg
    
    dW = (d_loss - loss)/h
    
    

    ##########################################################################
    # TODO:                                                                     #
    # Compute the gradient of the loss function and store it dW.                #
    # Rather that first computing the loss and then computing the derivative,   #
    # it may be simpler to compute the derivative at the same time that the     #
    # loss is being computed. As a result you may need to modify some of the    #
    # code above to compute the gradient.                                       #
    ##########################################################################

    return loss, dW



def svm_loss_vectorized(W, X, y, reg):
    """
    Structured SVM loss function, vectorized implementation.

    Inputs and outputs are the same as svm_loss_naive.
    """
    h = 0.00001
    loss = 0.0
    dW = np.zeros(W.shape)  # initialize the gradient as zero

    num_train = X.shape[0]
    num_feat = W.shape[0]
    num_classes = W.shape[1]
    
    scores = X.dot(W)
    correct_class_scores = scores[np.arange(num_train),y].reshape(num_train,1)
    margin = scores - correct_class_scores + 1
    rect_margin = np.maximum(margin, np.zeros(scores.shape))
    loss = np.sum(np.sum(rect_margin, axis=1)-1)/num_train
    

    d_loss = np.zeros(W.shape)
    d_reg = np.zeros(W.shape)
    
    cidx = np.arange(num_classes)*num_classes + np.arange(num_classes)
    
    replicated_W = np.tile(W, [1,num_classes])
    
    for f in xrange(num_feat):
        
        old_w = replicated_W[f,cidx]
        replicated_W[f,cidx] += h
        
        replicated_scores = X.dot(replicated_W)
        
        scores = replicated_scores.reshape(num_train,num_classes,num_classes).transpose([1,0,2])
        correct_class_scores = scores[:,np.arange(num_train),y].reshape(num_classes,num_train,1)
        margin = scores - correct_class_scores + 1
        rect_margin = np.maximum(margin, np.zeros(scores.shape))
        d_loss[f,:] = np.sum(np.sum(rect_margin, axis=2)-1, axis=1)/num_train

    
        reshaped_W = replicated_W.reshape(num_feat,num_classes,num_classes).transpose([1,0,2])
    
        reg_arr = np.sum(np.sum(reshaped_W * reshaped_W, axis=1), axis=1)
    
        d_reg[f,:] = reg_arr.reshape(1,num_classes)
        
        replicated_W[f,cidx] = old_w
        
        
    loss += 0.5 * reg * np.sum(W * W)
    
    d_loss += 0.5 * reg * d_reg
    
    dW = (d_loss - loss)/h

    return loss, dW


