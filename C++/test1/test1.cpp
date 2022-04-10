#include<iostream>
#include<cstdio>
#include<string.h>
using namespace std;


int main()
{
int a,b,c;
scanf("%d,%d",&a,&b);
if(a>b) c=a;
else c=b;
printf("%d",c);
return 0;
}

int min(){
	int count=0;
	string sa ,sb ,sc;
    getline(cin, sa);
    getline(cin, sb);
    for(int i =0;i<sb.size();i++)
	{
        sb[i] = toupper(sb[i]);//转换为大写
    }
    for(int i =0;i<sa.size();i++)
	{
        sa[i] = toupper(sa[i]);//转换为大写
    }
    int i=0,j=0,m=0,k;
	while(j<=sb.size())
	{
	    while(sb[j]==' ') j++;
	    m=j;
	    while(j<=sb.size())
        {
		for(;sb[j]!=' '&&sb[j]!='\n';j++) ;
        sc=sb.substr(m,j-1);
//		if((strcmp(sa.c_str(),sc.c_str()))==0)
//		{
//			count=count+1;
//			if(count==1)
//			{
//				cout << m;
//			}
//		}
        i=0;
        while(i<sa.size())
        {
            if(sa[i]!=sc[i]) i=sa.size();
            if(sa[i]==sc[i]&&i==sa.size()-1)
            {
                count=count+1;
                if(count==1) k=m;
            }
            i++;
        }
		j=j+1;
		m=j;
        }
	}
	if(count!=0)
	{
	    cout << count;
        cout << ' ';
        cout << k;
	}
	if(count==0) cout << -1;
}

