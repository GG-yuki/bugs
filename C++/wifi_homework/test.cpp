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
    vector<int> v1,v2,v3;
    int min_length = 0, temp_length = 0;
    int number,temp = 1, max = 1;
    while (cin >> number)
    {
         v1.push_back(number);
	 if (cin.get() == '\n') //按下回车键退出循环
		break;
    }
    auto it = v1.begin();

    for(; (*it) !=0; it++) v2.push_back((*it));//输入，遇0停止

    for(; it != v1.end(); it++)//遇0计算一遍乘积并判断，遇到数字则push进v2
    {
        if((*it) == 0) 
        {
            temp = multiplication(v2);
            temp_length = v2.size();
            v2.pop_back((*it));
        }
        if(temp >= max)
        {
            if (temp == max)
            {
                if(temp_length < min_length)
                {
                    temp_length = min_length;
                    v3 = v2;
                }
            }
            max = temp;
            v3 = v2;
            min_length = v3.size();
        }
        if((*it) != 0) v2.push_back((*it));
    }
    cout << max;
    return 0;
}

int multiplication(vector<int> v1)
{
    int result = 1;
    for(auto it = v1.begin(); it != v1.end(); it++)  result = result * (*it);
    return result;
}