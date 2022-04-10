// 不围棋（NoGo）样例程序
// 随机策略
// 游戏信息：http://www.botzone.org/games#NoGo


//json交互
#include <iostream>
#include <cstdio>
#include <string>
#include <cstring>
#include "jsoncpp/json.h"
using namespace std;

int board[9][9] = { {0} };


bool dfs_air_visit[9][9];
const int cx[] = { -1,0,1,0 };
const int cy[] = { 0,-1,0,1 };

bool inBorder(int x, int y) { return x >= 0 && y >= 0 && x<9 && y<9; }

//true: has air
bool dfs_air(int fx, int fy)
{
	dfs_air_visit[fx][fy] = true;
	bool flag = false;
	for (int dir = 0; dir < 4; dir++)
	{
		int dx = fx + cx[dir], dy = fy + cy[dir];
		if (inBorder(dx, dy))
		{
			if (board[dx][dy] == 0)
				flag = true;
			if (board[dx][dy] == board[fx][fy] && !dfs_air_visit[dx][dy])
				if (dfs_air(dx, dy))
					flag = true;
		}
	}
	return flag;
}

//true: available
bool judgeAvailable(int fx, int fy, int col)
{
	if (board[fx][fy]) return false;//若此处已放棋子，则决不能再放棋子
	board[fx][fy] = col;
	memset(dfs_air_visit, 0, sizeof(dfs_air_visit));
	if (!dfs_air(fx, fy))
	{
		board[fx][fy] = 0;
		return false;
	}
	for (int dir = 0; dir < 4; dir++)
	{
		int dx = fx + cx[dir], dy = fy + cy[dir];
		if (inBorder(dx, dy))
		{
			if (board[dx][dy] && !dfs_air_visit[dx][dy])
				if (!dfs_air(dx, dy))
				{
					board[fx][fy] = 0;
					return false;
				}
		}
	}
	board[fx][fy] = 0;
	return true;
}

int main()
{
	srand((unsigned)time(0));
	string str;
	int x, y;
	// 读入JSON
	getline(cin, str);
	//getline(cin, str);
	Json::Reader reader;
	Json::Value input;
	reader.parse(str, input);
	// 分析自己收到的输入和自己过往的输出，并恢复棋盘状态
	int turnID = input["responses"].size();//第一步时turnID等于0，注意是responses的size，而不是request的size
	for (int i = 0; i < turnID; i++)
	{
		x = input["requests"][i]["x"].asInt(), y = input["requests"][i]["y"].asInt();//对方，注意此处是requests
		if (x != -1) board[x][y] = 1;
		x = input["responses"][i]["x"].asInt(), y = input["responses"][i]["y"].asInt();//我方，注意此处是responses
		if (x != -1) board[x][y] = -1;
	}
	x = input["requests"][turnID]["x"].asInt(), y = input["requests"][turnID]["y"].asInt();//对方，注意此处是requests
	if (x != -1) board[x][y] = 1;
	//此时board[][]里存储的就是当前棋盘的所有棋子信息,x和y存的是对方最近一步下的棋
	
	/************************************************************************************/
	/***********在下面填充你的代码，决策结果（本方将落子的位置）存入new_x和new_y中****************/
		//下面仅为随机策略的示例代码，可删除
	int available_list[81]; //合法位置表 
	int k = 0;
	for (int i = 0; i<9; i++)
		for (int j = 0; j<9; j++)
			if (judgeAvailable(i, j, x == -1 ? 1 : -1))
			{
				available_list[k] = i * 9 + j;
				k++;
			}
	int result = available_list[rand() % k];
	int new_x = result / 9;		int new_y = result % 9;
	/***********在上方填充你的代码，决策结果（本方将落子的位置）存入new_x和new_y中****************/
	/************************************************************************************/
	
	// 输出决策JSON
	Json::Value ret;
	Json::Value action;
	action["x"] = new_x; action["y"] = new_y;
	ret["response"] = action;
	ret["debug"] = turnID;//调试信息可写在这里
	Json::FastWriter writer;

	cout << writer.write(ret) << endl;
	return 0;
}


