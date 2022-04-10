#include<iostream>
#include<stdio.h>
#include<string>
#include <cstring>
#include <algorithm>
#include <vector>
using namespace std;
#define INF 20000
// int** G;
int head[20000];
int gnum = 0;
int n,m,a,b,weight;
vector<int> node_dist;
vector<int> node_tf;
vector<int> node_rank;
vector<string> ans_rou;
struct Gap{
	int to;//指向边的结点 
	int val;//边的权值 
	int next;//指向下一个结点的下标 
} G[20000];

void add(int from,int to,int val){
	
	gnum++;
	G[gnum].to = to;
	G[gnum].val = val;
	G[gnum].next = head[from];
	head[from] = gnum;//更新head的值，当再有从from连接的点 它的下一个为 num 坐标 
} 

void dji(){
    for(int i = 0; i < n; i++)
    {
        node_tf.push_back(0);
        node_rank.push_back(1);
        ans_rou.push_back(("0->" + to_string(i)));
    }
    for(int i = head[0]; i != 0; i = G[i].next){//这里是选取源点为0的顶点，将和其相连边的权值存进去了 
		node_dist[G[i].to] = G[i].val;   //比如：0到1：即 node[i].to = 1表示的是顶点, node[i].val = 1 表示0到1这条边的权值为1;dist[1] = 1
	}
    node_tf[0] = 1;
    node_dist[0] = 0;
    for(int j = 1; j < n; j++){
        int temp = 0;
        int Min = INF;
        for(int i = 1;i < n;i++){
            if(node_tf[i] == 0 && node_dist[i] < Min){
                Min = node_dist[i];
                temp = i;
            }
        }
        node_tf[temp] = 1;
        // for(int i = head[temp];i != 0;i = G[i].next){
        //     if(node_tf[i] == 0 && G[temp][i] < INF && (node_dist[temp] + G[temp][i]) <= node_dist[i]){
        //         node_dist[i] = node_dist[temp] + G[temp][i];
        //         ans_rou[i] = ans_rou[temp] + "->" + to_string(i);
        //         if((node_dist[temp] + G[temp][i]) < node_dist[i]){
        //             node_rank[i]++;
        //         }
        //         else if((node_dist[temp] + G[temp][i]) == node_dist[i] && (node_rank[temp] + 1) < node_rank[i]){
        //             node_rank[i] = node_rank[temp] + 1;
        //         }
        //         else{
        //             node_rank[i]++;
        //         }
        //     }
        // }
        for(int i = head[temp];i != 0;i = G[i].next){
            if(node_tf[G[i].to] == 0 && (Min + G[i].val) < node_dist[G[i].to]){
                node_dist[G[i].to] = Min + G[i].val;
                ans_rou[G[i].to] = ans_rou[temp] + "->" + to_string(G[i].to);
                node_rank[G[i].to]++;
            if(node_tf[G[i].to] == 0 && (Min + G[i].val) == node_dist[G[i].to] && (node_rank[temp] + 1) < node_rank[G[i].to]){
                node_dist[G[i].to] = node_dist[temp] + G[i].val;
                ans_rou[G[i].to] = ans_rou[temp] + "->" + to_string(G[i].to);
                node_rank[G[i].to] = node_rank[temp] + 1;
                }
            }
        }
    }
    return;
 }


void result(){
   for(int i = 1;i < n;i++){
        if(node_dist[i] < INF)
           cout<<ans_rou[i]<<endl;
   }
   return;
}


int main(){
    cin>>n>>m;
    for(int num = 0; num < m; num++){
        cin>>a>>b>>weight;
        add(a,b,weight);
    }
    dji();
    result();
    return 0;
}