#include "pch.h"
#include <iostream>
#include <string>
#include <time.h>
#include "basic.h" 
using namespace std;

extern QQUsersManagerNo a1;
extern MicroBlogManagerNo b1;
extern WeChatUserManagerNo c1;

void UserNo::modify() {
	int temp3;
	cout << "请输入您的昵称：" << endl;
	cin >> name;
	do {
		cout << "请输入您的生日(8位，年月日)：" << endl;
		cin >> temp3;
	} while ((temp3 < 19000101) or (temp3 > 20200101) or (((temp3 % 10000) / 100) > 12) or (((temp3 % 10000) / 100) < 1) or ((temp3 % 100) > 31) or ((temp3 % 100) < 1));
	birthdate = temp3;
	cout << "请输入您的所在地：" << endl;
	cin >> place;
	cout << "修改成功！" << endl;
}

//========================================================分界线=============================================

QQUserNo::QQUserNo(int i, string n, int b, string p, int d){
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
	person = new personNo;
	person->QQID(i);
	person->MBLOGID(0);
	person->WECHATID(0);
}

void QQUserNo::AddFriend(int xid) {
	this->friends[number_of_friends] = a1.find(xid);
	number_of_friends++;
}

void QQUserNo::DeleteFriend(int xid) {
	int i, j;
	for (i = 0; i < number_of_friends; i++) { //遍历好友列表，查询是否有此好友
		if (a1.find(xid) == friends[i]) {//查找得到
			for (j = i; j < number_of_friends; j++) { friends[j] = friends[j + 1]; } //列表前移
			friends[number_of_friends] = 0;
			number_of_friends--;
		}
	}
}

void QQUserNo::Show() {
	int i;
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
	cout << endl;
}

void QQUserNo::Show_Friend() {
	int i;
	cout << "当前您的QQ好友列表：" << endl;
	for (i = 0; i < number_of_friends; i++) {
		cout << "第" << i + 1 << "个好友：" << friends[i]->name << "   QQ号：" << friends[i]->ID() << endl;
	}
	cout << endl;
}

void QQUserNo::Show_Group() {
	int i;
	cout << "当前您的群列表：" << endl;
	for (i = 0; i < number_of_groups; i++) {
		cout << "第" << i + 1 << "个群：" << groups[i]->Name() << "   群号：" << groups[i]->gID() << endl;
	}
	cout << endl;
}

void QQUserNo::InGroup(int xid) {
	groups[number_of_groups] = a1.find2(xid);
	number_of_groups++;
}

void QQUserNo::OutGroup(int xid) {
	int i, j;
	for (i = 0; i < number_of_groups; i++) { //遍历群列表，查询是否有此群
		if (a1.find2(xid) == groups[i]) { //查找得到
			for (j = i; j < number_of_groups; j++) { groups[j] = groups[j + 1]; } //列表前移
			groups[number_of_groups] = 0;
			number_of_groups--;
		}
	}
}

bool QQUserNo::IsFriend(int xid) {
	int i;
	for (i = 0; i < number_of_friends; i++) { //遍历好友列表，查询是否有此好友
		if (a1.find(xid) == friends[i]) { //查找得到
			return true;
		}
	}
	return false;
}

bool QQUserNo::IsInGroup(int xid) {
	int i;
	for (i = 0; i < number_of_groups; i++) { //遍历群列表，查询是否有此群
		if (a1.find2(xid) == groups[i]) { //查找得到
			return true;
		}
	}
	return false;
}

qqGroupNo::qqGroupNo(int i, string n, int x1, int d) {
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
	GroupMembers[0] = a1.find(x1);
	Head = a1.find(x1);//第一人为群主
	number_of_members = 1;
	number_of_managers = 0;
	number_of_minigroupmembers = 0;
}

void qqGroupNo::Add(int xid) {
	GroupMembers[number_of_members] = a1.find(xid);
	number_of_members++;
}

void qqGroupNo::Kick(int xid) {
	int i, j;
	for (i = 0; i < number_of_members; i++) { //遍历群成员列表，查询是否有此人
		if (a1.find(xid) == GroupMembers[i]) { //查找得到
			for (j = i; j < number_of_members; j++) { GroupMembers[j] = GroupMembers[j + 1]; } //列表前移
			GroupMembers[number_of_members] = 0;
			number_of_members--;
		}
	}
}

bool qqGroupNo::IsHead(int xid) {
	return (a1.find(xid) == Head);
}

bool qqGroupNo::IsManager(int xid) {
	int i;
	for (i = 0; i < number_of_managers; i++) { //遍历管理员列表，查询是否有此人
		if (a1.find(xid) == Managers[i]) return true;
	}
	return false;
}

void qqGroupNo::BecomeManager(int xid) {
	int i;
	for (i = 0; i < number_of_members; i++) { //遍历群成员列表，查询是否有此人
		if (a1.find(xid) == GroupMembers[i]) { //查找得到
			Managers[number_of_managers] = a1.find(xid);
			number_of_managers++;
		}
	}
}

void qqGroupNo::LostManager(int xid) {
	int i, j;
	for (i = 0; i < number_of_managers; i++) { //遍历群成员列表，查询是否有此人
		if (a1.find(xid) == Managers[i]) { //查找得到
			for (j = i; j < number_of_managers; j++) { Managers[j] = Managers[j + 1]; } //列表前移
			Managers[number_of_managers] = 0;
			number_of_managers--;
		}
	}
}

void qqGroupNo::getinminigroup(int xid) {
	minigroupmembers[number_of_minigroupmembers] = a1.find(xid);
	number_of_minigroupmembers++;
}

void qqGroupNo::deleteminigroup() {
	int j;
	for (j = 0; j < number_of_minigroupmembers; j++)
		minigroupmembers[j]= 0;	
	number_of_minigroupmembers = 0;
}

bool qqGroupNo::isinminigroup(int xid) {
	int i;
	for (i = 0; i < number_of_minigroupmembers; i++) { //遍历临时讨论组列表列表，查询是否有此人
		if (a1.find(xid) == minigroupmembers[i]) return true;
	}
	return false;
}

void qqGroupNo::Show() {
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

int qqGroupNo::MakeMicroBlogGroup() {
	struct tm timenow;   //tm结构指针
	time_t now;  //声明time_t类型变量
	time(&now);      //获取系统日期和时间
	localtime_s(&timenow, &now);   //获取当地日期和时间
	int date = (timenow.tm_year + 1900) * 10000 + (timenow.tm_mon + 1) * 100 + (timenow.tm_mday);
	int newgroupid;
	int i;
	b1.AddGroup(name, Head->person->returnMicroBlog()->ID(), date);
	newgroupid = b1.Number_of_Groups() + 1000;
	for (i = 1; i < number_of_members; i++) {
		if (GroupMembers[i]->person->returnMicroBlog() != 0) {
			b1.ingroup(newgroupid, GroupMembers[i]->person->returnMicroBlog()->ID());
		}
	}
	return newgroupid;
}

int qqGroupNo::MakeWeChatGroup() {
	struct tm timenow;   //tm结构指针
	time_t now;  //声明time_t类型变量
	time(&now);      //获取系统日期和时间
	localtime_s(&timenow, &now);   //获取当地日期和时间
	int date = (timenow.tm_year + 1900) * 10000 + (timenow.tm_mon + 1) * 100 + (timenow.tm_mday);
	int newgroupid;
	int i;
	c1.AddGroup(name, Head->person->returnwechat()->ID(), date);
	newgroupid = c1.Number_of_Groups() + 1000;
	for (i = 1; i < number_of_members; i++) {
		if (GroupMembers[i]->person->returnwechat() != 0) {
			c1.ingroup(newgroupid, GroupMembers[i]->person->returnwechat()->ID());
		}
	}
	return newgroupid;
}

QQUsersManagerNo::QQUsersManagerNo() {
	int i;
	for (i = 0; i < 200; i++) qqUsers[i] = 0;
	for (i = 0; i < 20; i++) qqGroups[i] = 0;
	for (i = 0; i < 200; i++) { friendrelations[i][0] = 0; friendrelations[i][1] = 0;}
	number_of_relations = 0;
	number_of_users = 0;
	number_of_groups = 0;
};

void QQUsersManagerNo::AddUser(string n, int b, string p, int d) {
	int i = number_of_users + 10001;
	qqUsers[number_of_users] = new QQUserNo(i, n, b, p, d);
	number_of_users++;
}

QQUserNo* QQUsersManagerNo::find(int xid) {
	int j;
	for (j = 0; j < number_of_users; j++) {
		if (qqUsers[j]->ID() == xid) return qqUsers[j];
	}
}

qqGroupNo* QQUsersManagerNo::find2(int xid) {
	int j;
	for (j = 0; j < number_of_groups; j++) {
		if (qqGroups[j]->gID() == xid) return qqGroups[j];
	}
}

void QQUsersManagerNo::AddGroup(string n, int x1, int d) {
	int i = number_of_groups + 1001;
	qqGroups[number_of_groups] = new qqGroupNo(i, n, x1, d);
	number_of_groups++;
	find(x1)->InGroup(i);
}

bool QQUsersManagerNo::Searching(int xid) {
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

bool QQUsersManagerNo::Searching2(int gid) {
	int j;
	for (j = 0; j < number_of_groups; j++) {
		if (qqGroups[j]->gID() == gid) return true;
	}
	return false;
}

void QQUsersManagerNo::open(int xid) {
	find(xid)->opened = true; 
	struct tm timenow;   //tm结构指针
	time_t now;  //声明time_t类型变量
	time(&now);      //获取系统日期和时间
	localtime_s(&timenow, &now);   //获取当地日期和时间
	int date_now = (timenow.tm_year + 1900) * 10000 + (timenow.tm_mon + 1) * 100 + (timenow.tm_mday);
	find(xid)->RegisterTime(date_now);
}

void QQUsersManagerNo::becomefriends(int x1, int x2) {
	find(x1)->AddFriend(x2); 
	find(x2)->AddFriend(x1); 
	friendrelations[number_of_relations][0] = find(x1)->ID(); 
	friendrelations[number_of_relations][1] = find(x2)->ID(); 
	number_of_relations++;
}

void QQUsersManagerNo::deletefriends(int x1, int x2) {
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

MicroBlogUserNo::MicroBlogUserNo(int i, string n, int b, string p, int d) {
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
	person = new personNo;
	person->MBLOGID(i);
	person->QQID(0);
	person->WECHATID(0);
}

void MicroBlogUserNo::AddFriend(int xid) {
	this->friends[number_of_friends] = b1.find(xid);
	number_of_friends++;
}

void MicroBlogUserNo::DeleteFriend(int xid) {
	int i, j;
	for (i = 0; i < number_of_friends; i++) { //遍历好友列表，查询是否有此好友
		if (b1.find(xid) == friends[i]) {//查找得到
			for (j = i; j < number_of_friends; j++) { friends[j] = friends[j + 1]; } //列表前移
			friends[number_of_friends] = 0;
			number_of_friends--;
		}
	}
}

void MicroBlogUserNo::Show() {
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

void MicroBlogUserNo::Show_Friend() {
	int i;
	cout << "当前您的微博好友列表：" << endl;
	for (i = 0; i < number_of_friends; i++) {
		cout << "第" << i + 1 << "个好友：" << friends[i]->name << "   微博ID：" << friends[i]->ID() << endl;
	}
	cout << endl;
}

void MicroBlogUserNo::Show_Group() {
	int i;
	cout << "当前您的群列表：" << endl;
	for (i = 0; i < number_of_groups; i++) {
		cout << "第" << i + 1 << "个群：" << groups[i]->Name() << "   群号：" << groups[i]->gID() << endl;
	}
	cout << endl;
}

void MicroBlogUserNo::InGroup(int xid) {
	groups[number_of_groups] = b1.find2(xid);
	number_of_groups++;
}

void MicroBlogUserNo::OutGroup(int xid) {
	int i, j;
	for (i = 0; i < number_of_groups; i++) { //遍历群列表，查询是否有此群
		if (b1.find2(xid) == groups[i]) { //查找得到
			for (j = i; j < number_of_groups; j++) { groups[j] = groups[j + 1]; } //列表前移
			groups[number_of_groups] = 0;
			number_of_groups--;
		}
	}
}

bool MicroBlogUserNo::IsFriend(int xid) {
	int i;
	for (i = 0; i < number_of_friends; i++) { //遍历好友列表，查询是否有此好友
		if (b1.find(xid) == friends[i]) { //查找得到
			return true;
		}
	}
	return false;
}

bool MicroBlogUserNo::IsInGroup(int xid) {
	int i;
	for (i = 0; i < number_of_groups; i++) { //遍历群列表，查询是否有此群
		if (b1.find2(xid) == groups[i]) { //查找得到
			return true;
		}
	}
	return false;
}


MicroBlogGroupNo::MicroBlogGroupNo(int i, string n, int x1, int d) {
	int j;
	ID = i;
	name = n;
	createtime = d;
	for (j = 0; j < 100; j++) {
		GroupMembers[j] = 0;
	}
	GroupMembers[0] = b1.find(x1);
	Head = b1.find(x1);//第一人为群主
	number_of_members = 1;
}

void MicroBlogGroupNo::Add(int xid) {
	GroupMembers[number_of_members] = b1.find(xid);
	number_of_members++;
}

void MicroBlogGroupNo::Kick(int xid) {
	int i, j;
	for (i = 0; i < number_of_members; i++) { //遍历群成员列表，查询是否有此人
		if (b1.find(xid) == GroupMembers[i]) { //查找得到
			for (j = i; j < number_of_members; j++) { GroupMembers[j] = GroupMembers[j + 1]; } //列表前移
			GroupMembers[number_of_members] = 0;
			number_of_members--;
		}
	}
}

bool MicroBlogGroupNo::IsHead(int xid) {
	return (b1.find(xid) == Head);
}

void MicroBlogGroupNo::Show() {
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

int MicroBlogGroupNo::MakeQQGroup() {
	struct tm timenow;   //tm结构指针
	time_t now;  //声明time_t类型变量
	time(&now);      //获取系统日期和时间
	localtime_s(&timenow, &now);   //获取当地日期和时间
	int date = (timenow.tm_year + 1900) * 10000 + (timenow.tm_mon + 1) * 100 + (timenow.tm_mday);
	int newgroupid;
	int i;
	a1.AddGroup(name, Head->person->returnqq()->ID(), date);
	newgroupid = a1.Number_of_Groups() + 1000;
	for (i = 1; i < number_of_members; i++) {
		if (GroupMembers[i]->person->returnqq() != 0) {
			a1.ingroup(newgroupid, GroupMembers[i]->person->returnqq()->ID());
		}
	}
	return newgroupid;
}

int MicroBlogGroupNo::MakeWeChatGroup() {
	struct tm timenow;   //tm结构指针
	time_t now;  //声明time_t类型变量
	time(&now);      //获取系统日期和时间
	localtime_s(&timenow, &now);   //获取当地日期和时间
	int date = (timenow.tm_year + 1900) * 10000 + (timenow.tm_mon + 1) * 100 + (timenow.tm_mday);
	int newgroupid;
	int i;
	c1.AddGroup(name, Head->person->returnwechat()->ID(), date);
	newgroupid = c1.Number_of_Groups() + 1000;
	for (i = 1; i < number_of_members; i++) {
		if (GroupMembers[i]->person->returnwechat() != 0) {
			c1.ingroup(newgroupid, GroupMembers[i]->person->returnwechat()->ID());
		}
	}
	return newgroupid;
}

MicroBlogManagerNo::MicroBlogManagerNo() {
	int i;
	for (i = 0; i < 200; i++) mbUsers[i] = 0;
	for (i = 0; i < 20; i++) mbGroups[i] = 0;
	for (i = 0; i < 200; i++) { friendrelations[i][0] = 0; friendrelations[i][1] = 0; }
	number_of_relations = 0;
	number_of_users = 0;
	number_of_groups = 0;
};

void MicroBlogManagerNo::AddUser(string n, int b, string p, int d) {
	int i = number_of_users + 10001;
	mbUsers[number_of_users] = new MicroBlogUserNo(i, n, b, p, d);
	number_of_users++;
}

MicroBlogUserNo* MicroBlogManagerNo::find(int xid) {
	int j;
	for (j = 0; j < number_of_users; j++) {
		if (mbUsers[j]->ID() == xid) return mbUsers[j];
	}
}

MicroBlogGroupNo* MicroBlogManagerNo::find2(int xid) {
	int j;
	for (j = 0; j < number_of_groups; j++) {
		if (mbGroups[j]->gID() == xid) return mbGroups[j];
	}
}

void MicroBlogManagerNo::AddGroup(string n, int x1, int d) {
	int i = number_of_groups + 1001;
	mbGroups[number_of_groups] = new MicroBlogGroupNo(i, n, x1, d);
	number_of_groups++;
	find(x1)->InGroup(i);
}

bool MicroBlogManagerNo::Searching(int xid) {
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

bool MicroBlogManagerNo::Searching2(int gid) {
	int j;
	for (j = 0; j < number_of_groups; j++) {
		if (mbGroups[j]->gID() == gid) return true;
	}
	return false;
}

void MicroBlogManagerNo::open(int xid) {
	find(xid)->opened = true;
	struct tm timenow;   //tm结构指针
	time_t now;  //声明time_t类型变量
	time(&now);      //获取系统日期和时间
	localtime_s(&timenow, &now);   //获取当地日期和时间
	int date_now = (timenow.tm_year + 1900) * 10000 + (timenow.tm_mon + 1) * 100 + (timenow.tm_mday);
	find(xid)->RegisterTime(date_now);
}

void MicroBlogManagerNo::becomefriends(int x1, int x2) {
	find(x1)->AddFriend(x2);
	find(x2)->AddFriend(x1);
	friendrelations[number_of_relations][0] = find(x1)->ID();
	friendrelations[number_of_relations][1] = find(x2)->ID();
	number_of_relations++;
}

void MicroBlogManagerNo::deletefriends(int x1, int x2) {
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

WeChatUserNo::WeChatUserNo(int i, string n, int b, string p, int d) {
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
	person = new personNo;
	person->WECHATID(i);
	person->QQID(0);
	person->MBLOGID(0);
}

void WeChatUserNo::AddFriend(int xid) {
	this->friends[number_of_friends] = c1.find(xid);
	number_of_friends++;
}

void WeChatUserNo::DeleteFriend(int xid) {
	int i, j;
	for (i = 0; i < number_of_friends; i++) { //遍历好友列表，查询是否有此好友
		if (c1.find(xid) == friends[i]) {//查找得到
			for (j = i; j < number_of_friends; j++) { friends[j] = friends[j + 1]; } //列表前移
			friends[number_of_friends] = 0;
			number_of_friends--;
		}
	}
}

void WeChatUserNo::Show() {
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

void WeChatUserNo::Show_Friend() {
	int i;
	cout << "当前您的微信好友列表：" << endl;
	for (i = 0; i < number_of_friends; i++) {
		cout << "第" << i + 1 << "个好友：" << friends[i]->name << "   微信ID：" << friends[i]->ID() << endl;
	}
	cout << endl;
}

void WeChatUserNo::Show_Group() {
	int i;
	cout << "当前您的群列表：" << endl;
	for (i = 0; i < number_of_groups; i++) {
		cout << "第" << i + 1 << "个群：" << groups[i]->Name() << "   群号：" << groups[i]->gID() << endl;
	}
	cout << endl;
}

void WeChatUserNo::InGroup(int xid) {
	groups[number_of_groups] = c1.find2(xid);
	number_of_groups++;
}

void WeChatUserNo::OutGroup(int xid) {
	int i, j;
	for (i = 0; i < number_of_groups; i++) { //遍历群列表，查询是否有此群
		if (c1.find2(xid) == groups[i]) { //查找得到
			for (j = i; j < number_of_groups; j++) { groups[j] = groups[j + 1]; } //列表前移
			groups[number_of_groups] = 0;
			number_of_groups--;
		}
	}
}

bool WeChatUserNo::IsFriend(int xid) {
	int i;
	for (i = 0; i < number_of_friends; i++) { //遍历好友列表，查询是否有此好友
		if (c1.find(xid) == friends[i]) { //查找得到
			return true;
		}
	}
	return false;
}

bool WeChatUserNo::IsInGroup(int xid) {
	int i;
	for (i = 0; i < number_of_groups; i++) { //遍历群列表，查询是否有此群
		if (c1.find2(xid) == groups[i]) { //查找得到
			return true;
		}
	}
	return false;
}


WeChatGroupNo::WeChatGroupNo(int i, string n, int x1, int d) {
	int j;
	ID = i;
	name = n;
	createtime = d;
	for (j = 0; j < 100; j++) {
		GroupMembers[j] = 0;
	}
	GroupMembers[0] = c1.find(x1);
	Head = c1.find(x1);//第一人为群主
	number_of_members = 1;
}

void WeChatGroupNo::Add(int xid) {
	GroupMembers[number_of_members] = c1.find(xid);
	number_of_members++;
}

void WeChatGroupNo::Kick(int xid) {
	int i, j;
	for (i = 0; i < number_of_members; i++) { //遍历群成员列表，查询是否有此人
		if (c1.find(xid) == GroupMembers[i]) { //查找得到
			for (j = i; j < number_of_members; j++) { GroupMembers[j] = GroupMembers[j + 1]; } //列表前移
			GroupMembers[number_of_members] = 0;
			number_of_members--;
		}
	}
}

bool WeChatGroupNo::IsHead(int xid) {
	return (c1.find(xid) == Head);
}

void WeChatGroupNo::Show() {
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

int WeChatGroupNo::MakeQQGroup() {
	struct tm timenow;   //tm结构指针
	time_t now;  //声明time_t类型变量
	time(&now);      //获取系统日期和时间
	localtime_s(&timenow, &now);   //获取当地日期和时间
	int date = (timenow.tm_year + 1900) * 10000 + (timenow.tm_mon + 1) * 100 + (timenow.tm_mday);
	int newgroupid;
	int i;
	a1.AddGroup(name, Head->person->returnqq()->ID(), date);
	newgroupid = a1.Number_of_Groups() + 1000;
	for (i = 1; i < number_of_members; i++) {
		if (GroupMembers[i]->person->returnqq() != 0) {
			a1.ingroup(newgroupid, GroupMembers[i]->person->returnqq()->ID());
		}
	}
	return newgroupid;
}

int WeChatGroupNo::MakeMicroBlogGroup() {
	struct tm timenow;   //tm结构指针
	time_t now;  //声明time_t类型变量
	time(&now);      //获取系统日期和时间
	localtime_s(&timenow, &now);   //获取当地日期和时间
	int date = (timenow.tm_year + 1900) * 10000 + (timenow.tm_mon + 1) * 100 + (timenow.tm_mday);
	int newgroupid;
	int i;
	b1.AddGroup(name, Head->person->returnMicroBlog()->ID(), date);
	newgroupid = b1.Number_of_Groups() + 1000;
	for (i = 1; i < number_of_members; i++) {
		if (GroupMembers[i]->person->returnMicroBlog() != 0) {
			b1.ingroup(newgroupid, GroupMembers[i]->person->returnMicroBlog()->ID());
		}
	}
	return newgroupid;
}


WeChatUserManagerNo::WeChatUserManagerNo() {
	int i;
	for (i = 0; i < 200; i++) WeChatUsers[i] = 0;
	for (i = 0; i < 20; i++) WeChatGroups[i] = 0;
	for (i = 0; i < 200; i++) { friendrelations[i][0] = 0; friendrelations[i][1] = 0; }
	number_of_relations = 0;
	number_of_users = 0;
	number_of_groups = 0;
};

void WeChatUserManagerNo::AddUser(string n, int b, string p, int d) {
	int i = number_of_users + 20001;
	WeChatUsers[number_of_users] = new WeChatUserNo(i, n, b, p, d);
	number_of_users++;
}

WeChatUserNo* WeChatUserManagerNo::find(int xid) {
	int j;
	for (j = 0; j < number_of_users; j++) {
		if (WeChatUsers[j]->ID() == xid) return WeChatUsers[j];
	}
}

WeChatGroupNo* WeChatUserManagerNo::find2(int xid) {
	int j;
	for (j = 0; j < number_of_groups; j++) {
		if (WeChatGroups[j]->gID() == xid) return WeChatGroups[j];
	}
}

void WeChatUserManagerNo::AddGroup(string n, int x1, int d) {
	int i = number_of_groups + 1001;
	WeChatGroups[number_of_groups] = new WeChatGroupNo(i, n, x1, d);
	number_of_groups++;
	find(x1)->InGroup(i);
}

bool WeChatUserManagerNo::Searching(int xid) {
	int j;
	for (j = 0; j < number_of_users; j++) {
		if (WeChatUsers[j]->ID() == xid) return true;
	}
	return false;
}

bool WeChatUserManagerNo::Searching2(int gid) {
	int j;
	for (j = 0; j < number_of_groups; j++) {
		if (WeChatGroups[j]->gID() == gid) return true;
	}
	return false;
}

void WeChatUserManagerNo::becomefriends(int x1, int x2) {
	find(x1)->AddFriend(x2);
	find(x2)->AddFriend(x1);
	friendrelations[number_of_relations][0] = find(x1)->ID();
	friendrelations[number_of_relations][1] = find(x2)->ID();
	number_of_relations++;
}

void WeChatUserManagerNo::deletefriends(int x1, int x2) {
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

QQUserNo * personNo::returnqq() { 
	if (qqid == 0) return 0; 
	return a1.find(qqid); 
}

MicroBlogUserNo * personNo::returnMicroBlog() {
	if (MicroBlogid == 0) return 0;
	return b1.find(MicroBlogid); 
}

WeChatUserNo * personNo::returnwechat() {
	if (Wechatid == 0) return 0;
	return c1.find(Wechatid); 
}

//============================================分界线========================
string QQUsersManagerNo::writetofile() {
	string all;
	int i;
	ostringstream ss1,ss2;
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

string QQUserNo::write() {
	ostringstream ss1, ss2; 
	ss1 << birthdate; 
	ss2 << registertime; 
	if (opened) return name + " " + ss1.str() + " " + place + " " + ss2.str() + " " + "1"; 
	else return name + " " + ss1.str() + " " + place + " " + ss2.str() + " " + "0";
}

string qqGroupNo::write1() {
	ostringstream ss1, ss2;
	ss1 << createtime;
	ss2 << Head->ID();
	return name + " " + ss2.str() + " " + ss1.str();
}

string qqGroupNo::write2() {
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

string qqGroupNo::write3() {
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

string MicroBlogManagerNo::writetofile() {
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

string MicroBlogUserNo::write() {
	ostringstream ss1, ss2;
	ss1 << birthdate;
	ss2 << registertime;
	if (opened) return name + " " + ss1.str() + " " + place + " " + ss2.str() + " " + "1";
	else return name + " " + ss1.str() + " " + place + " " + ss2.str() + " " + "0";
}

string MicroBlogGroupNo::write1() {
	ostringstream ss1, ss2;
	ss1 << createtime;
	ss2 << Head->ID();
	return name + " " + ss2.str() + " " + ss1.str();
}

string MicroBlogGroupNo::write2() {
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

string WeChatUserManagerNo::writetofile() {
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

string WeChatUserNo::write() {
	ostringstream ss1, ss2;
	ss1 << birthdate;
	ss2 << registertime;
	return name + " " + ss1.str() + " " + place + " " + ss2.str();
}

string WeChatGroupNo::write1() {
	ostringstream ss1, ss2;
	ss1 << createtime;
	ss2 << Head->ID();
	return name + " " + ss2.str() + " " + ss1.str();
}

string WeChatGroupNo::write2() {
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

string QQUsersManagerNo::writetofile2() {
	string all = "";
	int i;
	ostringstream ss1, ss2;
	for (i = 0; i < number_of_users; i++) {
		if (qqUsers[i]->person->returnMicroBlog() != 0) {
			ss1.str("");
			ss2.str("");
			ss1 << qqUsers[i]->ID();
			ss2 << qqUsers[i]->person->returnMicroBlog()->ID();
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

string MicroBlogManagerNo::writetofile2() {
	string all = "";
	int i;
	ostringstream ss1, ss2;
	for (i = 0; i < number_of_users; i++) {
		if (mbUsers[i]->person->returnMicroBlog() != 0) {
			ss1.str("");
			ss2.str("");
			ss1 << mbUsers[i]->ID();
			ss2 << mbUsers[i]->person->returnMicroBlog()->ID();
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

string WeChatUserManagerNo::writetofile2() {
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
		if (WeChatUsers[i]->person->returnMicroBlog() != 0) {
			ss1.str("");
			ss2.str("");
			ss1 << WeChatUsers[i]->ID();
			ss2 << WeChatUsers[i]->person->returnMicroBlog()->ID();
			all = all + ss1.str() + " " + ss2.str() + "\n";
		}
	}
	all += "0";
	all += "\n";
	return all;
}