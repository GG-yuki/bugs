#include<iostream>
#include<stdio.h>
#include<string>
using namespace std;
#define INT_MAX 2147483647
struct node{
   string route;
   int distance;
   int flag;
   int positions;
   node(){
       flag=0;
       distance=0;
       route="";
       positions=0;
   }
};
class Dijkstra{
   private:
       int Vertices;
       int Sides;
       int** Adjacent;
       node* Nodes;
    public:
        Dijkstra();
        void Calculate();
        void PrintRoute();
        ~Dijkstra();
};


Dijkstra::Dijkstra(){
    int V,S;
    cin>>V>>S;
    this->Vertices=V;
    this->Sides=S;
    Adjacent=new int*[V];
    Nodes=new node[S];
    for(int i=0;i<V;i++){
        Adjacent[i]=new int[V];
        for(int k=0;k<V;k++)
            Adjacent[i][k]=INT_MAX;
    }
    int left,right,weight,num=0;
    while(num<S){
        cin>>left>>right>>weight;
        Adjacent[left][right]=weight;
        num++;
    }
}
Dijkstra::~Dijkstra(){
    delete[] Nodes;
    for(int i=0;i<this->Vertices;i++){
        delete[] this->Adjacent[i];
    }
    delete[] Adjacent;
}
void Dijkstra::Calculate(){
    for(int i=0;i<this->Vertices;i++){
        Nodes[i].route="0->"+to_string(i);
        Nodes[i].positions++;
        Nodes[i].distance=Adjacent[0][i];
    }
    Nodes[0].flag=1;
    Nodes[0].distance=0;
    int num=1;
    while(num<this->Vertices){
        int Chosen=0;
        int Min=INT_MAX;
        for(int i=1;i<this->Vertices;i++){
            if(Nodes[i].flag==0&&Nodes[i].distance<Min){
                Min=Nodes[i].distance;
                Chosen=i;
            }
        }
        Nodes[Chosen].flag=1;
        
        num++;
        for(int i=0;i<this->Vertices;i++){
            if(Nodes[i].flag==0&&Adjacent[Chosen][i]<INT_MAX&&(Nodes[Chosen].distance+Adjacent[Chosen][i])<Nodes[i].distance){
                Nodes[i].distance=Nodes[Chosen].distance+Adjacent[Chosen][i];
                Nodes[i].route=Nodes[Chosen].route+"->"+to_string(i);
                Nodes[i].positions++;
                
            }
            if(Nodes[i].flag==0&&Adjacent[Chosen][i]<INT_MAX&&(Nodes[Chosen].distance+Adjacent[Chosen][i])==Nodes[i].distance&&(Nodes[Chosen].positions+1)<Nodes[i].positions){                
                Nodes[i].distance=Nodes[Chosen].distance+Adjacent[Chosen][i];
                Nodes[i].route=Nodes[Chosen].route+"->"+to_string(i);
                Nodes[i].positions=Nodes[Chosen].positions+1;
            }          
        }
    }
    return;
 }


void Dijkstra::PrintRoute(){
   for(int i=1;i<this->Vertices;i++){
        if(Nodes[i].distance<INT_MAX)
           cout<<Nodes[i].route<<endl;
   }
   return;
}

int main(){
    Dijkstra D;
    D.Calculate();
    D.PrintRoute();
    return 0;
}