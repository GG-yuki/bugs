stack<Node *> nodeStack;  //ʹ��C++��STL��׼ģ���
nodeStack.push(root);
Node *node;
int mindis=INF;
void depthFirstTravel(Node* root){
    while(!nodeStack.empty()){
        node = nodeStack.top();
        printf(format, node->data);  //���������
        nodeStack.pop();
        if(node->rchild){
            nodeStack.push(node->rchild);  //�Ƚ�������ѹջ
        }
        if(node->lchild){
            nodeStack.push(node->lchild);  //�ٽ�������ѹջ
        }
        if(!node->lchild&&!node->rchild){
            nodeStack.push(node->lchild);  //�ٽ�������ѹջ
        }
    }
}

int stacksum(stack<int> valstack)
{
	int sum=0;
	while(!valstack.empty())
	{
		sum=sum+valstack.top();
	}
}
