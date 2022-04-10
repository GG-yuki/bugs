#include <stdio.h>
void main()
{
    int m,n,i;
    float p;
    float re[1001]={0};
    scanf("%d",&m);
    for(i=0;i<m;i++)
    {
        scanf("%d%f",&n,&p);
		re[n]=p;
    }
    scanf("%d",&m);
    for(i=0;i<m;i++)
    {
        scanf("%d%f",&n,&p);
        re[n]=p+re[n];
    }
    m=0;
    for(i=0;i<=1000;i++)
    {
        if(re[i]!=0) m++;
    }
    printf("%d",m);
    for (i = 1000; i >= 0; i--) {
        if(re[i] != 0.0)
            printf(" %d %.1f", i, re[i]);
    }
}