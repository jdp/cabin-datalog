## CS 838: Foundations of Data Management

### Lecture 7: Intro to Datalog ([notes](https://pages.cs.wisc.edu/~paris/cs838-s16/lecture-notes/lecture7.pdf))

here i will struggle to even work these out on paper

> Example 7.1. Let R(A, B) be a relation that contains the edges of a directed graph. The following Datalog program computes the transitive closure of the graph: all the pairs (u, v) of vertices, such that there is a
directed path from node u to node v:
> 
>     T(x,y) :- R(x,y).
>     T(x,y) :- T(x,z), R(z,y).

cool

> Exercise 7.3. Consider the transitive closure on the following instance: I = {R(1, 2) R(2, 3), R(3, 4)}. What is the minimal model in this case? Can you find a non-minimal model and a non-model?

The EDB is:
    
    R(1,2)
    R(2,3)
    R(3,4)

The IDB is:

    T(1,2)
    T(1,3)
    T(1,4)
    T(2,3)
    T(2,4)
    T(3,4)

A non-minimal model would be any superset of the model and would include values for A and/or B outside of the active domain of {1, 2, 3, 4}.

A non-model would be any subset or disjoint set of the model.

> Exercise 7.7. Consider the transitive closure on the following instance: I = {R(1, 2) R(2, 3), R(3, 4)}.
Show the application of the operator TP until it reaches the fixpoint.

Initial

    T(1,2)
    T(2,3)
    T(3,4)

Iteration 1

    T(1,2)
    T(2,3)
    T(3,4)
    T(1,3)
    T(2,4)

Iteration 2

    T(1,2)
    T(2,3)
    T(3,4)
    T(1,3)
    T(2,4)
    T(1,4)
