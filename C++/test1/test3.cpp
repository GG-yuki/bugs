#include<iostream>
#include<bits/stdc++.h>
#include<cmath>
#include<iomanip>
#include<string>
#include<cstdio>
#include<stdlib.h>
using namespace std;

//template<typename T>

//int fuc(int *);

int main(void)
{
    int n;
    cin>>n;
    string c;
    cin>>c;

    int s;
    for(int i=0;i<n;i++){
        cin>>s;
        if(s==1){
            string c2;
            cin>>c2;
            c=c+c2;
            cout<<c<<endl;
        }
        if(s==2){
            int a,b;
            cin>>a>>b;
            string c2;
            int i,j=0;
            for(i=a;i<a+b;i++){
                c2[j]=c[i];
                j++;
            }
            c2[j]='\0';
            c=c2;
            cout<<c<<endl;
        }
        if(s==3){
            int x;
            cin>>x;
            string c2;
            cin>>c2;
            c.insert(x,c2);
            cout<<c<<endl;
        }
        if(s==4){
            string c2;
            cin>>c2;
            int ti=0,num=0;
            for(int i=0;i<=(c.size()-c2.size());i++){
                for(int j=0;j<c2.size();j++){
                    if(c[i+j]=c[j])ti++;
                }
                if(ti==c2.size()){
                    num=i;
                    break;
                }
            }
            if(num==0)cout<<"-1"<<endl;
            else cout<<num<<endl;
        }
    }



    return 0;
}
