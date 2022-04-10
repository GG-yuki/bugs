#ifndef _BASIC_H_
#include <iostream>
#include <string>
#include <sstream>
using namespace std;

class QQUserNo;
class WeChatUserNo;
class MicroBlogUserNo;
class QQGroupNo;
class WeChatGroupNo;
class MicroBlogGroupNo;
class QQUserNo;
class WeChatNo;
class MicroBlogNo;


class PersonNo
{
private:
    int QqID;
    int MicroBlogID;
    int WeChatID;


public:
    void QQID(int i)
    {
        QqID = i;
    }

    void MICROBLOGID(int i)
    {
        MicroBlogID = i;
    }

    void WECHATID(int i)
    {
        WeChatID = i;
    }

    // qqUserNo * returnqq();
	// MicroBlogUserNo * returnMicroBlog();
	// WeChatUserNo * returnwechat();
};


class UserNo
{ //用户
protected:
	int id; //Q号/微信ID （设置：qq10001+ 微信20000+）
	string name; //昵称
	int birth; //8位生日
	int registertime; //注册时间（准备调用系统时间实现）
	string province; //省份
	int num_friend; //好友个数
	int num_group; //群个数
public:
	PersonNo * personno;//使用者
	int ID() { return id; }//输出id
	string Name() { return name; };
	void change_info();//修改个人信息
	virtual void AddFriend(int i) = 0;
	virtual void DeleteFriend(int i) = 0;
	virtual void AddGroup(int i) = 0;
	virtual void DeleteGroup(int i) = 0;
	virtual void Show() = 0;
	virtual void Show_Friend() = 0;
	virtual void Show_Group() = 0;
	virtual bool IsFriend(int xid) = 0;///判断是不是好友
	virtual bool IsInGroup(int xid) = 0;//判断是否在群内
	void RegisterTime(int t) { registertime = t; }
	virtual string write() = 0;
};

class QQUserNo :public UserNo { //qq用户
private:
	QQUserNo * qqfriend[100]; //qq好友
	QQGroupNo * group[30]; //qq群
public:
	QQUserNo(int i, string n, int b, string p, int d);
	void AddFriend(int xid);
	void DeleteFriend(int xid);
	void InGroup(int xid);
	void OutGroup(int xid);
	void Show();
	void Show_Friend();
	void Show_Group();
	bool IsFriend(int xid);
	bool IsInGroup(int xid); 
	bool opened; //确实开通则为true，用于检测是不是预留的（未开通，则无法search到）
	string write();
};

class MicroBlogUserNo :public UserNo { //微博用户
private:
	MicroBlogUserNo * friends[100]; //微博好友
	MicroBlogGroupNo * groups[30]; //微博群
public:
	MicroBlogUserNo(int i, string n, int b, string p, int d);
	void AddFriend(int xid);
	void DeleteFriend(int xid);
	void InGroup(int xid);
	void OutGroup(int xid);
	void Show();
	void Show_Friend();
	void Show_Group();
	bool IsFriend(int xid);
	bool IsInGroup(int xid);
	bool opened; //确实开通则为true，用于检测是不是预留的（未开通，则无法search到）
	string write();
};

class WeChatUserNo :public UserNo { //微信用户
private:
	WeChatUserNo * wechatfriend[100]; //微信好友
	WeChatGroupNo * groups[30]; //微信群
public:
	WeChatUserNo(int i, string n, int b, string p, int d);
	void AddFriend(int xid);
	void DeleteFriend(int xid);
	void InGroup(int xid);
	void OutGroup(int xid);
	void Show();
	void Show_Friend();
	void Show_Group();
	bool IsFriend(int xid);
	bool IsInGroup(int xid);
	string write();
};

class GroupNo {
protected:
	int group_id; //群号（1000+）
	string group_name;//群名
	int register_time;//创建时间
	int group_num_of_members;
public:
	int Printnum_of_members() { return group_num_of_members; }
	int Printid() { return group_id; }//输出群号
	string Printame() { return group_name; }
	virtual void Add_mem(int xid) = 0;//加群
	virtual void Reduce_mem(int xid) = 0;//退出/踢出
	virtual void Show() = 0;
	virtual bool IsLeader(int xid) = 0;
	virtual string write1() = 0;
	virtual string write2() = 0;
};

class QQGroupNo :public GroupNo {
private:
	QQUserNo* GroupMembers[100]; //群员
	QQUserNo* Head; //群主
	QQUserNo* Managers[20]; //管理员
	int num_of_managers;
	QQUserNo* minigroupmembers[15];//临时讨论组
public:
	QQGroupNo(int i, string n, int x1, int t);//建群，初始一个成员
	void Add_mem(int xid) = 0;//加群
	void Reduce_mem(int xid) = 0;//退出/踢出
	void Show() = 0;
	bool IsLeader(int xid) = 0;
	bool IsManager(int xid);
	void BecomeManager(int xid);
	void LostManager(int xid);
	void getinminigroup(int xid);
	void deleteminigroup();
	int num_of_minigroupmembers;
	bool isinminigroup(int xid);
	int MakeMicroBlogGroup();
	int MakeWeChatGroup();
	string write1();
	string write2();
	string write3();
};

class MicroBlogGroupNo :public GroupNo {
private:
	MicroBlogUserNo* GroupMembers[100]; //群员
	MicroBlogUserNo* Head; //群主
public:
	MicroBlogGroupNo(int i, string n, int x1, int t);//建群
	void Add(int xid);
	void Kick(int xid);
	void Show();
	bool IsHead(int xid);
	int Num_of_members() { return group_num_of_members; }
	int MakeQQGroup();
	int MakeWeChatGroup();
	string write1();
	string write2();
};

class WeChatGroupNo :public GroupNo {
private:
	WeChatUserNo* GroupMembers[100]; //群员
	WeChatUserNo* Head; //群主
public:
	WeChatGroupNo(int i, string n, int x1, int t);//建群
	void Add(int xid);
	void Kick(int xid);
	void Show();
	bool IsHead(int xid);
	int Num_of_members() { return group_num_of_members; }
	int MakeQQGroup();
	int MakeMicroBlogGroup();
	string write1();
	string write2();
};

class UsersManagerNo {
protected:
	int num_of_users;
	int num_of_groups;
	int friendrelations[200][2]; //好友关系，主要是用于保存记录
	int num_of_relations;
public:
	int Num_of_Users() { return num_of_users; }
	int Num_of_Groups() { return num_of_groups; }
	virtual void Modify(int xid) = 0;
	virtual void AddUser(string n, int b, string p, int d) = 0;
	virtual void AddGroup(string n, int x1, int t) = 0;
	virtual void show(int xid) = 0;
	virtual void show2(int xid) = 0;
	virtual void showfriendlist(int xid) = 0;
	virtual void showgrouplist(int xid) = 0;
	virtual void becomefriends(int x1, int x2) = 0;
	virtual void deletefriends(int x1, int x2) = 0;
	virtual void ingroup(int g1, int x1) = 0;
	virtual void outgroup(int g1, int x1) = 0;
	virtual bool Searching(int xid) = 0;
	virtual bool Searching2(int gid) = 0;
	virtual bool isFriend(int xid, int gid) = 0;
	virtual bool isInGroup(int xid, int gid) = 0;
	virtual bool isHead(int xid, int gid) = 0;
	virtual int Num_of_Members(int gid) = 0;
	virtual string writetofile() = 0;
	virtual string writetofile2() = 0;
};

class QQUserManagerNo : public UsersManagerNo {
private:
	QQUserNo* qqUsers[200];
	QQGroupNo* qqGroups[20];
public:
	QQUserManagerNo();
	void Modify(int xid) { find(xid)->modify(); }
	void AddUser(string n, int b, string p, int d);
	void AddGroup(string n, int x1, int d);
	QQUserNo* find(int xid); //根据用户id返回指针
	QQGroupNo* find2(int xid); //根据群id返回指针
	void show(int xid) { qqUsers[xid - 10001]->Show(); }
	void show2(int xid) { qqGroups[xid - 1001]->Show(); }
	void showfriendlist(int xid) { qqUsers[xid - 10001]->Show_Friend(); }
	void showgrouplist(int xid) { qqUsers[xid - 10001]->Show_Group(); }
	void becomefriends(int x1, int x2);
	void deletefriends(int x1, int x2); 
	void ingroup(int g1, int x1) { find2(g1)->Add(x1); find(x1)->InGroup(g1); }
	void outgroup(int g1, int x1) { find2(g1)->Kick(x1); find(x1)->OutGroup(g1); }
	bool Searching(int xid);
	bool Searching2(int gid);
	bool isFriend(int xid, int gid) { return find(xid)->IsFriend(gid); }
	bool isInGroup(int xid, int gid) { return find(xid)->IsInGroup(gid); }
	bool isHead(int xid, int gid) { return find2(gid)->IsHead(xid); }
	bool isManager(int xid, int gid) { return find2(gid)->IsManager(xid); }
	void becomemanager(int xid, int gid) { find2(gid)->BecomeManager(xid); }
	void lostmanager(int xid, int gid) { find2(gid)->LostManager(xid); }
	void Getinminigroup(int xid, int gid) { find2(gid)->getinminigroup(xid); }
	void Deleteminigroup(int gid) { find2(gid)->deleteminigroup(); }
	bool Isinminigroup(int xid, int gid) { return find2(gid)->isinminigroup(xid); }
	int Num_of_Members(int gid) { return find2(gid)->Num_of_members(); }
	MicroBlogUserNo * returnMicroBlog(int xid) { return find(xid)->person->returnMicroBlog(); }
	WeChatUserNo * returnWeChat(int xid) { return find(xid)->person->returnwechat(); }
	void changeMicroBlog(int qqid, int mbid) { find(qqid)->person->MicroBlogID(mbid); }
	void changewechat(int qqid, int wxid) { find(qqid)->person->WECHATID(wxid); }
	void open(int xid);
	string groupname(int g1) { return find2(g1)->Name(); }
	int makeMicroBloggroup(int g1) { return find2(g1)->MakeMicroBlogGroup(); }//返回群号
	int makewechatgroup(int g1) { return find2(g1)->MakeWeChatGroup(); }
	string writetofile();
	string writetofile2();
};

class MicroBlogManagerNo : public UsersManagerNo {
private:
	MicroBlogUserNo* mbUsers[200];
	MicroBlogGroupNo* mbGroups[20];
public:
	MicroBlogManagerNo();
	void Modify(int xid) { find(xid)->modify(); }
	void AddUser(string n, int b, string p, int d);
	void AddGroup(string n, int x1, int d);
	MicroBlogUserNo* find(int xid); //根据用户id返回指针
	MicroBlogGroupNo* find2(int xid); //根据群id返回指针
	void show(int xid) { mbUsers[xid - 10001]->Show(); }
	void show2(int xid) { mbGroups[xid - 1001]->Show(); }
	void showfriendlist(int xid) { mbUsers[xid - 10001]->Show_Friend(); }
	void showgrouplist(int xid) { mbUsers[xid - 10001]->Show_Group(); }
	void becomefriends(int x1, int x2);
	void deletefriends(int x1, int x2);
	void ingroup(int g1, int x1) { find2(g1)->Add(x1); find(x1)->InGroup(g1); }
	void outgroup(int g1, int x1) { find2(g1)->Kick(x1); find(x1)->OutGroup(g1); }
	bool Searching(int xid);
	bool Searching2(int gid);
	bool isFriend(int xid, int gid) { return find(xid)->IsFriend(gid); }
	bool isInGroup(int xid, int gid) { return find(xid)->IsInGroup(gid); }
	bool isHead(int xid, int gid) { return find2(gid)->IsHead(xid); }
	int Num_of_Members(int gid) { return find2(gid)->Num_of_members(); }
	qqUserNo * returnqq(int xid) { return find(xid)->person->returnqq(); }
	WeChatUserNo * returnWeChat(int xid) { return find(xid)->person->returnwechat(); }
	void changeqq(int mbid, int qqid) { find(mbid)->person->QQID(qqid); }
	void changewechat(int mbid, int wxid) { find(mbid)->person->WECHATID(wxid); }
	void open(int xid);
	int makeqqgroup(int g1) { return find2(g1)->MakeQQGroup(); }
	int makewechatgroup(int g1) { return find2(g1)->MakeWeChatGroup(); }
	string writetofile();
	string writetofile2();
};

class WeChatUserManagerNo : public UsersManagerNo {
private:
	WeChatUserNo* WeChatUsers[200];
	WeChatGroupNo* WeChatGroups[20];
public:
	WeChatUserManagerNo();
	void Modify(int xid) { find(xid)->modify(); }
	void AddUser(string n, int b, string p, int d);
	void AddGroup(string n, int x1, int d);
	WeChatUserNo* find(int xid); //根据用户id返回指针
	WeChatGroupNo* find2(int xid); //根据群id返回指针
	void show(int xid) { WeChatUsers[xid - 20001]->Show(); }
	void show2(int xid) { WeChatGroups[xid - 1001]->Show(); }
	void showfriendlist(int xid) { WeChatUsers[xid - 20001]->Show_Friend(); }
	void showgrouplist(int xid) { WeChatUsers[xid - 20001]->Show_Group(); }
	void becomefriends(int x1, int x2);
	void deletefriends(int x1, int x2);
	void ingroup(int g1, int x1) { find2(g1)->Add(x1); find(x1)->InGroup(g1); }
	void outgroup(int g1, int x1) { find2(g1)->Kick(x1); find(x1)->OutGroup(g1); }
	bool Searching(int xid);
	bool Searching2(int gid);
	bool isFriend(int xid, int gid) { return find(xid)->IsFriend(gid); }
	bool isInGroup(int xid, int gid) { return find(xid)->IsInGroup(gid); }
	bool isHead(int xid, int gid) { return find2(gid)->IsHead(xid); }
	int Num_of_Members(int gid) { return find2(gid)->Num_of_members(); }
	qqUserNo * returnqq(int xid) { return find(xid)->person->returnqq(); }
	MicroBlogUserNo * returnMicroBlog(int xid) { return find(xid)->person->returnMicroBlog(); } 
	void changeqq(int wxid, int qqid) { find(wxid)->person->QQID(qqid); }
	void changeMicroBlog(int wxid, int mbid) { find(wxid)->person->MicroBlogID(mbid); }
	int makeqqgroup(int g1) { return find2(g1)->MakeQQGroup(); }
	int makeMicroBloggroup(int g1) { return find2(g1)->MakeMicroBlogGroup(); }
	string writetofile();
	string writetofile2();
};

#endif