#pragma once

#include "pch.h"
#include <iostream>
#include <string>
#include <time.h>
#include "head.h" 

using namespace std;

extern qqUsersManagerXXX qqusermanage;
extern mBlogManagerXXX mbusermanage;
extern WeChatUsersManagerXXX wcusermanage;

void UserXXX::modify() {
	int temp3;
	system("cls");
	printf("     ____________________________________________________________________________________________ \n");
	printf("    ||------------------------------------------------------------------------------------------||\n");
	printf("    ||                                                                                          ||\n");
	printf("    ||                                                                                          ||\n");
	printf("    ||          +---------------------------------------------------------------------+         ||\n");
	printf("    ||          |                                                                     |         ||\n");
	printf("    ||          |                         请输入您的昵称：                            |         ||\n");
	printf("    ||          |                                                                     |         ||\n");
	printf("    ||          |                                                                     |         ||\n");
	printf("    ||          +---------------------------------------------------------------------+         ||\n");
	printf("    ||                                                                                          ||\n");
	printf("    ||                                                                                          ||\n");
	printf("    ||------------------------------------------------------------------------------------------||\n");
	printf("    ||__________________________________________________________________________________________||\n");
	cin >> name;
	do {
		system("cls");
		printf("     ____________________________________________________________________________________________ \n");
		printf("    ||------------------------------------------------------------------------------------------||\n");
		printf("    ||                                                                                          ||\n");
		printf("    ||                                                                                          ||\n");
		printf("    ||          +---------------------------------------------------------------------+         ||\n");
		printf("    ||          |                                                                     |         ||\n");
		printf("    ||          |                   请输入您的生日(8位，年月日)：                     |         ||\n");
		printf("    ||          |                                                                     |         ||\n");
		printf("    ||          |                                                                     |         ||\n");
		printf("    ||          +---------------------------------------------------------------------+         ||\n");
		printf("    ||                                                                                          ||\n");
		printf("    ||                                                                                          ||\n");
		printf("    ||------------------------------------------------------------------------------------------||\n");
		printf("    ||__________________________________________________________________________________________||\n");
		cin >> temp3;
	} while ((temp3 < 19000101) or (temp3 > 20200101) or (((temp3 % 10000) / 100) > 12) or (((temp3 % 10000) / 100) < 1) or ((temp3 % 100) > 31) or ((temp3 % 100) < 1));
	birthdate = temp3;
	system("cls");
	printf("     ____________________________________________________________________________________________ \n");
	printf("    ||------------------------------------------------------------------------------------------||\n");
	printf("    ||                                                                                          ||\n");
	printf("    ||                                                                                          ||\n");
	printf("    ||          +---------------------------------------------------------------------+         ||\n");
	printf("    ||          |                                                                     |         ||\n");
	printf("    ||          |                         请输入您的所在地：                          |         ||\n");
	printf("    ||          |                                                                     |         ||\n");
	printf("    ||          |                                                                     |         ||\n");
	printf("    ||          +---------------------------------------------------------------------+         ||\n");
	printf("    ||                                                                                          ||\n");
	printf("    ||                                                                                          ||\n");
	printf("    ||------------------------------------------------------------------------------------------||\n");
	printf("    ||__________________________________________________________________________________________||\n");

	cin >> place;
	printf("     ____________________________________________________________________________________________ \n");
	printf("    ||------------------------------------------------------------------------------------------||\n");
	printf("    ||                                                                                          ||\n");
	printf("    ||                                                                                          ||\n");
	printf("    ||          +---------------------------------------------------------------------+         ||\n");
	printf("    ||          |                                                                     |         ||\n");
	printf("    ||          |                             修改成功！                              |         ||\n");
	printf("    ||          |                                                                     |         ||\n");
	printf("    ||          |                                                                     |         ||\n");
	printf("    ||          +---------------------------------------------------------------------+         ||\n");
	printf("    ||                                                                                          ||\n");
	printf("    ||                                                                                          ||\n");
	printf("    ||------------------------------------------------------------------------------------------||\n");
	printf("    ||__________________________________________________________________________________________||\n");

}

//========================================================分界线=============================================

qqUserXXX::qqUserXXX(int i, string n, int b, string p, int d) {
	int j;
	id = i;
	name = n;
	birthdate = b;
	place = p;
	registertime = d;
	number_of_friends = 0;
	number_of_groups = 0;
	for (j = 0; j < 100; j++) { friends[j] = 0; }
	for (j = 0; j < 30; j++) { groups[j] = 0; }
	person = new personXXX;
	person->QQID(i);
	person->MBLOGID(0);
	person->WECHATID(0);
}

void qqUserXXX::AddFriend(int xid) {
	this->friends[number_of_friends] = qqusermanage.find(xid);
	number_of_friends++;
}

void qqUserXXX::DeleteFriend(int xid) {
	int i, j;
	for (i = 0; i < number_of_friends; i++) { //遍历好友列表，查询是否有此好友
		if (qqusermanage.find(xid) == friends[i]) {//查找得到
			for (j = i; j < number_of_friends; j++) { friends[j] = friends[j + 1]; } //列表前移
			friends[number_of_friends] = 0;
			number_of_friends--;
		}
	}
}

void qqUserXXX::Show() {
	int i;
	system("cls");
	printf("     ____________________________________________________________________________________________ \n");
	printf("    ||------------------------------------------------------------------------------------------||\n");
	printf("    ||                                                                                          ||\n");
	printf("    ||                                                                                          ||\n");
	printf("    ||          +---------------------------------------------------------------------+         ||\n");
	printf("    ||          |                                                                     |         ||\n");
	printf("    ||          |                         QQ号：                                      |         ||\n");
	printf("    ||          |                         QQ昵称：                                    |         ||\n");
	printf("    ||          |                         出生时间：                                  |         ||\n");
	printf("    ||          |                         注册时间：                                  |         ||\n");
	printf("    ||          |                         所在地：                                    |         ||\n");
	printf("    ||          |                         好友个数：                                  |         ||\n");
	printf("    ||          |                         群个数：                                    |         ||\n");
	printf("    ||          |                                                                     |         ||\n");
	printf("    ||          |                                                                     |         ||\n");
	printf("    ||          +---------------------------------------------------------------------+         ||\n");
	printf("    ||                                                                                          ||\n");
	printf("    ||                                                                                          ||\n");
	printf("    ||------------------------------------------------------------------------------------------||\n");
	printf("    ||__________________________________________________________________________________________||\n");
	cout << "QQ号：" << id << endl;
	cout << "QQ昵称：" << name << endl;
	cout << "出生时间：" << birthdate << endl;
	cout << "注册时间：" << registertime << endl;
	cout << "所在地：" << place << endl;
	cout << "好友个数：" << number_of_friends << endl;
	cout << "群个数：" << number_of_groups << endl;
	for (i = 0; i < number_of_friends; i++) {
		cout << "第" << i + 1 << "个好友：" << friends[i]->name << "   QQ号：" << friends[i]->ID() << endl;
	}
	for (i = 0; i < number_of_groups; i++) {
		cout << "第" << i + 1 << "个群：" << groups[i]->Name() << "   群号：" << groups[i]->gID() << endl;
	}
	system("pause");
	cout << endl;
}

void qqUserXXX::Show_Friend() {
	int i;
	cout << "当前您的QQ好友列表：" << endl;
	for (i = 0; i < number_of_friends; i++) {
		cout << "第" << i + 1 << "个好友：" << friends[i]->name << "   QQ号：" << friends[i]->ID() << endl;
	}
	cout << endl;
}

void qqUserXXX::Show_Group() {
	int i;
	cout << "当前您的群列表：" << endl;
	for (i = 0; i < number_of_groups; i++) {
		cout << "第" << i + 1 << "个群：" << groups[i]->Name() << "   群号：" << groups[i]->gID() << endl;
	}
	cout << endl;
}

void qqUserXXX::InGroup(int xid) {
	groups[number_of_groups] = qqusermanage.find2(xid);
	number_of_groups++;
}

void qqUserXXX::OutGroup(int xid) {
	int i, j;
	for (i = 0; i < number_of_groups; i++) { //遍历群列表，查询是否有此群
		if (qqusermanage.find2(xid) == groups[i]) { //查找得到
			for (j = i; j < number_of_groups; j++) { groups[j] = groups[j + 1]; } //列表前移
			groups[number_of_groups] = 0;
			number_of_groups--;
		}
	}
}

bool qqUserXXX::IsFriend(int xid) {
	int i;
	for (i = 0; i < number_of_friends; i++) { //遍历好友列表，查询是否有此好友
		if (qqusermanage.find(xid) == friends[i]) { //查找得到
			return true;
		}
	}
	return false;
}

bool qqUserXXX::IsInGroup(int xid) {
	int i;
	for (i = 0; i < number_of_groups; i++) { //遍历群列表，查询是否有此群
		if (qqusermanage.find2(xid) == groups[i]) { //查找得到
			return true;
		}
	}
	return false;
}

qqGroupXXX::qqGroupXXX(int i, string n, int x1, int d) {
	int j;
	ID = i;
	name = n;
	createtime = d;
	for (j = 0; j < 100; j++) {
		GroupMembers[j] = 0;
	}
	for (j = 0; j < 20; j++) {
		Managers[j] = 0;
	}
	for (j = 0; j < 15; j++) {
		minigroupmembers[j] = 0;
	}
	GroupMembers[0] = qqusermanage.find(x1);
	Head = qqusermanage.find(x1);//第一人为群主
	number_of_members = 1;
	number_of_managers = 0;
	number_of_minigroupmembers = 0;
}

void qqGroupXXX::Add(int xid) {
	GroupMembers[number_of_members] = qqusermanage.find(xid);
	number_of_members++;
}

void qqGroupXXX::Kick(int xid) {
	int i, j;
	for (i = 0; i < number_of_members; i++) { //遍历群成员列表，查询是否有此人
		if (qqusermanage.find(xid) == GroupMembers[i]) { //查找得到
			for (j = i; j < number_of_members; j++) { GroupMembers[j] = GroupMembers[j + 1]; } //列表前移
			GroupMembers[number_of_members] = 0;
			number_of_members--;
		}
	}
}

bool qqGroupXXX::IsHead(int xid) {
	return (qqusermanage.find(xid) == Head);
}

bool qqGroupXXX::IsManager(int xid) {
	int i;
	for (i = 0; i < number_of_managers; i++) { //遍历管理员列表，查询是否有此人
		if (qqusermanage.find(xid) == Managers[i]) return true;
	}
	return false;
}

void qqGroupXXX::BecomeManager(int xid) {
	int i;
	for (i = 0; i < number_of_members; i++) { //遍历群成员列表，查询是否有此人
		if (qqusermanage.find(xid) == GroupMembers[i]) { //查找得到
			Managers[number_of_managers] = qqusermanage.find(xid);
			number_of_managers++;
		}
	}
}

void qqGroupXXX::LostManager(int xid) {
	int i, j;
	for (i = 0; i < number_of_managers; i++) { //遍历群成员列表，查询是否有此人
		if (qqusermanage.find(xid) == Managers[i]) { //查找得到
			for (j = i; j < number_of_managers; j++) { Managers[j] = Managers[j + 1]; } //列表前移
			Managers[number_of_managers] = 0;
			number_of_managers--;
		}
	}
}

void qqGroupXXX::getinminigroup(int xid) {
	minigroupmembers[number_of_minigroupmembers] = qqusermanage.find(xid);
	number_of_minigroupmembers++;
}

void qqGroupXXX::deleteminigroup() {
	int j;
	for (j = 0; j < number_of_minigroupmembers; j++)
		minigroupmembers[j] = 0;
	number_of_minigroupmembers = 0;
}

bool qqGroupXXX::isinminigroup(int xid) {
	int i;
	for (i = 0; i < number_of_minigroupmembers; i++) { //遍历临时讨论组列表列表，查询是否有此人
		if (qqusermanage.find(xid) == minigroupmembers[i]) return true;
	}
	return false;
}

void qqGroupXXX::Show() {
	int i;
	cout << "QQ群号：" << ID << endl;
	cout << "QQ群名：" << name << endl;
	cout << "创建时间：" << createtime << endl;
	cout << "群友个数：" << number_of_members << endl;
	cout << "群主：" << Head->Name() << endl;
	for (i = 0; i < number_of_managers; i++) {
		cout << "第" << i + 1 << "个管理员：" << Managers[i]->Name() << "   QQ号：" << Managers[i]->ID() << endl;
	}
	for (i = 0; i < number_of_members; i++) {
		cout << "第" << i + 1 << "个群员：" << GroupMembers[i]->Name() << "   QQ号：" << GroupMembers[i]->ID() << endl;
	}
	if (number_of_minigroupmembers != 0) {
		cout << "本群目前有临时讨论组，以下群员在内：" << endl;
		for (i = 0; i < number_of_minigroupmembers; i++) {
			cout << minigroupmembers[i]->Name() << "   ";
		}
		cout << endl;
	}
	cout << endl;
}

int qqGroupXXX::MakemBlogGroup() {
	struct tm timenow;   //tm结构指针
	time_t now;  //声明time_t类型变量
	time(&now);      //获取系统日期和时间
	localtime_s(&timenow, &now);   //获取当地日期和时间
	int date = (timenow.tm_year + 1900) * 10000 + (timenow.tm_mon + 1) * 100 + (timenow.tm_mday);
	int newgroupid;
	int i;
	mbusermanage.AddGroup(name, Head->person->returnmBlog()->ID(), date);
	newgroupid = mbusermanage.Number_of_Groups() + 1000;
	for (i = 1; i < number_of_members; i++) {
		if (GroupMembers[i]->person->returnmBlog() != 0) {
			mbusermanage.ingroup(newgroupid, GroupMembers[i]->person->returnmBlog()->ID());
		}
	}
	return newgroupid;
}

int qqGroupXXX::MakeWeChatGroup() {
	struct tm timenow;   //tm结构指针
	time_t now;  //声明time_t类型变量
	time(&now);      //获取系统日期和时间
	localtime_s(&timenow, &now);   //获取当地日期和时间
	int date = (timenow.tm_year + 1900) * 10000 + (timenow.tm_mon + 1) * 100 + (timenow.tm_mday);
	int newgroupid;
	int i;
	wcusermanage.AddGroup(name, Head->person->returnwechat()->ID(), date);
	newgroupid = wcusermanage.Number_of_Groups() + 1000;
	for (i = 1; i < number_of_members; i++) {
		if (GroupMembers[i]->person->returnwechat() != 0) {
			wcusermanage.ingroup(newgroupid, GroupMembers[i]->person->returnwechat()->ID());
		}
	}
	return newgroupid;
}

qqUsersManagerXXX::qqUsersManagerXXX() {
	int i;
	for (i = 0; i < 200; i++) qqUsers[i] = 0;
	for (i = 0; i < 20; i++) qqGroups[i] = 0;
	for (i = 0; i < 200; i++) { friendrelations[i][0] = 0; friendrelations[i][1] = 0; }
	number_of_relations = 0;
	number_of_users = 0;
	number_of_groups = 0;
};

void qqUsersManagerXXX::AddUser(string n, int b, string p, int d) {
	int i = number_of_users + 10001;
	qqUsers[number_of_users] = new qqUserXXX(i, n, b, p, d);
	number_of_users++;
}

qqUserXXX* qqUsersManagerXXX::find(int xid) {
	int j;
	for (j = 0; j < number_of_users; j++) {
		if (qqUsers[j]->ID() == xid) return qqUsers[j];
	}
}

qqGroupXXX* qqUsersManagerXXX::find2(int xid) {
	int j;
	for (j = 0; j < number_of_groups; j++) {
		if (qqGroups[j]->gID() == xid) return qqGroups[j];
	}
}

void qqUsersManagerXXX::AddGroup(string n, int x1, int d) {
	int i = number_of_groups + 1001;
	qqGroups[number_of_groups] = new qqGroupXXX(i, n, x1, d);
	number_of_groups++;
	find(x1)->InGroup(i);
}

bool qqUsersManagerXXX::Searching(int xid) {
	int j;
	for (j = 0; j < number_of_users; j++) {
		if (qqUsers[j]->ID() == xid) {
			if (qqUsers[j]->opened == true)
				return true;
			else return false;
		}
	}
	return false;
}

bool qqUsersManagerXXX::Searching2(int gid) {
	int j;
	for (j = 0; j < number_of_groups; j++) {
		if (qqGroups[j]->gID() == gid) return true;
	}
	return false;
}

void qqUsersManagerXXX::open(int xid) {
	find(xid)->opened = true;
	struct tm timenow;   //tm结构指针
	time_t now;  //声明time_t类型变量
	time(&now);      //获取系统日期和时间
	localtime_s(&timenow, &now);   //获取当地日期和时间
	int date_now = (timenow.tm_year + 1900) * 10000 + (timenow.tm_mon + 1) * 100 + (timenow.tm_mday);
	find(xid)->RegisterTime(date_now);
}

void qqUsersManagerXXX::becomefriends(int x1, int x2) {
	find(x1)->AddFriend(x2);
	find(x2)->AddFriend(x1);
	friendrelations[number_of_relations][0] = find(x1)->ID();
	friendrelations[number_of_relations][1] = find(x2)->ID();
	number_of_relations++;
}

void qqUsersManagerXXX::deletefriends(int x1, int x2) {
	find(x1)->DeleteFriend(x2);
	find(x2)->DeleteFriend(x1);
	for (int i = 0; i < number_of_relations; i++) {
		if (((x1 == friendrelations[i][0]) && (x1 == friendrelations[i][1])) || ((x1 == friendrelations[i][0]) && (x1 == friendrelations[i][1])))
			for (int j = i; j < number_of_relations; j++) {
				friendrelations[j][0] = friendrelations[j + 1][0];
				friendrelations[j][1] = friendrelations[j + 1][1];
			}
		friendrelations[number_of_relations][0] = 0;
		friendrelations[number_of_relations][1] = 0;
		number_of_relations--;
		break;
	}
}

//===============================分界线===============================================================

mBlogUserXXX::mBlogUserXXX(int i, string n, int b, string p, int d) {
	int j;
	id = i;
	name = n;
	birthdate = b;
	place = p;
	registertime = d;
	number_of_friends = 0;
	number_of_groups = 0;
	for (j = 0; j < 100; j++) { friends[j] = 0; }
	for (j = 0; j < 30; j++) { groups[j] = 0; }
	person = new personXXX;
	person->MBLOGID(i);
	person->QQID(0);
	person->WECHATID(0);
}

void mBlogUserXXX::AddFriend(int xid) {
	this->friends[number_of_friends] = mbusermanage.find(xid);
	number_of_friends++;
}

void mBlogUserXXX::DeleteFriend(int xid) {
	int i, j;
	for (i = 0; i < number_of_friends; i++) { //遍历好友列表，查询是否有此好友
		if (mbusermanage.find(xid) == friends[i]) {//查找得到
			for (j = i; j < number_of_friends; j++) { friends[j] = friends[j + 1]; } //列表前移
			friends[number_of_friends] = 0;
			number_of_friends--;
		}
	}
}

void mBlogUserXXX::Show() {
	int i;
	cout << "微博ID：" << id << endl;
	cout << "微博昵称：" << name << endl;
	cout << "出生时间：" << birthdate << endl;
	cout << "注册时间：" << registertime << endl;
	cout << "所在地：" << place << endl;
	cout << "好友个数：" << number_of_friends << endl;
	cout << "群个数：" << number_of_groups << endl;
	for (i = 0; i < number_of_friends; i++) {
		cout << "第" << i + 1 << "个好友：" << friends[i]->name << "   微博ID：" << friends[i]->ID() << endl;
	}
	for (i = 0; i < number_of_groups; i++) {
		cout << "第" << i + 1 << "个群：" << groups[i]->Name() << "   群号：" << groups[i]->gID() << endl;
	}
	cout << endl;
}

void mBlogUserXXX::Show_Friend() {
	int i;
	cout << "当前您的微博好友列表：" << endl;
	for (i = 0; i < number_of_friends; i++) {
		cout << "第" << i + 1 << "个好友：" << friends[i]->name << "   微博ID：" << friends[i]->ID() << endl;
	}
	cout << endl;
}

void mBlogUserXXX::Show_Group() {
	int i;
	cout << "当前您的群列表：" << endl;
	for (i = 0; i < number_of_groups; i++) {
		cout << "第" << i + 1 << "个群：" << groups[i]->Name() << "   群号：" << groups[i]->gID() << endl;
	}
	cout << endl;
}

void mBlogUserXXX::InGroup(int xid) {
	groups[number_of_groups] = mbusermanage.find2(xid);
	number_of_groups++;
}

void mBlogUserXXX::OutGroup(int xid) {
	int i, j;
	for (i = 0; i < number_of_groups; i++) { //遍历群列表，查询是否有此群
		if (mbusermanage.find2(xid) == groups[i]) { //查找得到
			for (j = i; j < number_of_groups; j++) { groups[j] = groups[j + 1]; } //列表前移
			groups[number_of_groups] = 0;
			number_of_groups--;
		}
	}
}

bool mBlogUserXXX::IsFriend(int xid) {
	int i;
	for (i = 0; i < number_of_friends; i++) { //遍历好友列表，查询是否有此好友
		if (mbusermanage.find(xid) == friends[i]) { //查找得到
			return true;
		}
	}
	return false;
}

bool mBlogUserXXX::IsInGroup(int xid) {
	int i;
	for (i = 0; i < number_of_groups; i++) { //遍历群列表，查询是否有此群
		if (mbusermanage.find2(xid) == groups[i]) { //查找得到
			return true;
		}
	}
	return false;
}


mBlogGroupXXX::mBlogGroupXXX(int i, string n, int x1, int d) {
	int j;
	ID = i;
	name = n;
	createtime = d;
	for (j = 0; j < 100; j++) {
		GroupMembers[j] = 0;
	}
	GroupMembers[0] = mbusermanage.find(x1);
	Head = mbusermanage.find(x1);//第一人为群主
	number_of_members = 1;
}

void mBlogGroupXXX::Add(int xid) {
	GroupMembers[number_of_members] = mbusermanage.find(xid);
	number_of_members++;
}

void mBlogGroupXXX::Kick(int xid) {
	int i, j;
	for (i = 0; i < number_of_members; i++) { //遍历群成员列表，查询是否有此人
		if (mbusermanage.find(xid) == GroupMembers[i]) { //查找得到
			for (j = i; j < number_of_members; j++) { GroupMembers[j] = GroupMembers[j + 1]; } //列表前移
			GroupMembers[number_of_members] = 0;
			number_of_members--;
		}
	}
}

bool mBlogGroupXXX::IsHead(int xid) {
	return (mbusermanage.find(xid) == Head);
}

void mBlogGroupXXX::Show() {
	int i;
	cout << "微博群ID：" << ID << endl;
	cout << "微博群名：" << name << endl;
	cout << "创建时间：" << createtime << endl;
	cout << "群友个数：" << number_of_members << endl;
	cout << "群主：" << Head->Name() << endl;
	for (i = 0; i < number_of_members; i++) {
		cout << "第" << i + 1 << "个群员：" << GroupMembers[i]->Name() << "   微博ID：" << GroupMembers[i]->ID() << endl;
	}
	cout << endl;
}

int mBlogGroupXXX::MakeQQGroup() {
	struct tm timenow;   //tm结构指针
	time_t now;  //声明time_t类型变量
	time(&now);      //获取系统日期和时间
	localtime_s(&timenow, &now);   //获取当地日期和时间
	int date = (timenow.tm_year + 1900) * 10000 + (timenow.tm_mon + 1) * 100 + (timenow.tm_mday);
	int newgroupid;
	int i;
	qqusermanage.AddGroup(name, Head->person->returnqq()->ID(), date);
	newgroupid = qqusermanage.Number_of_Groups() + 1000;
	for (i = 1; i < number_of_members; i++) {
		if (GroupMembers[i]->person->returnqq() != 0) {
			qqusermanage.ingroup(newgroupid, GroupMembers[i]->person->returnqq()->ID());
		}
	}
	return newgroupid;
}

int mBlogGroupXXX::MakeWeChatGroup() {
	struct tm timenow;   //tm结构指针
	time_t now;  //声明time_t类型变量
	time(&now);      //获取系统日期和时间
	localtime_s(&timenow, &now);   //获取当地日期和时间
	int date = (timenow.tm_year + 1900) * 10000 + (timenow.tm_mon + 1) * 100 + (timenow.tm_mday);
	int newgroupid;
	int i;
	wcusermanage.AddGroup(name, Head->person->returnwechat()->ID(), date);
	newgroupid = wcusermanage.Number_of_Groups() + 1000;
	for (i = 1; i < number_of_members; i++) {
		if (GroupMembers[i]->person->returnwechat() != 0) {
			wcusermanage.ingroup(newgroupid, GroupMembers[i]->person->returnwechat()->ID());
		}
	}
	return newgroupid;
}

mBlogManagerXXX::mBlogManagerXXX() {
	int i;
	for (i = 0; i < 200; i++) mbUsers[i] = 0;
	for (i = 0; i < 20; i++) mbGroups[i] = 0;
	for (i = 0; i < 200; i++) { friendrelations[i][0] = 0; friendrelations[i][1] = 0; }
	number_of_relations = 0;
	number_of_users = 0;
	number_of_groups = 0;
};

void mBlogManagerXXX::AddUser(string n, int b, string p, int d) {
	int i = number_of_users + 10001;
	mbUsers[number_of_users] = new mBlogUserXXX(i, n, b, p, d);
	number_of_users++;
}

mBlogUserXXX* mBlogManagerXXX::find(int xid) {
	int j;
	for (j = 0; j < number_of_users; j++) {
		if (mbUsers[j]->ID() == xid) return mbUsers[j];
	}
}

mBlogGroupXXX* mBlogManagerXXX::find2(int xid) {
	int j;
	for (j = 0; j < number_of_groups; j++) {
		if (mbGroups[j]->gID() == xid) return mbGroups[j];
	}
}

void mBlogManagerXXX::AddGroup(string n, int x1, int d) {
	int i = number_of_groups + 1001;
	mbGroups[number_of_groups] = new mBlogGroupXXX(i, n, x1, d);
	number_of_groups++;
	find(x1)->InGroup(i);
}

bool mBlogManagerXXX::Searching(int xid) {
	int j;
	for (j = 0; j < number_of_users; j++) {
		if (mbUsers[j]->ID() == xid) {
			if (mbUsers[j]->opened == true)
				return true;
			else return false;
		}
	}
	return false;
}

bool mBlogManagerXXX::Searching2(int gid) {
	int j;
	for (j = 0; j < number_of_groups; j++) {
		if (mbGroups[j]->gID() == gid) return true;
	}
	return false;
}

void mBlogManagerXXX::open(int xid) {
	find(xid)->opened = true;
	struct tm timenow;   //tm结构指针
	time_t now;  //声明time_t类型变量
	time(&now);      //获取系统日期和时间
	localtime_s(&timenow, &now);   //获取当地日期和时间
	int date_now = (timenow.tm_year + 1900) * 10000 + (timenow.tm_mon + 1) * 100 + (timenow.tm_mday);
	find(xid)->RegisterTime(date_now);
}

void mBlogManagerXXX::becomefriends(int x1, int x2) {
	find(x1)->AddFriend(x2);
	find(x2)->AddFriend(x1);
	friendrelations[number_of_relations][0] = find(x1)->ID();
	friendrelations[number_of_relations][1] = find(x2)->ID();
	number_of_relations++;
}

void mBlogManagerXXX::deletefriends(int x1, int x2) {
	find(x1)->DeleteFriend(x2);
	find(x2)->DeleteFriend(x1);
	for (int i = 0; i < number_of_relations; i++) {
		if (((x1 == friendrelations[i][0]) && (x1 == friendrelations[i][1])) || ((x1 == friendrelations[i][0]) && (x1 == friendrelations[i][1])))
			for (int j = i; j < number_of_relations; j++) {
				friendrelations[j][0] = friendrelations[j + 1][0];
				friendrelations[j][1] = friendrelations[j + 1][1];
			}
		friendrelations[number_of_relations][0] = 0;
		friendrelations[number_of_relations][1] = 0;
		number_of_relations--;
		break;
	}
}

//========================================分割线=======================================================

WeChatUserXXX::WeChatUserXXX(int i, string n, int b, string p, int d) {
	int j;
	id = i;
	name = n;
	birthdate = b;
	place = p;
	registertime = d;
	number_of_friends = 0;
	number_of_groups = 0;
	for (j = 0; j < 100; j++) { friends[j] = 0; }
	for (j = 0; j < 30; j++) { groups[j] = 0; }
	person = new personXXX;
	person->WECHATID(i);
	person->QQID(0);
	person->MBLOGID(0);
}

void WeChatUserXXX::AddFriend(int xid) {
	this->friends[number_of_friends] = wcusermanage.find(xid);
	number_of_friends++;
}

void WeChatUserXXX::DeleteFriend(int xid) {
	int i, j;
	for (i = 0; i < number_of_friends; i++) { //遍历好友列表，查询是否有此好友
		if (wcusermanage.find(xid) == friends[i]) {//查找得到
			for (j = i; j < number_of_friends; j++) { friends[j] = friends[j + 1]; } //列表前移
			friends[number_of_friends] = 0;
			number_of_friends--;
		}
	}
}

void WeChatUserXXX::Show() {
	int i;
	cout << "微信ID：" << id << endl;
	cout << "微信昵称：" << name << endl;
	cout << "出生时间：" << birthdate << endl;
	cout << "注册时间：" << registertime << endl;
	cout << "所在地：" << place << endl;
	cout << "好友个数：" << number_of_friends << endl;
	cout << "群个数：" << number_of_groups << endl;
	for (i = 0; i < number_of_friends; i++) {
		cout << "第" << i + 1 << "个好友：" << friends[i]->name << "   微信ID：" << friends[i]->ID() << endl;
	}
	for (i = 0; i < number_of_groups; i++) {
		cout << "第" << i + 1 << "个群：" << groups[i]->Name() << "   群号：" << groups[i]->gID() << endl;
	}
	cout << endl;
}

void WeChatUserXXX::Show_Friend() {
	int i;
	cout << "当前您的微信好友列表：" << endl;
	for (i = 0; i < number_of_friends; i++) {
		cout << "第" << i + 1 << "个好友：" << friends[i]->name << "   微信ID：" << friends[i]->ID() << endl;
	}
	cout << endl;
}

void WeChatUserXXX::Show_Group() {
	int i;
	cout << "当前您的群列表：" << endl;
	for (i = 0; i < number_of_groups; i++) {
		cout << "第" << i + 1 << "个群：" << groups[i]->Name() << "   群号：" << groups[i]->gID() << endl;
	}
	cout << endl;
}

void WeChatUserXXX::InGroup(int xid) {
	groups[number_of_groups] = wcusermanage.find2(xid);
	number_of_groups++;
}

void WeChatUserXXX::OutGroup(int xid) {
	int i, j;
	for (i = 0; i < number_of_groups; i++) { //遍历群列表，查询是否有此群
		if (wcusermanage.find2(xid) == groups[i]) { //查找得到
			for (j = i; j < number_of_groups; j++) { groups[j] = groups[j + 1]; } //列表前移
			groups[number_of_groups] = 0;
			number_of_groups--;
		}
	}
}

bool WeChatUserXXX::IsFriend(int xid) {
	int i;
	for (i = 0; i < number_of_friends; i++) { //遍历好友列表，查询是否有此好友
		if (wcusermanage.find(xid) == friends[i]) { //查找得到
			return true;
		}
	}
	return false;
}

bool WeChatUserXXX::IsInGroup(int xid) {
	int i;
	for (i = 0; i < number_of_groups; i++) { //遍历群列表，查询是否有此群
		if (wcusermanage.find2(xid) == groups[i]) { //查找得到
			return true;
		}
	}
	return false;
}


WeChatGroupXXX::WeChatGroupXXX(int i, string n, int x1, int d) {
	int j;
	ID = i;
	name = n;
	createtime = d;
	for (j = 0; j < 100; j++) {
		GroupMembers[j] = 0;
	}
	GroupMembers[0] = wcusermanage.find(x1);
	Head = wcusermanage.find(x1);//第一人为群主
	number_of_members = 1;
}

void WeChatGroupXXX::Add(int xid) {
	GroupMembers[number_of_members] = wcusermanage.find(xid);
	number_of_members++;
}

void WeChatGroupXXX::Kick(int xid) {
	int i, j;
	for (i = 0; i < number_of_members; i++) { //遍历群成员列表，查询是否有此人
		if (wcusermanage.find(xid) == GroupMembers[i]) { //查找得到
			for (j = i; j < number_of_members; j++) { GroupMembers[j] = GroupMembers[j + 1]; } //列表前移
			GroupMembers[number_of_members] = 0;
			number_of_members--;
		}
	}
}

bool WeChatGroupXXX::IsHead(int xid) {
	return (wcusermanage.find(xid) == Head);
}

void WeChatGroupXXX::Show() {
	int i;
	cout << "微信群ID：" << ID << endl;
	cout << "微信群名：" << name << endl;
	cout << "创建时间：" << createtime << endl;
	cout << "群友个数：" << number_of_members << endl;
	cout << "群主：" << Head->Name() << endl;
	for (i = 0; i < number_of_members; i++) {
		cout << "第" << i + 1 << "个群员：" << GroupMembers[i]->Name() << "   微信ID：" << GroupMembers[i]->ID() << endl;
	}
	cout << endl;
}

int WeChatGroupXXX::MakeQQGroup() {
	struct tm timenow;   //tm结构指针
	time_t now;  //声明time_t类型变量
	time(&now);      //获取系统日期和时间
	localtime_s(&timenow, &now);   //获取当地日期和时间
	int date = (timenow.tm_year + 1900) * 10000 + (timenow.tm_mon + 1) * 100 + (timenow.tm_mday);
	int newgroupid;
	int i;
	qqusermanage.AddGroup(name, Head->person->returnqq()->ID(), date);
	newgroupid = qqusermanage.Number_of_Groups() + 1000;
	for (i = 1; i < number_of_members; i++) {
		if (GroupMembers[i]->person->returnqq() != 0) {
			qqusermanage.ingroup(newgroupid, GroupMembers[i]->person->returnqq()->ID());
		}
	}
	return newgroupid;
}

int WeChatGroupXXX::MakemBlogGroup() {
	struct tm timenow;   //tm结构指针
	time_t now;  //声明time_t类型变量
	time(&now);      //获取系统日期和时间
	localtime_s(&timenow, &now);   //获取当地日期和时间
	int date = (timenow.tm_year + 1900) * 10000 + (timenow.tm_mon + 1) * 100 + (timenow.tm_mday);
	int newgroupid;
	int i;
	mbusermanage.AddGroup(name, Head->person->returnmBlog()->ID(), date);
	newgroupid = mbusermanage.Number_of_Groups() + 1000;
	for (i = 1; i < number_of_members; i++) {
		if (GroupMembers[i]->person->returnmBlog() != 0) {
			mbusermanage.ingroup(newgroupid, GroupMembers[i]->person->returnmBlog()->ID());
		}
	}
	return newgroupid;
}


WeChatUsersManagerXXX::WeChatUsersManagerXXX() {
	int i;
	for (i = 0; i < 200; i++) WeChatUsers[i] = 0;
	for (i = 0; i < 20; i++) WeChatGroups[i] = 0;
	for (i = 0; i < 200; i++) { friendrelations[i][0] = 0; friendrelations[i][1] = 0; }
	number_of_relations = 0;
	number_of_users = 0;
	number_of_groups = 0;
};

void WeChatUsersManagerXXX::AddUser(string n, int b, string p, int d) {
	int i = number_of_users + 20001;
	WeChatUsers[number_of_users] = new WeChatUserXXX(i, n, b, p, d);
	number_of_users++;
}

WeChatUserXXX* WeChatUsersManagerXXX::find(int xid) {
	int j;
	for (j = 0; j < number_of_users; j++) {
		if (WeChatUsers[j]->ID() == xid) return WeChatUsers[j];
	}
}

WeChatGroupXXX* WeChatUsersManagerXXX::find2(int xid) {
	int j;
	for (j = 0; j < number_of_groups; j++) {
		if (WeChatGroups[j]->gID() == xid) return WeChatGroups[j];
	}
}

void WeChatUsersManagerXXX::AddGroup(string n, int x1, int d) {
	int i = number_of_groups + 1001;
	WeChatGroups[number_of_groups] = new WeChatGroupXXX(i, n, x1, d);
	number_of_groups++;
	find(x1)->InGroup(i);
}

bool WeChatUsersManagerXXX::Searching(int xid) {
	int j;
	for (j = 0; j < number_of_users; j++) {
		if (WeChatUsers[j]->ID() == xid) return true;
	}
	return false;
}

bool WeChatUsersManagerXXX::Searching2(int gid) {
	int j;
	for (j = 0; j < number_of_groups; j++) {
		if (WeChatGroups[j]->gID() == gid) return true;
	}
	return false;
}

void WeChatUsersManagerXXX::becomefriends(int x1, int x2) {
	find(x1)->AddFriend(x2);
	find(x2)->AddFriend(x1);
	friendrelations[number_of_relations][0] = find(x1)->ID();
	friendrelations[number_of_relations][1] = find(x2)->ID();
	number_of_relations++;
}

void WeChatUsersManagerXXX::deletefriends(int x1, int x2) {
	find(x1)->DeleteFriend(x2);
	find(x2)->DeleteFriend(x1);
	for (int i = 0; i < number_of_relations; i++) {
		if (((x1 == friendrelations[i][0]) && (x1 == friendrelations[i][1])) || ((x1 == friendrelations[i][0]) && (x1 == friendrelations[i][1])))
			for (int j = i; j < number_of_relations; j++) {
				friendrelations[j][0] = friendrelations[j + 1][0];
				friendrelations[j][1] = friendrelations[j + 1][1];
			}
		friendrelations[number_of_relations][0] = 0;
		friendrelations[number_of_relations][1] = 0;
		number_of_relations--;
		break;
	}
}


//========================================分割线=======================================================

qqUserXXX* personXXX::returnqq() {
	if (qqid == 0) return 0;
	return qqusermanage.find(qqid);
}

mBlogUserXXX* personXXX::returnmBlog() {
	if (mBlogid == 0) return 0;
	return mbusermanage.find(mBlogid);
}

WeChatUserXXX* personXXX::returnwechat() {
	if (Wechatid == 0) return 0;
	return wcusermanage.find(Wechatid);
}

//============================================分界线========================
string qqUsersManagerXXX::writetofile() {
	string all;
	int i;
	ostringstream ss1, ss2;
	all = "";
	ss1 << number_of_users;
	all += ss1.str() + "\n";
	for (i = 0; i < number_of_users; i++)
		all += qqUsers[i]->write() + "\n";
	ss1.str("");
	for (i = 0; i < number_of_relations; i++) {
		ss1 << friendrelations[i][0];
		ss2 << friendrelations[i][1];
		all += ss1.str() + " " + ss2.str() + "\n";
		ss1.str("");
		ss2.str("");
	}
	all += "0";
	all += "\n";
	ss1.str("");
	ss1 << number_of_groups;
	all += ss1.str();
	all += "\n";
	for (i = 0; i < number_of_groups; i++)
		all += qqGroups[i]->write1() + "\n";
	for (i = 0; i < number_of_groups; i++)
		all += qqGroups[i]->write2();
	all += "0";
	all += "\n";
	for (i = 0; i < number_of_groups; i++)
		all += qqGroups[i]->write3();
	all += "0";
	all += "\n";
	return all;
}

string qqUserXXX::write() {
	ostringstream ss1, ss2;
	ss1 << birthdate;
	ss2 << registertime;
	if (opened) return name + " " + ss1.str() + " " + place + " " + ss2.str() + " " + "1";
	else return name + " " + ss1.str() + " " + place + " " + ss2.str() + " " + "0";
}

string qqGroupXXX::write1() {
	ostringstream ss1, ss2;
	ss1 << createtime;
	ss2 << Head->ID();
	return name + " " + ss2.str() + " " + ss1.str();
}

string qqGroupXXX::write2() {
	ostringstream ss1, ss2;
	string s1 = "";
	ss1 << ID;
	int i;
	for (i = 1; i < number_of_members; i++) {
		ss2.str("");
		ss2 << GroupMembers[i]->ID();
		s1 = s1 + ss1.str() + " " + ss2.str() + "\n";
	}
	return s1;
}

string qqGroupXXX::write3() {
	ostringstream ss1, ss2;
	string s1 = "";
	ss1 << ID;
	int i;
	for (i = 0; i < number_of_managers; i++) {
		ss2.str("");
		ss2 << Managers[i]->ID();
		s1 = s1 + ss1.str() + " " + ss2.str() + "\n";
	}
	return s1;
}

string mBlogManagerXXX::writetofile() {
	string all;
	int i;
	ostringstream ss1, ss2;
	all = "";
	ss1 << number_of_users;
	all += ss1.str() + "\n";
	for (i = 0; i < number_of_users; i++)
		all += mbUsers[i]->write() + "\n";
	ss1.str("");
	for (i = 0; i < number_of_relations; i++) {
		ss1 << friendrelations[i][0];
		ss2 << friendrelations[i][1];
		all += ss1.str() + " " + ss2.str() + "\n";
		ss1.str("");
		ss2.str("");
	}
	all += "0";
	all += "\n";
	ss1.str("");
	ss1 << number_of_groups;
	all += ss1.str();
	all += "\n";
	for (i = 0; i < number_of_groups; i++)
		all += mbGroups[i]->write1() + "\n";
	for (i = 0; i < number_of_groups; i++)
		all += mbGroups[i]->write2();
	all += "0";
	all += "\n";
	return all;
}

string mBlogUserXXX::write() {
	ostringstream ss1, ss2;
	ss1 << birthdate;
	ss2 << registertime;
	if (opened) return name + " " + ss1.str() + " " + place + " " + ss2.str() + " " + "1";
	else return name + " " + ss1.str() + " " + place + " " + ss2.str() + " " + "0";
}

string mBlogGroupXXX::write1() {
	ostringstream ss1, ss2;
	ss1 << createtime;
	ss2 << Head->ID();
	return name + " " + ss2.str() + " " + ss1.str();
}

string mBlogGroupXXX::write2() {
	ostringstream ss1, ss2;
	string s1 = "";
	ss1 << ID;
	int i;
	for (i = 1; i < number_of_members; i++) {
		ss2.str("");
		ss2 << GroupMembers[i]->ID();
		s1 = s1 + ss1.str() + " " + ss2.str() + "\n";
	}
	return s1;
}

string WeChatUsersManagerXXX::writetofile() {
	string all;
	int i;
	ostringstream ss1, ss2;
	all = "";
	ss1 << number_of_users;
	all += ss1.str() + "\n";
	for (i = 0; i < number_of_users; i++)
		all += WeChatUsers[i]->write() + "\n";
	ss1.str("");
	for (i = 0; i < number_of_relations; i++) {
		ss1 << friendrelations[i][0];
		ss2 << friendrelations[i][1];
		all += ss1.str() + " " + ss2.str() + "\n";
		ss1.str("");
		ss2.str("");
	}
	all += "0";
	all += "\n";
	ss1.str("");
	ss1 << number_of_groups;
	all += ss1.str();
	all += "\n";
	for (i = 0; i < number_of_groups; i++)
		all += WeChatGroups[i]->write1() + "\n";
	for (i = 0; i < number_of_groups; i++)
		all += WeChatGroups[i]->write2();
	all += "0";
	all += "\n";
	return all;
}

string WeChatUserXXX::write() {
	ostringstream ss1, ss2;
	ss1 << birthdate;
	ss2 << registertime;
	return name + " " + ss1.str() + " " + place + " " + ss2.str();
}

string WeChatGroupXXX::write1() {
	ostringstream ss1, ss2;
	ss1 << createtime;
	ss2 << Head->ID();
	return name + " " + ss2.str() + " " + ss1.str();
}

string WeChatGroupXXX::write2() {
	ostringstream ss1, ss2;
	string s1 = "";
	ss1 << ID;
	int i;
	for (i = 1; i < number_of_members; i++) {
		ss2.str("");
		ss2 << GroupMembers[i]->ID();
		s1 = s1 + ss1.str() + " " + ss2.str() + "\n";
	}
	return s1;
}

string qqUsersManagerXXX::writetofile2() {
	string all = "";
	int i;
	ostringstream ss1, ss2;
	for (i = 0; i < number_of_users; i++) {
		if (qqUsers[i]->person->returnmBlog() != 0) {
			ss1.str("");
			ss2.str("");
			ss1 << qqUsers[i]->ID();
			ss2 << qqUsers[i]->person->returnmBlog()->ID();
			all = all + ss1.str() + " " + ss2.str() + "\n";
		}
	}
	all += "0";
	all += "\n";
	for (i = 0; i < number_of_users; i++) {
		if (qqUsers[i]->person->returnwechat() != 0) {
			ss1.str("");
			ss2.str("");
			ss1 << qqUsers[i]->ID();
			ss2 << qqUsers[i]->person->returnwechat()->ID();
			all = all + ss1.str() + " " + ss2.str() + "\n";
		}
	}
	all += "0";
	all += "\n";
	return all;
}

string mBlogManagerXXX::writetofile2() {
	string all = "";
	int i;
	ostringstream ss1, ss2;
	for (i = 0; i < number_of_users; i++) {
		if (mbUsers[i]->person->returnmBlog() != 0) {
			ss1.str("");
			ss2.str("");
			ss1 << mbUsers[i]->ID();
			ss2 << mbUsers[i]->person->returnmBlog()->ID();
			all = all + ss1.str() + " " + ss2.str() + "\n";
		}
	}
	all += "0";
	all += "\n";
	for (i = 0; i < number_of_users; i++) {
		if (mbUsers[i]->person->returnwechat() != 0) {
			ss1.str("");
			ss2.str("");
			ss1 << mbUsers[i]->ID();
			ss2 << mbUsers[i]->person->returnwechat()->ID();
			all = all + ss1.str() + " " + ss2.str() + "\n";
		}
	}
	all += "0";
	all += "\n";
	return all;
}

string WeChatUsersManagerXXX::writetofile2() {
	string all = "";
	int i;
	ostringstream ss1, ss2;
	for (i = 0; i < number_of_users; i++) {
		if (WeChatUsers[i]->person->returnqq() != 0) {
			ss1.str("");
			ss2.str("");
			ss1 << WeChatUsers[i]->ID();
			ss2 << WeChatUsers[i]->person->returnqq()->ID();
			all = all + ss1.str() + " " + ss2.str() + "\n";
		}
	}
	all += "0";
	all += "\n";
	for (i = 0; i < number_of_users; i++) {
		if (WeChatUsers[i]->person->returnmBlog() != 0) {
			ss1.str("");
			ss2.str("");
			ss1 << WeChatUsers[i]->ID();
			ss2 << WeChatUsers[i]->person->returnmBlog()->ID();
			all = all + ss1.str() + " " + ss2.str() + "\n";
		}
	}
	all += "0";
	all += "\n";
	return all;
}
