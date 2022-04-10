/******************************************************************** 
* 
*  文件名：test1.c 
* 
*  文件描述：msort 
* 
*  创建日期： 2019年12月19日 
* 
*  版本号：1.0 
* 
*  修改记录： 暂无 
* 
********************************************************************/ 
#include<stdio.h>
#include<stdlib.h>
#include<string.h>

typedef struct student
{
	int number;
	char name[20];
	int grades;
	struct student *next;
}stu;

void output_(stu *head);
stu* input_();

int main(){
	stu *head;
	head=input_();
	output_(head);
	return 0;
}

stu* input_()
{
	/*============================================================ 
	* 
	* 函 数 名：input_
	* 
	* 功能描述: 读取并排序 
	* 
	* 返 回 值：头链表 
	* 
	*============================================================*/ 
	FILE *fp=fopen("in.txt","r");
	if(fp==NULL)
	{
		printf("error\n");
		exit(0);
	}
	stu *head,*p0,*temp;
	p0=(stu*)malloc(sizeof(stu));//开空间 
	head=p0;
	head->next=NULL;
	while(!feof(fp))
	{
	    temp=(stu*)malloc(sizeof(stu));
		fscanf(fp,"%d",&temp->number);
		fscanf(fp,"%s",temp->name);
		fscanf(fp,"%d",&temp->grades);
		if(temp->number<0) continue;//检验学号是否正常 
		while(p0->next!=NULL&&p0->next->number-temp->number<0)	p0=p0->next;//排序 
		if(p0->next==NULL)
		{
			p0->next=temp;
			temp->next=NULL;
		}
		else
		{
			temp->next=p0->next;
			p0->next=temp;
		}
		p0=head;
	}
	temp=head;
	head=head->next;
	free(temp);//释放节点 
	fclose(fp);
	return head;
}

void output_(stu *head)
{
	/*============================================================ 
	* 
	* 函 数 名：output_
	* 
	* 功能描述:输出文件 
	* 
	* 返 回 值：头链表 
	* 
	*============================================================*/ 
	FILE *out=fopen("out.txt","w");
	stu *p=head;
	if(out==NULL)
	{
	    printf("error\n");
	}
	while(p!=NULL)
	{
		fprintf(out,"%d\t",p->number);
		fprintf(out,"%s\t",p->name);
		fprintf(out,"%d\n",p->grades);
	    p=p->next;
	}
	fclose(out);
	printf("ok\n");
}

