// ��Χ�壨NoGo����������
// �������
// ��Ϸ��Ϣ��http://www.botzone.org/games#NoGo


//json����
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
	if (board[fx][fy]) return false;//���˴��ѷ����ӣ���������ٷ�����
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
	// ����JSON
	getline(cin, str);
	//getline(cin, str);
	Json::Reader reader;
	Json::Value input;
	reader.parse(str, input);
	// �����Լ��յ���������Լ���������������ָ�����״̬
	int turnID = input["responses"].size();//��һ��ʱturnID����0��ע����responses��size��������request��size
	for (int i = 0; i < turnID; i++)
	{
		x = input["requests"][i]["x"].asInt(), y = input["requests"][i]["y"].asInt();//�Է���ע��˴���requests
		if (x != -1) board[x][y] = 1;
		x = input["responses"][i]["x"].asInt(), y = input["responses"][i]["y"].asInt();//�ҷ���ע��˴���responses
		if (x != -1) board[x][y] = -1;
	}
	x = input["requests"][turnID]["x"].asInt(), y = input["requests"][turnID]["y"].asInt();//�Է���ע��˴���requests
	if (x != -1) board[x][y] = 1;
	//��ʱboard[][]��洢�ľ��ǵ�ǰ���̵�����������Ϣ,x��y����ǶԷ����һ���µ���
	
	/************************************************************************************/
	/***********�����������Ĵ��룬���߽�������������ӵ�λ�ã�����new_x��new_y��****************/
		//�����Ϊ������Ե�ʾ�����룬��ɾ��
	int available_list[81]; //�Ϸ�λ�ñ� 
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
	/***********���Ϸ������Ĵ��룬���߽�������������ӵ�λ�ã�����new_x��new_y��****************/
	/************************************************************************************/
	
	// �������JSON
	Json::Value ret;
	Json::Value action;
	action["x"] = new_x; action["y"] = new_y;
	ret["response"] = action;
	ret["debug"] = turnID;//������Ϣ��д������
	Json::FastWriter writer;

	cout << writer.write(ret) << endl;
	return 0;
}


