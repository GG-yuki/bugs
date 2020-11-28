s#include<iostream>

using namespace std;
#define lint long long
#define inf 0x3f3f3f

template<typename T>
class vector
{
public:
    vector()
    {
        array=new T[100];
        num=0;
    }
    ~vector()
    {
        delete[] array;
    }
    int size()const{return num;}
    bool empty()const{return num==0;}
    void push_back(T x)
    {
        array[num++]=x;
    }
    void pop_back(){num--;}
    T operator[](int x)
    {
        return array[x];
    }
    void clear()
    {
        while(!empty()) pop_back();
    }

private:
    T* array;
    int num;
};





template<typename T>
struct Node
{
    T data;
    Node* next;
    Node(){next=NULL;}
};
template<typename T>
class queue
{
private:
    Node<T> *head,*rear;
public:
    queue(){head=rear=NULL;}
    ~queue(){clear();}
    void push(T x)
    {
        Node<T>* p=new Node<T>;
        p->data=x;
        if(head==NULL) head=rear=p;
        else rear->next=p;
        rear=p;
    }
    void pop()
    {
        Node<T>*p=head;
        head=head->next;
        delete p;
        if(head==NULL) rear=NULL;
    }
    T size()
    {
        int count=0;
        Node<T>*p=head;
        while(p)
        {
            p=p->next;
            count++;
        }
        return count;
    }
    bool empty()
    {
        return head==NULL&&rear==NULL;
    }
    T front()
    {
        return head->data;
    }
    T back()
    {
        Node<T>*p=head;
        while(p->next) p=p->next;
        return p->data;
    }
    void clear()
    {
        while(!empty())
        {
            Node<T>*p=head;
            if(head) head=head->next;
            else head=rear=NULL;
            delete p;
        }
    }
};






struct node
{
    lint num;
    node*firstChild;
    node*nextBrother;
    lint MAX_weight;
    lint MIN_weight;
    vector<int> maxnode;
    vector<int> minnode;
    node(){firstChild=nextBrother=NULL;}
};


node*MAX;
node*createTree()
{
    lint x;
    cin >> x;
    if(x==0) return NULL;
    node*tmp=new node;
    tmp->num=x;
    tmp->firstChild=createTree();
    tmp->nextBrother=createTree();
    return tmp;
}


void caculateLength(node*root)
{
    if(root->firstChild)
    {
        caculateLength(root->firstChild);
        lint MAXweight=-inf;
        lint MINweight=inf;
        node *maxnode=NULL,*minnode=NULL;
        for(node*tmp=root->firstChild;tmp;tmp=tmp->nextBrother)
        {
            if(tmp->MAX_weight>MAXweight)
            {
                maxnode=tmp;
                MAXweight=tmp->MAX_weight;
            }
            else if(tmp->MAX_weight==MAXweight)
            {
                if(tmp->maxnode.size() < maxnode->maxnode.size())
                {
                    maxnode=tmp;
                    MAXweight=tmp->MAX_weight;
                }
            }

            if(tmp->MIN_weight<MINweight)
            {
                minnode=tmp;
                MINweight=tmp->MIN_weight;
            }
            else if(tmp->MIN_weight==MINweight)
            {
                if(tmp->minnode.size() < maxnode->minnode.size())
                {
                    minnode=tmp;
                    MINweight=tmp->MIN_weight;
                }
            }
        }





        if(root->num>0)
        {

                root->MAX_weight=root->num*MAXweight;
                root->maxnode=maxnode->maxnode;
                if(root->num!=1||!root->maxnode.empty())root->maxnode.push_back(root->num);

                root->MIN_weight=root->num*MINweight;
                root->minnode=minnode->minnode;
                if(root->num!=1||!root->maxnode.empty()) root->minnode.push_back(root->num);

                if(root->MAX_weight==0)
                {
                    root->MAX_weight=root->num;
                    root->maxnode.clear();
                    root->maxnode.push_back(root->num);
                }
                if(root->MIN_weight==0)
                {
                    root->minnode.clear();
                }
//                if(root->MAX_weight<0)
//                {
//                    root->MAX_weight=root->num;
//                    root->maxnode.clear();
//                    root->maxnode.push_back(root->num);
//                }
//                if(root->MIN_weight>0)
//                {
//                    root->MIN_weight=1;
//                    root->minnode.clear();
//                }

        }
        else if(root->num<0)
        {

                root->MAX_weight=root->num*MINweight;
                root->maxnode=minnode->minnode;
                root->maxnode.push_back(root->num);

                root->MIN_weight=root->num*MAXweight;
                root->minnode=maxnode->maxnode;
                root->minnode.push_back(root->num);

                if(root->MAX_weight==0)
                {
                    root->maxnode.clear();
                }
                if(root->MIN_weight==0)
                {
                    root->MIN_weight=root->num;
                    root->minnode.clear();
                    root->minnode.push_back(root->num);
                }

//                if(root->MAX_weight<0)
//                {
//                    root->MAX_weight=1;
//                    root->maxnode.clear();
//                }
//                if(root->MIN_weight>0)
//                {
//                    root->MIN_weight=root->num;
//                    root->minnode.clear();
//                    root->minnode.push_back(root->num);
//                }

        }


    }
    else
    {
        if(root->num>0)
        {
            if(root->num!=1) root->maxnode.push_back(root->num);
            root->MAX_weight=root->num;
            root->MIN_weight=0;
        }
        else
        {
            root->MAX_weight=0;
            root->minnode.push_back(root->num);
            root->MIN_weight=root->num;
        }

    }

    if(root->nextBrother) caculateLength(root->nextBrother);

}

//void preorder(node*root)
//{
//    node*tmp=root;
//    if((tmp->MAX_weight > MAX->MAX_weight)||
//                (tmp->MAX_weight==MAX->MAX_weight && tmp->maxnode.size()<MAX->maxnode.size())) MAX=tmp;
//    if(root->firstChild)preorder(root->firstChild);
//    if(root->nextBrother) preorder(root->nextBrother);
//}

void levelorder(node*root)
{

    queue<node*> q;
    q.push(root);

    while(!q.empty())
    {

        node*tmp=q.front();
        q.pop();
        while(tmp)
        {
            if((tmp->MAX_weight > MAX->MAX_weight)||
                        (tmp->MAX_weight==MAX->MAX_weight && tmp->maxnode.size()< MAX->maxnode.size())) MAX=tmp;
            if(tmp->firstChild) q.push(tmp->firstChild);
            tmp=tmp->nextBrother;
        }

    }
}


void print()
{
    cout << MAX->MAX_weight << endl;
    if(MAX->maxnode.empty()) cout << "1 ";
    for(int i=MAX->maxnode.size()-1;i>=0;i--)
    {
        cout << MAX->maxnode[i] << " ";
    }


}
int main()
{
    node*root=createTree();
    caculateLength(root);
    MAX=root;
//    preorder(root);
    levelorder(root);
    print();
    return 0;
}

/*
8 100 -1 0 -6 0 -2 0 0 -3 4 0 0 7 0 0 0
8 -6 3 -2 -1 9 0 0 0 0 0 0 0
-10 -2 -10 1 0 0 0 -1 2 0 0 -2 0 0 0
1 1 0 1 0 0 0
3 -2 5 0 0
2 1 3 -1 3 1 2 0 0 0 0 0 0 0 0
4 -3 1 0 -1 0 0 2 0 -1 -5 -9 0 -9 0 2 0 0 0 0 0
-2 -1 4 0 -1 0 6 0-4 -3 -2 -1 0 2 0 0 0 0 0 0 3 5 0 0 7 0 0 0
-2 -2 -2 -1 0 2 0 0 0 0 0
1 1 6 0 1 0 1 0 0 2 3 0 0 1 0 0 0
-4 -1 0 -1 2 1 1 0 0 0 0 0 0
*/

