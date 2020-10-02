#include <stdio.h>
#include <math.h>
#include <string.h>
int main()
{
  int a, b,length,num,anonum;
  char s[7];
  while(scanf("%d %d",&a, &b) != EOF)
  {
	int i=0;
    sprintf(s,"%d",a+b);
    num=a+b;
    length=strlen(s);
    if(abs(num)>=1000)
    {
        if(num<0)
        {
            printf("-");
            i=i+1;
        }
		anonum=(length-i)-3;
        for(int count=0;count<anonum;count++)
        {
            printf("%c",s[i]);
            i=i+1;
        }
        printf(",");
        for(;i<=length;i++)
            printf("%c",s[i]);
    }
    else
        printf("%d",num);
  }
  return 0;
}