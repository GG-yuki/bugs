#include<iostream>
#include<bits/stdc++.h>
#include<cmath>
#include<iomanip>
#include<algorithm>
#include<cstring>
#include<string.h>
#include<cstdio>
#include<stdlib.h>
#include<stdio.h>
#include<vector>
#include<stack>
#include<queue>
#include<math.h>
#include<sstream>

using namespace std;

int main(void)
{
    vector<int> v1,v2;
    int number,temp;
    while (cin >> number)
    {
         v1.push_back(number);
	 if (cin.get() == '\n') //按下回车键退出循环
		break;
    }
    for(auto it = v1.begin(); it != v1.end(); it++)
    {
        if((*it) != 0) v2.push_back((*it));
        if((*it) == 0) 
        {
        }
    }
    return 0;
}

int multiplication(vector<int> v1)
{
    int result = 1;
    for(auto it = v1.begin(); it != v1.end(); it++)  result = result * (*it);
    return result;
}