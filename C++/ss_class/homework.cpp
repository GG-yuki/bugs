#include <string>
#include <iostream>
using namespace std;

typedef struct Node
{
	int data;			//data中存放结点数据域（默认是int型）
	struct LNode *next; //指向后继结点的指针
}Node;

int main()
{
    Node *L;
    int i,n,m,flag;
    int pos,data;
    cout<<"请输入链表长度";
    cin>>n;
    L = TailCreateList(n);
    cin>>m;
    for(i = 0; i < m; i++)
    {
        cin>>flag;
        if(flag) 
        {
            cin>>pos>>data;
            Insert(L,pos,data);
        }
        if(!flag) 
        {
            cin>>pos;
            delete(L,pos);
        }
    }
    PrintfList(L);
    return 0
}



Node *TailCreateList(int len)
{
	Node *L = (Node*)malloc(sizeofLNode)); //创建一个头结点
	Node *temp = L;//声明一个中间变量，指向头结点，用于遍历链表（曾因没有这个中间变量而出错）
	temp->next = NULL;//该链表此刻只带头结点
	
	for(int i=1;i<=len;i++) //循环申请len个结点来接收scanf得到的元素
	{
		Node *p = (Node*)malloc(sizeof(Node)); //生成新结点
		scanf("%d",&p->data);  //用新申请的结点来接收scanf得到的元素
		/* 以下两条语句是尾插法的关键步骤 */
		temp->next = p;   //用来接纳新结点
		temp = p;		  //指向终端结点，以便于接纳下一个到来的结点，此语句也可以改为"L = L->next"
	}
	temp->next = NULL;	  //此刻所有元素已经全装入链表L中，L的终端结点的指针域置为NULL
	
	return (Node*)L;
}

Node *Insert(Node *L, int pos, int elem)
{
	Node *temp = L;	//引入一个中间变量，用于循环变量链表
	int i = 0;
	/* 首先找到插入结点的上一结点，即第pos-1个结点 */
	while( (temp!=NULL)&&(i<pos-1) )
	{
		temp = temp->next;
		++i;
	}
	/* 错误处理：链表为空或插入位置不存在 */
	if( (temp==NULL)||(i>pos-1) )		
	{
		printf("%s:Insert false!\n",__FUNCTION__);
		return (Node*)temp;
	}
	Node *new = (Node*)malloc(sizeof(Node));	//创建新结点new
	new->data = elem;		//插入的新结点的数据域
	new->next = temp->next; //新结点的next指针指向插入位置后的结点
	temp->next = new;		//插入位置前的结点的next指针指向新结点
	
	return (Node*)L;		//注意！！不能写为 "return (LNode*)temp;"
}

Node *Delete(Node *L, int pos, int *elem)
{
	Node *temp = L;	//引入一个中间变量，用于循环变量链表
	int i = 0;
	/* 首先找到删除结点的上一结点，即第pos-1个结点 */
	while( (temp!=NULL)&&(i<pos-1) )
	{
		temp = temp->next;
		++i;
	}
	/* 错误处理：链表为空或删除位置不存在 */
	if( (temp==NULL)||(i>pos-1) )
	{
		printf("%s:Delete false!\n",__FUNCTION__);
		return (Node*)temp;
	}
	Node *del = temp->next;	//定义一个del指针指向被删除结点
	*elem = del->data;			//保存被删除的结点的数据域
	temp->next = del->next;		/*删除结点的上一个结点的指针域指向删除结点的下一个结点，
								  也可写为“temp->next = temp->next->next”*/
	free(del);					//手动释放该结点，防止内存泄露
	del = NULL;					//防止出现野指针
	
	return (Node*)L;			//注意！！不能写为 "return (LNode*)temp;"
}

void PrintfList(Node *L)
{
	Node *temp = L;
	int count = 0;		//计数器
	printf("List:\n");
	while(temp->next)
	{
		temp = temp->next;
		printf("%d\t",temp->data);
		count++;
	}
	printf("\n");
}
