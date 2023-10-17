//Author : Vibesh Kumar and Prakhar Gupta
#include <iostream>
#include <cstdlib>
#include <vector>
#include <cmath>
using namespace std;

double Prob_head = 0.4;
int N = 10;
int end_Reward = N * 2;
double gamma2 = 0.9;

int state_count = N+1;
double epsilon = 1e-14;

//util for 0 and N is -1 meaning exit
vector<int> policy1()
{
    vector<int> state_policy = vector<int>(state_count);
    for(int i = 1; i < state_policy.size(); i++)
    {
        state_policy[i]=  min(i,N-i);
    }
    state_policy[0] = -1;
    state_policy[N] = -1;

    return state_policy;
}

vector<int> policy2()
{
    vector<int> state_policy = vector<int>(state_count);
    for(int i = 0; i < state_policy.size(); i++)
    {
        state_policy[i] = 1;
    }
    state_policy[0] = -1;
    state_policy[N] = -1;
    return state_policy;
}

bool norm_check(vector<double> U_i0, vector<double> U_i1)
{
    double square_diff = 0;
    for(int i = 0; i < U_i0.size(); i++)
    {
        square_diff += (U_i0[i] - U_i1[i])*(U_i0[i] - U_i1[i]);
    }
    square_diff = sqrt(square_diff);
    if(square_diff < epsilon)
    {
        return true;
    }
    else
    {
    return false;
    }

}

vector<double> policy_util(vector<int> state_policy)
{
    vector<double> old_util(state_count,0);
    vector<double> new_util(state_count,0);
    old_util[N]= end_Reward;
    new_util[N] = end_Reward;
    do
    {
        old_util = new_util;
        for(int i = 1; i < state_policy.size()-1; i++)
        {
            new_util[i] = Prob_head*(gamma2*(old_util[i+state_policy[i]])) + (1-Prob_head)*(gamma2*(old_util[i-state_policy[i]]));
        }
    }while(!norm_check(old_util,new_util));
    return new_util;
}


vector<int> policyOptimal_valueIteration()
{
    vector<double> old_util(state_count,0);
    vector<double> util(state_count,0);
    vector<int> policy(state_count,0);
    do{
        old_util =util;
        for(int j = 0; j < state_count; j++)
        {
            if(j == N)
            {
               util[j] = end_Reward;
            }
            else if(j == 0)
            {
               util[j] = 0;
            }
            else
            {
                double maxx = -1e37;
                for(int i = 0; i <= min(j,N-j); i++)
                {
                    if(maxx < (Prob_head*(gamma2*old_util[i+j]) + (1-Prob_head)*(gamma2*old_util[j-i])) )
                    {
                        policy[j] = i;
                        maxx =(Prob_head*(gamma2*old_util[i+j]) + (1-Prob_head)*(gamma2*old_util[j-i]));
                        util[j] = maxx;
                    }
                }
            }
        }
    }while(!norm_check(util,old_util));
    return policy;
}

vector<int> policyOptimal_policyIteration()
{
    vector<double> util(state_count,0);
    vector<int> policy(state_count,0);
    vector<int> prev_policy(state_count,0);
    do{
        prev_policy = policy;
        for(int j = 0; j < state_count; j++)
        {
                vector<double> policy_util_temp = policy_util(policy);
                double maxx = policy_util_temp[j];
                for(int i = 0; i <= min(j,N-j); i++)
                {                    
                    double eachAction_util = (Prob_head*(gamma2* policy_util_temp[i+j]) + (1-Prob_head)*(gamma2*  policy_util_temp[j-i]));
                    if(maxx < eachAction_util)
                    {
                        maxx = eachAction_util;
                        policy[j] = i;
                    }
                }
            }
        }
    while(!(prev_policy==policy));
    return policy;
}

int main()
{
    cout << "State" << " " << "Policy" << "  "<< "Utility" << endl;
    cout << endl;
    cout << "Policy 1" << endl;
    for(int x =  0; x < policy1().size() ; x++)
    cout << x  << "     " << policy1()[x]<< "      " << policy_util(policy1())[x] << endl;

    cout << endl;
    cout << "Policy 2" << endl;
    for(int x =  0; x < policy2().size() ; x++)
    cout << x  << "      " << policy2()[x]<< "      " << policy_util(policy2())[x] << endl;

    cout << endl;
    cout << "Optimal Policy (Value Iteration)" << endl;
    for(int x =  0; x < policyOptimal_valueIteration().size() ; x++)
    cout << x  << "      " << policyOptimal_valueIteration()[x]<< "     " << policy_util(policyOptimal_valueIteration())[x] << endl;
    
    cout << endl;
    cout << "Optimal Policy (Policy Iteration)" << endl;
    for(int x =  0; x < policyOptimal_policyIteration().size() ; x++)
    cout << x  << "     " << policyOptimal_policyIteration()[x]<< "      " << policy_util(policyOptimal_policyIteration())[x] << endl;

    return 1;
}