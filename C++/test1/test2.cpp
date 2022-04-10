/******************************************************************** 
* 
*  �ļ�����test1.c 
* 
*  �ļ�������msort 
* 
*  �������ڣ� 2019��12��19�� 
* 
*  �汾�ţ�1.0 
* 
*  �޸ļ�¼�� ���� 
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
	* �� �� ����input_
	* 
	* ��������: ��ȡ������ 
	* 
	* �� �� ֵ��ͷ���� 
	* 
	*============================================================*/ 
	FILE *fp=fopen("in.txt","r");
	if(fp==NULL)
	{
		printf("error\n");
		exit(0);
	}
	stu *head,*p0,*temp;
	p0=(stu*)malloc(sizeof(stu));//���ռ� 
	head=p0;
	head->next=NULL;
	while(!feof(fp))
	{
	    temp=(stu*)malloc(sizeof(stu));
		fscanf(fp,"%d",&temp->number);
		fscanf(fp,"%s",temp->name);
		fscanf(fp,"%d",&temp->grades);
		if(temp->number<0) continue;//����ѧ���Ƿ����� 
		while(p0->next!=NULL&&p0->next->number-temp->number<0)	p0=p0->next;//���� 
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
	free(temp);//�ͷŽڵ� 
	fclose(fp);
	return head;
}

void output_(stu *head)
{
	/*============================================================ 
	* 
	* �� �� ����output_
	* 
	* ��������:����ļ� 
	* 
	* �� �� ֵ��ͷ���� 
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

