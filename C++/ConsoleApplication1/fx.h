#pragma once
#include <windows.h>
//定义隐藏光标函数
void HideCursor()
{
	CONSOLE_CURSOR_INFO cursor;
	cursor.bVisible = FALSE;
	cursor.dwSize = sizeof(cursor);
	HANDLE handle = GetStdHandle(STD_OUTPUT_HANDLE);
	SetConsoleCursorInfo(handle, &cursor);
}
void gotoxy(int x, int y) {//光标跳转
	HANDLE handle = GetStdHandle(STD_OUTPUT_HANDLE);
	COORD pos; pos.X = x;
	pos.Y = y;
	SetConsoleCursorPosition(handle, pos);
}