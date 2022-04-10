stack<Node *> nodeStack;  //使用C++的STL标准模板库
nodeStack.push(root);
Node *node;
int mindis=INF;
void depthFirstTravel(Node* root){
    while(!nodeStack.empty()){
        node = nodeStack.top();
        printf(format, node->data);  //遍历根结点
        nodeStack.pop();
        if(node->rchild){
            nodeStack.push(node->rchild);  //先将右子树压栈
        }
        if(node->lchild){
            nodeStack.push(node->lchild);  //再将左子树压栈
        }
        if(!node->lchild&&!node->rchild){
            nodeStack.push(node->lchild);  //再将左子树压栈
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
