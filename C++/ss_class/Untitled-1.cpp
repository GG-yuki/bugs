#include<iostream>
#include<bits/stdc++.h>
#include<cmath>
#include<iomanip>
#include<algorithm>
#include<cstring>
#include<string.h>
#include<cstdio>
#include<cstdlib>
#include<stdio.h>
#include<vector>
#include<stack>
#include<queue>
#include<math.h>
#include<sstream>
using namespace std;
//q}}}}}}}}}}}}}}}}we{a
//jilin[i lofe{{-v-} ] universiti=y
string s;
string res;
string res0;
int main()
{
    getline(cin,s);

    int i=0;
    int pos=0;
    int flag=0;//未开启替换状态

    while(i<s.size()){
        if((s[i]>='a'&&s[i]<='z')||s[i]==' '){
            res+=s[i];
            pos++;
            i++;
        }else if(s[i]=='['){
            pos=0;
            int j=i+1;
            for(j=i+1;j<s.size()&&((s[j]>='a'&&s[j]<='z')||s[j]==' ');j++){
                res0+=s[j];
                pos++;
            }
            res.insert(0,res0);
            i=j;
            res0.clear();
        }else if(s[i]==']'){
            pos=res.size();
            i++;
        }else if(s[i]=='{'){
            if(pos>0)pos--;
            int j=i+1;
            for(j=i+1;j<s.size()&&((s[j]>='a'&&s[j]<='z')||s[j]==' ');j++){
                res0+=s[j];
            }
                res.insert(pos,res0);
                i=j;
                res0.clear();
        }else if(s[i]=='}'){
            if(pos<res.size())pos++;
            int j=i+1;
            for(j=i+1;j<s.size()&&((s[j]>='a'&&s[j]<='z')||s[j]==' ');j++){
                res0+=s[j];
            }
                res.insert(pos,res0);
                i=j;
                pos+=res0.size();
                res0.clear();
        }else if(s[i]=='-'&&flag==1){
            flag=0;
            int j=i+1;
            for(j=i+1;j<s.size()&&((s[j]>='a'&&s[j]<='z')||s[j]==' ');j++){
                res0+=s[j];
            }
                res.insert(pos,res0);
                i=j;
                res0.clear();
                pos++;
        }else if(s[i]=='-'&&flag==0){
            int j=i+1;
            for(j=i+1;j<s.size()&&((s[j]>='a'&&s[j]<='z')||s[j]==' ');j++){
                res0+=s[j];
            }
            if(pos+res0.size()<res.size()){
                res.replace(pos,res0.size(),res0);
            }else{
                for(int i=pos;i<res.size();i++)res[i]=res0[i];
                pos=res.size();
            }
            res0.clear();
            flag=1;
            i=j;
        }else if(s[i]=='='){
            if(pos==0){
                    i++;
                continue;
            }
            res.erase(pos-1,1);
            res0.clear();
            pos--;
            i++;
        }
    }
    cout<<res;
    return 0;
}