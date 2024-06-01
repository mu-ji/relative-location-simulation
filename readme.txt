Author Manjiang Cao
E-mail mcao999@connect.hkust-gz.edu.cn

This project trying to figure out if all nodes don't know their position, and they can only measure the distance and direction between each other, can their find out the relative position between each other






research log

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
05/31/2024

Update:

Now the simulator works randomly, trying to find out in which condition (how noisy and how many nodes are communicable) the localization can convergent

when noise varance is 4 and communicable rate = 0.5, convergent very quick (within 10 steps)
when noise varance is 4 and communicable rate = 0.25, hardly convergnet or can't convergent
when noise varance is 3 and communicable rate = 0.25, hardly convergnet or can't convergent
when noise varance is 2 and communicable rate = 0.25, convergent very quick (within 10 steps)

it seems that noise are more important, when noise is 0, even communicable rate = 0.1 can convergent. BTW, in simulator, number of nodes is 20, so communicable rate = 0.1 equals one node only communicate with two node

to convergent, each node need communicate with at least two nodes !!

Basically, the larger the noise, the harder it is to converge. The lower the communicable rate, the harder it is to converge.


Action:

Try to make this randomly simulator into an optimization problem.

The optimization problem has faster convergence and higher accuracy, but may require a deeper understanding of the topology

Maybe it is possible to find the relationship between noise level, network complexity (communicable rate) with convergence speed and localization accuracy in optimization problems

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

06/01/2024

Update:

Trying to implement a KF on each node to avoid random

KF is in KF4single_node.py, the performance is not good, maybe not suit for KF. It works when there only two nodes, maybe can be used in second idea (Notion->research idea->multi target tracking->use some methods to locate some nodes, them use these nodes to locate others nearby, until all nodes are located)



Action:

avoid using true position to judge when is convergence, because in real situation, the true position is unknow

find another optimization target

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------