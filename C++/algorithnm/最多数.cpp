#include<iostream>
#include<vector>
#include<algorithm>
using namespace std;
class Solution {
public:
    int main(vector<int>& nums) {
        sort(nums.begin(),nums.end());
        int n = nums.size();
        int count = 1,a = 0;
        for(a = 0;a < n-1;a++)
        {
            if(nums[a] == nums[a+1])
            {
                count++;
                if(count > n/2)
                    return nums[a];
            }
            else
            {
                count = 1;
            }
        }
    }
};
