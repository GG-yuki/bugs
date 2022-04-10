#include<bits/stdc++.h>
using namespace std;
#define max 20001

struct Node{
	int to;//指向边的结点 
	int val;//边的权值 
	int next;//指向下一个结点的下标 
} node[max];

int head[max],n,m,num = 0;
int infinite = 99999;

//建立邻接表 
void add(int from,int to,int val){
	
	num++;
	node[num].to = to;
	node[num].val = val;
	node[num].next = head[from];
	head[from] = num;//更新head的值，当再有从from连接的点 它的下一个为 num 坐标 
} 

//dij算法
void dijkstra(){
	int dist[max];
	fill(dist, dist + 20001, infinite);
	int vis[max] = {0};
	
	for(int i = head[0]; i != 0; i = node[i].next){//这里是选取源点为0的顶点，将和其相连边的权值存进去了 
		dist[node[i].to] = node[i].val;   //比如：0到1：即 node[i].to = 1表示的是顶点, node[i].val = 1 表示0到1这条边的权值为1;dist[1] = 1
	}
	
	vis[0] = 1;
	
	while(1){
		
		int m = -1;
		int min = infinite;
		
		for(int i = 0; i < n; i++){
			
			if(vis[i] != 1 && dist[i] < min){
				min = dist[i];
				m = i;
			}
		}
		
		if(m == -1){//已经遍历完了所有结点 
			break;
		}
		
		vis[m] = 1;
		
		//确定m这个顶点 接下来遍历 m这个结点的链表 
		
		for(int i = head[m]; i != 0; i = node[i].next){
			
			if(vis[node[i].to] != 1 && min + node[i].val < dist[node[i].to]){//vis[node[i].to] != 1如果出现 1到2 和2到1这种情况，那么当1已经遍历过，在顶点为2的这个链表中就不用再遍历了
				
				dist[node[i].to] = min + node[i].val;
				
			}	
		} 		
	} 
	
	for(int i = 0; i < n; i++){
		if(dist[i] != infinite){
			cout << dist[i] << ' ';
		}
	}		
} 
 
int main(){
	
	memset(head,0,sizeof(head));
	cin >> n >> m;
	
	for(int i = 0; i < m; i++){
		int from,to,val;
		cin >> from >> to >> val;
		add(from,to,val);
	} 
	//测试邻接表的数据是否正确 
//	for(int i = 0; i < n; i++){
//		cout << i << ' ';
//		for(int j = head[i]; j != 0; j = node[j].next){
//			cout << node[j].to << ' ' << node[j].val << ' '; 
//		}
//		cout << endl;
//	}
	
	dijkstra();
	
}


//4 4
//0 1 1
//0 3 1
//1 3 1
//2 0 1

//邻接表输出的数据 
//0 3 1 1 1
//1 3 1
//2 0 1
//3

//4 5
//0 1 1
//1 3 2
//0 3 4
//0 2 2
//2 3 3


