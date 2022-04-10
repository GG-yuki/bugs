#include "pch.h"
#include <iostream>
#include <string>
#include <time.h>
#include <fstream>
#include "basic.h"
using namespace std;

QQUserManagerNo qqusermanage;
MicroBlogManagerNo mbusermanage;
WeChatUserManagerNo wcusermanage;

int main()
{
	char input;
	string nickname, stay_province, groupname;
	int birthday, number2, number_of_users, friends_id1, friends_id2, leader_id, group_id, groupmembers_id, social_plat1, social_plat2, number1; 
	bool temp6;
	bool status_online = false; //是否已经登录
	bool manage = false;//是否正在群管理状态
	bool temp = false;
	bool out = false;
	int qq_user_now = 0;//当前qq用户id
	int mb_user_now = 0;//当前MicroBlog用户id
	int wx_user_now = 0;//当前Wechat用户id
	int social_platform = 0;//当前使用平台：1.qq 2.MicroBlog 3.Wechat
	
	ifstream read_files; //读文件
	ofstream save_files; //写文件
	read_files.open("record.txt");

	//以下为读取QQ信息
	read_files >> number_of_users; //读入用户个数
	for (int j = 0; j < number_of_users; j++) 
	{
		read_files >> nickname >> birthday >> stay_province >> number2 >> temp6;//昵称、生日、地点、注册时间、open与否
		qqusermanage.AddUser(nickname, birthday, stay_province, number2);
		if (temp6) qqusermanage.open(j + 10001);
	}
	do 
	{ // friends信息
		read_files >> friends_id1;
		if (friends_id1 == 0) break;
		read_files >> friends_id2;
		if (friends_id2 == 0) break;
		qqusermanage.becomefriends(friends_id1, friends_id2);
	} while (1);
	read_files >> number_of_users; //读入群个数
	for (int j = 0; j < number_of_users; j++) {
		read_files >> groupname >> leader_id >> number2;//名称、群主、创建时间
		qqusermanage.AddGroup(groupname, leader_id, number2);
	}
	do { //加入群
		read_files >> group_id; //群号
		if (group_id == 0) break;
		read_files >> groupmembers_id; //群友
		if (groupmembers_id == 0) break;
		qqusermanage.ingroup(group_id, groupmembers_id);
	} while (1);
	do { //管理员
		read_files >> group_id; //群号
		if (group_id == 0) break;
		read_files >> groupmembers_id; //群友
		if (groupmembers_id == 0) break;
		qqusermanage.ingroup(group_id, groupmembers_id);
	} while (1);

	//以下为读取MicroBlog信息
	read_files >> number_of_users; //读入用户个数
	for (int j = 0; j < number_of_users; j++) {
		read_files >> nickname >> birthday >> stay_province >> number2 >> temp6;//昵称、生日、地点、注册时间、open与否
		mbusermanage.AddUser(nickname, birthday, stay_province, number2);
		if (temp6) mbusermanage.open(j + 10001);
	}
	do{ // friends信息
		read_files >> friends_id1;
		if (friends_id1 == 0) break;
		read_files >> friends_id2;
		if (friends_id2 == 0) break;
		mbusermanage.becomefriends(friends_id1, friends_id2);
	} while (1);
	read_files >> number_of_users; //读入群个数
	for (int j = 0; j < number_of_users; j++) {
		read_files >> groupname >> leader_id >> number2;//名称、群主、创建时间
		mbusermanage.AddGroup(groupname, leader_id, number2);
	}
	do { //加入群
		read_files >> group_id; //群号
		if (group_id == 0) break;
		read_files >> groupmembers_id; //群友
		if (groupmembers_id == 0) break;
		mbusermanage.ingroup(group_id, groupmembers_id);
	} while (1);

	//以下为读取Wechat信息
	read_files >> number_of_users; //读入用户个数
	for (int j = 0; j < number_of_users; j++) {
		read_files >> nickname >> birthday >> stay_province >> number2 >> temp6;//昵称、生日、地点、注册时间、open与否
		wcusermanage.AddUser(nickname, birthday, stay_province, number2);
	}
	do{ // friends信息
		read_files >> friends_id1;
		if (friends_id1 == 0) break;
		read_files >> friends_id2;
		if (friends_id2 == 0) break;
		wcusermanage.becomefriends(friends_id1, friends_id2);
	} while (1);
	read_files >> number_of_users; //读入群个数
	for (int j = 0; j < number_of_users; j++) {
		read_files >> groupname >> leader_id >> number2;//名称、群主、创建时间
		wcusermanage.AddGroup(groupname, leader_id, number2);
	}
	do { //加入群
		read_files >> group_id; //群号
		if (group_id == 0) break;
		read_files >> groupmembers_id; //群友
		if (groupmembers_id == 0) break;
		wcusermanage.ingroup(group_id, groupmembers_id);
	} while (1);

	//以下为绑定部分
	for(int j = 0; j < 6; j++)
	{
		while (1) 
		{ //qq+wb, qq+wc, wb+qq, wb+wx, wx+qq,wx+wb
			read_files >> social_plat1; 
			if (social_plat1 == 0) break;
			read_files >> social_plat2; 
			if (social_plat2 == 0) break;
			qqusermanage.changemblog(social_plat1, social_plat2);
		}
	}

	struct tm timenow;   //tm结构指针
	time_t now;  //声明time_t类型变量
	time(&now);      //获取系统日期和时间
	localtime_s(&timenow, &now);   //获取当地日期和时间
	int date_now = (timenow.tm_year + 1900) * 10000 + (timenow.tm_mon + 1) * 100 + (timenow.tm_mday);

	do {
		cout << "Choose social platform to log in" << endl << "1.QQ 2.MicroBlog 3.Wechat" << endl;
		cin >> input;
		switch (input) {
		case'1': social_platform = 1; break;
		case'2': social_platform = 2; break;
		case'3': social_platform = 3; break;
		default://结束程序，保存文件 
			save_files.open("record.txt");
			save_files << qqusermanage.writetofile();
			save_files << mbusermanage.writetofile();
			save_files << wcusermanage.writetofile();
			save_files << qqusermanage.writetofile2();
			save_files << mbusermanage.writetofile2();
			save_files << wcusermanage.writetofile2();
			save_files.close();
			return 0;
		}
		while (social_platform == 1) {
			do {
				cout << "1.log in to an existing account 2.register a new account" << endl;
				cin >> input;
				switch (input) {
				case '1':
					cout << "account";
					cin >> number1;
					if (qqusermanage.Searching(number1)) {
						status_online = true;
						qq_user_now = number1;
						cout << "log in success" << endl;
						qqusermanage.show(number1);
						if (qqusermanage.returnmBlog(number1) = 0) {
							mb_user_now = qqusermanage.returnmBlog(qq_user_now)->ID();
							cout << "log in to revelant MicroBlog with account" << mb_user_now << endl;
						}
						else { cout << "can't find relevant MicroBlog account." << endl; }
						if (qqusermanage.returnWeChat(number1) = 0) {
							wx_user_now = qqusermanage.returnWeChat(qq_user_now)->ID();
							cout << "log in to relevant Wechat with account" << wx_user_now << endl;
						}
						else { cout << "can't find relevant Wechat account." << endl; }
					}
					else { cout << "log in failed" << endl; status_online = false; }
					break;
				case '2':
					cout << "enter your nickname" << endl;
					cin >> nickname;
					do {
						cout << "enter your birthday" << endl;
						cin >> birthday;
					} while ((birthday < 19000101) or (birthday > 20200101) or (((birthday % 10000) / 100) > 12) or (((birthday % 10000) / 100) < 1) or ((birthday % 100) > 31) or ((birthday % 100) < 1));
					cout << "enter " << endl;
					cin >> number1;
					qqusermanage.AddUser(nickname, birthday, number1, date_now);
					cout << "register success with account" << qqusermanage.Number_of_Users() + 10000 << endl;
					qq_user_now = qqusermanage.Number_of_Users() + 10000;
					status_online = true;
					cout << endl;
					qqusermanage.show(qqusermanage.Number_of_Users() + 10000);
					cout << "status: log in" << endl;
					qqusermanage.open(qq_user_now);
					mbusermanage.AddUser(nickname, birthday, number1,date_now);//预留MicroBlogid位置（这么做是因为qq与MicroBlog号码必须一致）
					break;
				default:
					social_platform = 0; out = true;
				}
			} while ((status_online == false) && (out == false));
			do {
				if (out) { out = false; break; }
				cout << endl << "choose your next action" << endl;
				cout << "1.change individual information 2.check for friends' info 3.add friends 4.delete friends 5.check for group info" << endl
					<< "6.enter in group 7.withdraw from group 8.manage group 9.create a new group 0.ESC" << endl
					<< "a.ckeck for revelant info of MicroBlog or Wechat b.register a new MicroBlog account c.binding with Wechat account d.unbinding with Wechat account" << endl
					<< "e.check for and add MicroBlog friends f.check for and add Wechat friends" << endl;
				// cout << "（注：QQ friends可以直接通过QQ号添加QQ群可以直接通过群号加入QQ群临时讨论组退出后不会保存）" << endl;
				cin >> input;
				switch (input) {
				case'1':qqusermanage.Modify(qq_user_now); qqusermanage.show(qq_user_now); break;
				case'2':
					cout << "please enter the friend's account number you want to check for" << endl;
					cin >> number1;
					if (qqusermanage.Searching(number1)) qqusermanage.show(number1);
					else cout << "can't find the account" << endl;
					break;
				case'3':
					qqusermanage.showfriendlist(qq_user_now);
					cout << "please enter the user's account number you want to add as a friend" << endl;
					cin >> number1;
					if (qqusermanage.isFriend(qq_user_now, number1)) cout << "already friends" << endl;
					else if (qqusermanage.Searching(number1) == false) cout << "can't find the account" << endl;
					else if (number1 == qq_user_now) cout << "can't add yourself" << endl;
					else { qqusermanage.becomefriends(qq_user_now, number1); cout << "success adding friends" << endl; qqusermanage.showfriendlist(qq_user_now); }
					break;
				case'4':
					qqusermanage.showfriendlist(qq_user_now);
					cout << "enter the friend's account you want to delete" << endl;
					cin >> number1;
					if (qqusermanage.isFriend(qq_user_now, number1)) { qqusermanage.deletefriends(qq_user_now, number1); cout << "already delete friends" << endl; qqusermanage.showfriendlist(qq_user_now); }
					else { cout << "can't find the friends" << endl; }
					break;
				case'5':
					cout << "please enter the group number" << endl;
					cin >> group_id;
					if (qqusermanage.isInGroup(qq_user_now, group_id)) qqusermanage.show2(group_id);
					else cout << "can't find the group" << endl;
					break;
				case '6': //QQ群通过输入群号直接加入 Wechat群通过接受他人邀请加入
					qqusermanage.showgrouplist(qq_user_now);
					cout << "please enter the group number you want to join in" << endl;
					cin >> group_id;
					if (qqusermanage.isInGroup(qq_user_now, group_id)) cout << "already in the group" << endl;
					else if (qqusermanage.Searching2(group_id) == false) cout << "can't find the group" << endl;
					else { qqusermanage.ingroup(group_id, qq_user_now); cout << "success joining in the group" << endl; qqusermanage.showgrouplist(qq_user_now); }
					break;
				case '7':
					qqusermanage.showgrouplist(qq_user_now);
					cout << "enter the group number you want to withdraw from" << endl;
					cin >> group_id;
					if ((qqusermanage.isInGroup(qq_user_now, group_id)) and (qqusermanage.isHead(qq_user_now, group_id) == false)) {
						qqusermanage.outgroup(group_id, qq_user_now); cout << "already withdraw from the group" << endl;
						if (qqusermanage.isManager(qq_user_now, group_id)) qqusermanage.lostmanager(qq_user_now, group_id);
						qqusermanage.showgrouplist(qq_user_now); 
					}
					else if (qqusermanage.isHead(qq_user_now, group_id))cout << "group leader can't withdraw from the group" << endl;
					else cout << "You're not in the group" << endl;
					break;
				case '8':
					qqusermanage.showgrouplist(qq_user_now);
					cout << "please enter the group number you want to manage" << endl;
					cin >> group_id;
					if (qqusermanage.isInGroup(qq_user_now, group_id)) {
						if (qqusermanage.isHead(qq_user_now, group_id)) {
							qqusermanage.show2(group_id);
							manage = true;
							do {
								cout << "As group leader, you can：1.invite member 2.delete member 3.promote manager 4.demote manager 5.build temporary team 6.dismiss temporary team" << endl
									<<"7.change manage mode to MicroBlog group 8.change manage mode to Wechat group" << endl;
								cin >> input;
								switch (input) {
								case '1':
									cout << "please enter the friend's account number you want to invite to the group";
									cin >> number1;
									if (qqusermanage.Searching(number2) == false) cout << "can't find the user" << endl;
									else if (qqusermanage.isInGroup(number2, number1)) { cout << "he's already in the group" << endl; }
									else if (qqusermanage.isFriend(qq_user_now, number2)) { qqusermanage.ingroup(number1, number2); cout << "succeed joining in the group" << endl; qqusermanage.show2(number1); }
									else cout << "you're not friends" << endl;
									break;
								case '2':
									cout << "please enter the member's QQ number you want to kick out：";
									cin >> number2;
									if (qqusermanage.Searching(number2) == false) cout << "can't find the user" << endl;
									else if (number2 == qq_user_now) { cout << "can't kick out yourself" << endl; }
									else if (qqusermanage.isInGroup(number2, number1)) {
										qqusermanage.outgroup(number1, number2);
										if (qqusermanage.isManager(number2, number1)) qqusermanage.lostmanager(number2, number1);
										cout << "he's already not in the group" << endl;
										qqusermanage.show2(number1);
									}
									else cout << "he's already not in the group";
									break;
								case '3':
									cout << "please enter the member's QQ number you want to appoint with manager：";
									cin >> number1;
									if (qqusermanage.Searching(number1) == false) cout << "can't find the user" << endl;
									else if (qqusermanage.isInGroup(number2, number1)) {
										if (qqusermanage.isManager(number2, number1)) { cout << "he's already a manager" << endl; }
										else if (qqusermanage.isHead(number2, number1)) { cout << "can't appoint leader as a managger" << endl; }
										else { qqusermanage.becomemanager(number2, number1); cout << "already appoint the member as a manager" << endl; qqusermanage.show2(number1); }
									}
									else cout << "he's already not in the group" << endl;
									break;
								case '4':
									cout << "please enter the manager's QQ number you want to remove manager position：";
									cin >> number2;
									if (qqusermanage.Searching(number2) == false) cout << "can't find the user" << endl;
									else if (qqusermanage.isInGroup(number2, number1)) {
										if (qqusermanage.isManager(number2, number1)) { qqusermanage.lostmanager(number2, number1); cout << "already remove his manager position" << endl; qqusermanage.show2(number1); }
										else { cout << "he's not a manager" << endl; }
									}
									else cout << "he's already not in the group" << endl;
									break;
								case'5':
									qqusermanage.Deleteminigroup(number1);
									cout << "please enter the number of members in the temporary team(2-15)（leader will join in the team automatically）" << endl;
									cin >> number2;
									if ((number2 < 2) or (number2 > 15) or (number2 > qqusermanage.Number_of_Members(number1))) { cout << "number of people don't satisfy the need" << endl; break; }
									qqusermanage.Getinminigroup(qq_user_now, number1);
									int i;
									for (i = 1; i < number2; i++) {
										do {
											cout << "please enter enter tne QQ number of next group member（enter 0：give up building temporary team）" << endl;
											cin >> number_of_users;
											if (number_of_users == 0) { i = 100; qqusermanage.Deleteminigroup(number1); break; }//强行跳出循环
											if (qqusermanage.Searching(number_of_users) == false) cout << "can't find the user" << endl;
											else if (qqusermanage.isInGroup(number_of_users, number1) == false) cout << "not in the group" << endl;
											else if (qqusermanage.Isinminigroup(number_of_users, number1) == true) cout << "already in the temporary team" << endl;
											else {
												temp = true;
												qqusermanage.Getinminigroup(number_of_users, number1);
											}
										} while (temp == false);
										temp = false;
									}
									qqusermanage.show2(number1);
									break;
								case'6':
									qqusermanage.Deleteminigroup(number1);
									cout << "already dismiss the temporary team" << endl;
									break;
								case'7':
									cout << "ps：this function can build a new MicroBlog group，same member as the QQ group（only the member has MicroBlog account can join in the team）" << endl;
									if (mb_user_now == 0) cout << "you don't have account in MicroBlog，can't use this function" << endl;
									else {
										number2 = qqusermanage.makembloggroup(number1); 
										cout << "succeed" << endl;
										mbusermanage.show2(number2);
									}
									break;
								case'8':
									cout << "ps：this function can build a new MicroBlog group，same member as the QQ group（only the member has MicroBlog account can join in the team）" << endl;
									if (wx_user_now == 0) cout << "you haven't bind with Wechat，can't use this function" << endl;
									else {
										number2 = qqusermanage.makewechatgroup(number1);
										cout << "succeed" << endl;
										wcusermanage.show2(number2);
									}
									break;
								default:manage = false;
								}
							} while (manage == true);
						}
						else if (qqusermanage.isManager(qq_user_now, number1)) {
							qqusermanage.show2(number1);
							manage = true;
							do {
								cout << "as manager, you can：1.invite member 2.kick out members" << endl;
								cin >> input;
								switch (input) {
								case '1':
									cout << "please enter the friend's ID you want to invite to the group：";
									cin >> number2;
									if (qqusermanage.Searching(number2) == false) cout << "can't find the user" << endl;
									else if (qqusermanage.isInGroup(number2, number1)) { cout << "he's already in the group" << endl; }
									else if (qqusermanage.isFriend(qq_user_now, number2)) { qqusermanage.ingroup(number1, number2); cout << "he has already joined in the group" << endl; qqusermanage.show2(number1); }
									else cout << "you're not friends" << endl;
									break;
								case '2':
									cout << "please enter the friend's ID you want to kick out from the group：";
									cin >> number2;
									if (qqusermanage.Searching(number2) == false) cout << "can't find the user" << endl;
									else if (qqusermanage.isHead(number2, number1)) { cout << "can't kick out the leader" << endl; }
									else if (qqusermanage.isManager(number2, number1)) { cout << "can't kick out the manager" << endl; }
									else if (qqusermanage.isInGroup(number2, number1) == false) cout << "he's already not in the group" << endl;
									else { qqusermanage.outgroup(number1, number2); cout << "he's already not in the group" << endl; qqusermanage.show2(number1); }
									break;
								default:manage = false;
								}
							} while (manage == true);
						}
						else cout << "you're not the leader or manager" << endl;
					}
					else cout << "you're not in the group" << endl;
					break;
				case'9':
					cout << "please enter name of the new group" << endl;
					cin >> nickname;
					qqusermanage.AddGroup(nickname, qq_user_now, date_now);
					cout << "succeed building a group" << endl;
					qqusermanage.show2(qqusermanage.Number_of_Groups() + 1000);
					break;
				case'a':
					if (qqusermanage.returnmBlog(qq_user_now) = 0) { cout << "register MicroBlog account with ID " << mb_user_now << endl; }
					else { cout << "don't have account in MicroBlog account" << endl; }
					if (qqusermanage.returnWeChat(qq_user_now) = 0) { cout << "bind Wechat account with ID " << wx_user_now << endl; }
					else { cout << "haven't bind the Wechat account" << endl; }
					break;
				case'b':
					if (mb_user_now == 0) {
						cout << "Are you sure to register MicroBlog account？（MicroBlogID will be same as QQ account，and will share the same individual info with QQ） 1.register other：not register" << endl;
						cin >> input;
						if (input == '1') {
							mbusermanage.open(qq_user_now);
							mb_user_now = qq_user_now;
							cout << "succeed registering" << endl;
							mbusermanage.show(mb_user_now);
							qqusermanage.changemblog(qq_user_now, mb_user_now);
							mbusermanage.changeqq(mb_user_now, qq_user_now);
						}
					}
					else { cout << "already register MicroBlog account" << endl; }
					break;
				case'c':
					if (wx_user_now == 0) {
						cout << "please enter the Wechat account you want to bind with？" << endl;
						cin >> number1;
						if (wcusermanage.Searching(number1)) {
							qqusermanage.changewechat(qq_user_now, number1);
							wcusermanage.changeqq(number1, qq_user_now);
							if (mbusermanage.Searching(qq_user_now)) { 
								wcusermanage.changemblog(number1, qq_user_now); 
								mbusermanage.changewechat(qq_user_now, number1);
							}
							wx_user_now = number1;
							cout << "succeed binding the account" << endl;
						}
						else { cout << "can't find Wechat account" << endl; }
					}
					else { cout << "already bind this Wechat account，can't bind again" << endl; }
					break;
				case'd':
					if (wx_user_now = 0) {
						qqusermanage.changewechat(qq_user_now, 0);
						mbusermanage.changewechat(qq_user_now, 0);
						wcusermanage.changeqq(wx_user_now, 0);
						wcusermanage.changemblog(wx_user_now, 0);
						wx_user_now = 0;
						cout << "already unbound" << endl;
					}
					else { cout << "unbound, and can't remove the binding relations" << endl; }
					break;
				case'e':
					if (mb_user_now == 0)
						cout << "don't have account in MicroBlog，can't use the function" << endl;
					else {
						mbusermanage.showfriendlist(mb_user_now);
						cout << "please choose a MicroBlog friends to be your QQ friends：" << endl;//输入0退出
						cin >> number1;
						if (number1 == 0) break;
						if (mbusermanage.isFriend(mb_user_now, number1)) {
							if (mbusermanage.returnqq(number1) == 0) cout << "he don't have account in QQ service，can't add him as friends" << endl;
							else { qqusermanage.becomefriends(qq_user_now, number1); cout << "success adding the friend" << endl; qqusermanage.showfriendlist(qq_user_now); }
						}
						else { cout << "he's not your MicroBlog friends，can't add him as your qq friends" << endl; }
					}
					break;
				case'f':
					if (wx_user_now == 0)
						cout << "haven't bound Wechat，can't use the function" << endl;
					else {
						wcusermanage.showfriendlist(wx_user_now);
						cout << "please enter choose a Wechat friends to be your QQ friends：" << endl;//（输入0退出）
						cin >> number1;
						if (number1 == 0) break;
						if (wcusermanage.isFriend(wx_user_now, number1)) {
							if (wcusermanage.returnqq(number1) == 0) cout << "he hasn't bind QQ account，can't add him as friends" << endl;
							else { number1 = wcusermanage.returnqq(number1)->ID(); qqusermanage.becomefriends(qq_user_now, number1); cout << "success adding the friend" << endl; qqusermanage.showfriendlist(qq_user_now); }
						}
						else { cout << "he's not your MicroBlog friends，can't add him as your qq friends" << endl; }
					}
					break;
				case'0':status_online = false; qq_user_now = 0; mb_user_now = 0; wx_user_now = 0; social_platform = 0; cout << endl; break;
				default:cout << "invalid common" << endl;
				}
			} while (status_online == true);
		}
		while (social_platform == 2) {
			do {
				cout << "1.log in account 2.register a new account" << endl;
				cin >> input;
				switch (input) {
				case '1':
					cout << "please enter your MicroBlogID：";
					cin >> number1;
					if (mbusermanage.Searching(number1)) {
						status_online = true;
						mb_user_now = number1;
						cout << "log in succeed" << endl;
						mbusermanage.show(number1);
						if (mbusermanage.returnqq(number1) = 0) {
							qq_user_now = mbusermanage.returnqq(mb_user_now)->ID();
							cout << "have loged in QQ with ID" << qq_user_now << endl;
						}
						else { cout << "don't have account in QQ" << endl; }
						if (mbusermanage.returnWeChat(number1) = 0) {
							wx_user_now = mbusermanage.returnWeChat(mb_user_now)->ID();
							cout << "have loged Wechat with ID" << wx_user_now << endl;
						}
						else { cout << "haven't bind the Wechat account" << endl; }
					}
					else { cout << "login failed" << endl; status_online = false; }
					break;
				case '2':
					cout << "please enter your nickname：" << endl;
					cin >> nickname;
					do {
						cout << "please enter your birhday(8 number)：" << endl;
						cin >> number1;
					} while ((number1 < 19000101) or (number1 > 20200101) or (((number1 % 10000) / 100) > 12) or (((number1 % 10000) / 100) < 1) or ((number1 % 100) > 31) or ((number1 % 100) < 1));
					cout << "please enter ：" << endl;
					cin >> birthday;
					mbusermanage.AddUser(nickname, number1, birthday, date_now);
					cout << "suceed registering MicroBlog with ID" << mbusermanage.Number_of_Users() + 10000 << endl;
					mb_user_now = mbusermanage.Number_of_Users() + 10000;
					status_online = true;
					cout << endl;
					mbusermanage.show(mbusermanage.Number_of_Users() + 10000);
					cout << "status:online" << endl;
					mbusermanage.open(mb_user_now);
					qqusermanage.AddUser(nickname, number1, birthday, date_now);//预留qqid位置（这么做是因为qq与MicroBlog号码必须一致）
					break;
				default:
					social_platform = 0; out = true;
				}
			} while ((status_online == false) && (out == false));
			do {
				if (out) { out = false; break; }
				cout << endl << "choose your next action" << endl;
				cout << "1.change individual information 2.check for friends' info 3.add friends 4.delete friends 5.check for group info" << endl
					<< "6.enter in group  7.withdraw from group 8.manage group 9.create a new group 0.ESC" << endl
					<< "a.check for the binding relations b.register QQ account c.bind Wechat account d.unbound Wechat account" << endl
					<< "e.check and add QQ friends f.check and add Wechat friends" << endl;
				cout << "（ps：you can add MicroBlog friends by ID,but you need to be invited into MicroBlog group ）" << endl;
				cin >> input;
				switch (input) {
				case'1':mbusermanage.Modify(mb_user_now); mbusermanage.show(mb_user_now); break;
				case'2':
					cout << "please enter the user's MicroBlogID：" << endl;
					cin >> number1;
					if (mbusermanage.Searching(number1)) mbusermanage.show(number1);
					else cout << "can't find the user" << endl;
					break;
				case'3':
					mbusermanage.showfriendlist(mb_user_now);
					cout << "please enter the user's ID you want to add as friends：" << endl;
					cin >> number1;
					if (mbusermanage.isFriend(mb_user_now, number1)) cout << "already become friends" << endl;
					else if (mbusermanage.Searching(number1) == false) cout << "can't find the user" << endl;
					else if (number1 == mb_user_now) cout << "can't add yourself as friends" << endl;
					else { mbusermanage.becomefriends(mb_user_now, number1); cout << "success adding the friend" << endl; mbusermanage.showfriendlist(mb_user_now); }
					break;
				case'4':
					mbusermanage.showfriendlist(mb_user_now);
					cout << "please enter the friend's ID you want to delete：" << endl;
					cin >> number1;
					if (mbusermanage.isFriend(mb_user_now, number1)) { mbusermanage.deletefriends(mb_user_now, number1); cout << "succeed deleting friends" << endl; mbusermanage.showfriendlist(mb_user_now); }
					else { cout << "you're not friends" << endl; }
					break;
				case'5':
					cout << "please enter the group number" << endl;
					cin >> number1;
					if (mbusermanage.isInGroup(mb_user_now, number1)) mbusermanage.show2(number1);
					else cout << "you're not in the group" << endl;
					break;
					//QQ群通过输入群号直接加入 Wechat群通过接受他人邀请加入
				case'6':
					mbusermanage.showgrouplist(mb_user_now);
					cout << "please enter the group number";
					cin >> number1;
					if (mbusermanage.isInGroup(mb_user_now, number1)) {
						cout << "please enter the frine's ID you want to invite to the group：";
						cin >> number2;
						if (mbusermanage.Searching(number2) == false) cout << "can't find the user" << endl;
						else if (mbusermanage.isInGroup(number2, number1)) { cout << "he's already in the group" << endl; }
						else if (mbusermanage.isFriend(mb_user_now, number2)) { mbusermanage.ingroup(number1, number2); cout << "he succeeds joining in the group" << endl; mbusermanage.show2(number1); }
						else cout << "you're not friends" << endl;
					}
					else cout << "you're not in the group, so you can't invite others" << endl;
					break;
				case '7':
					mbusermanage.showgrouplist(mb_user_now);
					cout << "please enter the group number you want to withdraw from：" << endl;
					cin >> number1;
					if ((mbusermanage.isInGroup(mb_user_now, number1)) and (mbusermanage.isHead(mb_user_now, number1) == false)) {	
						mbusermanage.outgroup(number1, mb_user_now); 
						cout << "you have withdrawn from the group" << endl; 
						mbusermanage.showgrouplist(mb_user_now); 
					}
					else if (mbusermanage.isHead(mb_user_now, number1))cout << "leader can't withdraw from the group" << endl;
					else cout << "you're not in the group" << endl;
					break;
				case '8':
					mbusermanage.showgrouplist(mb_user_now);
					cout << "please enter the group number you want to manage" << endl;
					cin >> number1;
					if (mbusermanage.isInGroup(mb_user_now, number1)) {
						if (mbusermanage.isHead(mb_user_now, number1)) {
							mbusermanage.show2(number1);
							manage = true;
							do {
								cout << "as leader，you can：1.invite members 2.kikc out members" << endl
									<< "7.change manage mode to QQ group 8.change manage mode to Wechat group" << endl;
								cin >> input;
								switch (input) {
								case '1':
									cout << "please enter the friend's ID you want to invite to the group：";
									cin >> number2;
									if (mbusermanage.Searching(number2) == false) cout << "can't find the user" << endl;
									else if (mbusermanage.isInGroup(number2, number1)) { cout << "he's already in the group" << endl; }
									else if (mbusermanage.isFriend(mb_user_now, number2)) { mbusermanage.ingroup(number1, number2); cout << "he joined the group" << endl; mbusermanage.show2(number1); }
									else cout << "you're not friends" << endl;
									break;
								case '2':
									cout << "please enter the member's ID you want to kick out：";
									cin >> number2;
									if (mbusermanage.Searching(number2) == false) cout << "can't find the user" << endl;
									else if (number2 == mb_user_now) { cout << "can't kick out yourself" << endl; }
									else if (mbusermanage.isInGroup(number2, number1)) {
										mbusermanage.outgroup(number1, number2);
										cout << "he's already not in the group" << endl;
										mbusermanage.show2(number1);
									}
									else cout << "he's already not in the group";
									break;
								case'7':
									cout << "ps：this function can build a new QQ group with the same group members as MicroBlog(only the has QQ account can join in the group）" << endl;
									if (qq_user_now == 0) cout << "你don't have account in QQ，can't use this function" << endl;
									else {
										number2 = mbusermanage.makeqqgroup(number1);
										cout << "succeed" << endl;
										qqusermanage.show2(number2);
									}
									break;
								case'8':
									cout << "ps：this function can build a new Wechat group with the same group members as MicroBlog(only the has Wechat account can join in the group）" << endl;
									if (wx_user_now == 0) cout << "you haven't bind with Wechat，can't use this function" << endl;
									else {
										number2 = mbusermanage.makewechatgroup(number1);
										cout << "succeed" << endl;
										wcusermanage.show2(number2);
									}
									break;
								default:manage = false;
								}
							} while (manage == true);
						}
						else cout << "you're not the leader" << endl;
					}
					else cout << "you're not in the group" << endl;
					break;
				case'9':
					cout << "please enter name of the new group" << endl;
					cin >> nickname;
					mbusermanage.AddGroup(nickname, mb_user_now, date_now);
					cout << "succeed building a group" << endl;
					mbusermanage.show2(mbusermanage.Number_of_Groups() + 1000);
					break;
				case'a':
					if (mbusermanage.returnqq(mb_user_now) = 0) { cout << "register QQ with ID" << qq_user_now << endl; }
					else { cout << "don't have account in QQ" << endl; }
					if (mbusermanage.returnWeChat(mb_user_now) = 0) { cout << "bind Wechat with ID" << wx_user_now << endl; }
					else { cout << "haven't bind the Wechat account" << endl; }
					break;
				case'b':
					if (qq_user_now == 0) {
						cout << "are you to register a QQ account？（same MicroBlogID as QQID，and will get individual info from QQ automatically） 1.register other:not register" << endl;
						cin >> input;
						if (input == '1') {
							qqusermanage.open(mb_user_now);
							qq_user_now = mb_user_now;
							cout << "succeed registering" << endl;
							qqusermanage.show(qq_user_now);
							mbusermanage.changeqq(mb_user_now, qq_user_now);
							qqusermanage.changemblog(qq_user_now, mb_user_now);
						}
					}
					else { cout << "already register QQ account，don't neeed to register again" << endl; }
					break;
				case'c':
					if (wx_user_now == 0) {
						cout << "please enter the Wechat account you want to bind with？" << endl;
						cin >> number1;
						if (wcusermanage.Searching(number1)) {
							mbusermanage.changewechat(mb_user_now, number1);
							wcusermanage.changemblog(number1, mb_user_now);
							if (qqusermanage.Searching(mb_user_now)) {
								qqusermanage.changewechat(mb_user_now, number1);
								wcusermanage.changeqq(number1, mb_user_now);
							}
							wx_user_now = number1;
							cout << "succeed binding the account" << endl;
						}
						else { cout << "can't find the Wechat account" << endl; }
					}
					else { cout << "have already bound Wechat account，can't bind again" << endl; }
					break;
				case'd':
					if (wx_user_now = 0) {
						mbusermanage.changewechat(mb_user_now, 0);
						qqusermanage.changewechat(mb_user_now, 0);
						wcusermanage.changeqq(wx_user_now, 0);
						wcusermanage.changemblog(wx_user_now, 0);
						wx_user_now = 0;
						cout << "already unbound" << endl;
					}
					else { cout << "unbound, and can't remove the binding relations" << endl; }
					break;
				case'e':
					if (qq_user_now == 0)
						cout << "don't have account in QQ，can't use the function" << endl;
					else {
						qqusermanage.showfriendlist(qq_user_now);
						cout << "please enter the QQ friends you want to add as MicroBlog friends（enter 0 exit）：" << endl;
						cin >> number1;
						if (number1 == 0) break;
						if (qqusermanage.isFriend(qq_user_now, number1)) {
							if (qqusermanage.returnmBlog(number1) == 0) cout << "he don't have account in MicroBlog ，can't add him as friend" << endl;
							else { mbusermanage.becomefriends(qq_user_now, number1); cout << "success adding the friend" << endl; mbusermanage.showfriendlist(mb_user_now); }
						}
						else { cout << "he's not your QQ friends，can't add him as your MicroBlog friends" << endl; }
					}
					break;
				case'f':
					if (wx_user_now == 0)
						cout << "haven'r bind Wechat，can't use the function" << endl;
					else {
						wcusermanage.showfriendlist(wx_user_now);
						cout << "please enter the MicroBlog friends you want to add as Wechat friends（enter 0 exit）：" << endl;
						cin >> number1;
						if (number1 == 0) break;
						if (wcusermanage.isFriend(wx_user_now, number1)) {
							if (wcusermanage.returnmBlog(number1) == 0) cout << "he hasn't bind MicroBlog account，can't add him as friend" << endl;
							else { number1 = wcusermanage.returnmBlog(number1)->ID(); mbusermanage.becomefriends(mb_user_now, number1); cout << "success adding the friend" << endl; mbusermanage.showfriendlist(mb_user_now); }
						}
						else { cout << "he's not your Wechat friends，can't add him as your MicroBlog friends" << endl; }
					}
					break;
				case'0':status_online = false; qq_user_now = 0; mb_user_now = 0; wx_user_now = 0; social_platform = 0; cout << endl; break;
				default:cout << "invalid common" << endl;
				}
			} while (status_online == true);
		}
		while (social_platform == 3) {
			do {
				cout << "1.log in account 2.register a new account" << endl;
				cin >> input;
				switch (input) {
				case '1':
					cout << "please enter your WechatID：";
					cin >> number1;
					if (wcusermanage.Searching(number1)) {
						status_online = true;
						wx_user_now = number1;
						cout << "log in succeed" << endl;
						wcusermanage.show(number1);
						if (wcusermanage.returnqq(number1) = 0) {
							qq_user_now = wcusermanage.returnqq(wx_user_now)->ID();
							cout << "already log in the QQ with ID" << qq_user_now << endl;
						}
						else { cout << "can't bind QQ account" << endl; }
						if (wcusermanage.returnmBlog(number1) = 0) {
							mb_user_now = wcusermanage.returnmBlog(wx_user_now)->ID();
							cout << "already log in MicroBlog with ID" << mb_user_now << endl;
						}
						else { cout << "haven't bound MicroBlog account" << endl; }
					}
					else { cout << "log in failed" << endl; status_online = false; }
					break;
				case '2':
					cout << "please enter your nickname：" << endl;
					cin >> nickname;
					do {
						cout << "please enter your birhday(8 number)：" << endl;
						cin >> number1;
					} while ((number1 < 19000101) or (number1 > 20200101) or (((number1 % 10000) / 100) > 12) or (((number1 % 10000) / 100) < 1) or ((number1 % 100) > 31) or ((number1 % 100) < 1));
					cout << "please enter ：" << endl;
					cin >> birthday;
					wcusermanage.AddUser(nickname, number1, birthday, date_now);
					cout << "already registered Wechat with ID" << wcusermanage.Number_of_Users() + 20000 << endl;
					wx_user_now = wcusermanage.Number_of_Users() + 20000;
					status_online = true;
					cout << endl;
					wcusermanage.show(wcusermanage.Number_of_Users() + 20000);
					cout << "status:online" << endl;
					break;
				default:
					social_platform = 0; out = true;
				}
			} while ((status_online == false) && (out == false));
			do {
				if (out) { out = false; break; }
				cout << endl << "next you can：" << endl;
				cout << endl << "choose your next action" << endl;
				cout << "1.change individual information 2.check for friends' info 3.add friends 4.delete friends 5.check for group info" << endl
					<< "6.enter in group 7.withdraw from group 8.manage group 9.create a new group 0.ESC" << endl
					<< "a.check bingding info with QQ b.bind QQ account c.dismiss binding with QQ account" << endl //一个QQ号（包括QQ、MicroBlog）只能绑定一个Wechat
					<< "e.check and add QQ friends f.check and add MicroBlog friends" << endl;
					<< "a.check for the binding relations b.register QQ account c.bind Wechat account d.unbound Wechat account" << endl
					<< "e.check and add QQ friends f.check and add Wechat friends" << endl;
				cout << "（ps：you can add Wechat friends by ID,but you need to be invited into Wechat group ）" << endl;
				cin >> input;
				switch (input) {
				case'1':wcusermanage.Modify(wx_user_now); wcusermanage.show(wx_user_now); break;
				case'2':
					cout << "please enter the user's WechatID：" << endl;
					cin >> number1;
					if (wcusermanage.Searching(number1)) wcusermanage.show(number1);
					else cout << "can't find theuser" << endl;
					break;
				case'3':
					wcusermanage.showfriendlist(wx_user_now);
					cout << "please enter friends's：" << endl;
					cin >> number1;
					if (wcusermanage.isFriend(wx_user_now, number1)) cout << "you're already friends" << endl;
					else if (wcusermanage.Searching(number1) == false) cout << "can't find the user" << endl;
					else if (number1 == wx_user_now) cout << "can't add yourself" << endl;
					else { wcusermanage.becomefriends(wx_user_now, number1); cout << "success adding the friend" << endl; wcusermanage.showfriendlist(wx_user_now); }
					break;
				case'4':
					wcusermanage.showfriendlist(wx_user_now);
					cout << "please enter friend's ID you want to delete：" << endl;
					cin >> number1;
					if (wcusermanage.isFriend(wx_user_now, number1)) { wcusermanage.deletefriends(wx_user_now, number1); cout << "succeed deleting friends" << endl; wcusermanage.showfriendlist(wx_user_now); }
					else { cout << "you're not friends" << endl; }
					break;
				case'5':
					cout << "please enter the group number" << endl;
					cin >> number1;
					if (wcusermanage.isInGroup(wx_user_now, number1)) wcusermanage.show2(number1);
					else cout << "you're not in the group" << endl;
					break;
					//QQ群通过输入群号直接加入 Wechat群通过接受他人邀请加入
				case'6':
					wcusermanage.showgrouplist(wx_user_now);
					cout << "please enter the group number";
					cin >> number1;
					if (wcusermanage.isInGroup(wx_user_now, number1)) {
						cout << "please enter the friend's ID you want to invite to the group：";
						cin >> number2;
						if (wcusermanage.Searching(number2) == false) cout << "can't find the user" << endl;
						else if (wcusermanage.isInGroup(number2, number1)) { cout << "he's already in the group" << endl; }
						else if (wcusermanage.isFriend(wx_user_now, number2)) { wcusermanage.ingroup(number1, number2); cout << "he joined in the group" << endl; wcusermanage.show2(number1); }
						else cout << "you're not friends" << endl;
					}
					else cout << "you're not in the group, can't invite others" << endl;
					break;
				case '7':
					wcusermanage.showgrouplist(wx_user_now);
					cout << "please enter the group ID you want to withdraw from：" << endl;
					cin >> number1;
					if ((wcusermanage.isInGroup(wx_user_now, number1)) and (wcusermanage.isHead(wx_user_now, number1) == false))
						{ wcusermanage.outgroup(number1, wx_user_now); cout << "you have withdrawn from the group" << endl; wcusermanage.showgrouplist(wx_user_now);}
					else if (wcusermanage.isHead(wx_user_now, number1))cout << "leader can't withdraw from the group" << endl;
					else cout << "you're not in the group" << endl;
					break;
				case '8':
					wcusermanage.showgrouplist(wx_user_now);
					cout << "please enter the group ID you want to manage：" << endl;
					cin >> number1;
					if (wcusermanage.isInGroup(wx_user_now, number1)) {
						if (wcusermanage.isHead(wx_user_now, number1)) {
							wcusermanage.show2(number1);
							manage = true;
							do {
								cout << "as leader，you can：1.invite members 2.kick out members" << endl
									<< "7.change manage mode to QQ group 8.change manage mode to Wechat group" << endl;
								cin >> input;
								switch (input) {
								case '1':
									cout << "please enter the friend's ID you want to invite to the group：";
									cin >> number2;
									if (wcusermanage.Searching(number2) == false) cout << "can't find the user" << endl;
									else if (wcusermanage.isInGroup(number2, number1)) { cout << "he's already in the group" << endl; }
									else if (wcusermanage.isFriend(wx_user_now, number2)) { wcusermanage.ingroup(number1, number2); cout << "he joined in the group" << endl; wcusermanage.show2(number1); }
									else cout << "you're not friends" << endl;
									break;
								case '2':
									cout << "please enter the member's ID you want to kick out：";
									cin >> number2;
									if (wcusermanage.Searching(number2) == false) cout << "can't find the user" << endl;
									else if (number2 == wx_user_now) { cout << "can't kick out yourself" << endl; }
									else if (wcusermanage.isInGroup(number2, number1)) {
										wcusermanage.outgroup(number1, number2);
										cout << "he's already not in the group" << endl;
										wcusermanage.show2(number1);
									}
									else cout << "he's already not in the group";
								case'7':
									cout << "ps：this function can build a new QQ group with the same group members as Wechat(only the has QQ account can join in the group）" << endl;
									if (qq_user_now == 0) cout << "you haven't bind with QQ，can't use this function" << endl;
									else {
										number2 = wcusermanage.makeqqgroup(number1);
										cout << "succeed" << endl;
										qqusermanage.show2(number2);
									}
									break;
								case'8':
									cout << "ps：this function can build a new MicroBlog group with the same group members as Wechat(only the has MicroBlog account can join in the group）" << endl;
									if (mb_user_now == 0) cout << "you haven't bind with MicroBlog，can't use this function" << endl;
									else {
										number2 = wcusermanage.makembloggroup(number1);
										cout << "succeed" << endl;
										mbusermanage.show2(number2);
									}
									break;
									break;
								default:manage = false;
								}
							} while (manage == true);
						}
						else cout << "you're not the leader" << endl;
					}
					else cout << "you're not in the group" << endl;
					break;
				case'9':
					cout << "please enter name of the new group" << endl;
					cin >> nickname;
					wcusermanage.AddGroup(nickname, wx_user_now, date_now);
					cout << "succeed building a group" << endl;
					wcusermanage.show2(wcusermanage.Number_of_Groups() + 1000);
					break;
				case'a':
					if (wcusermanage.returnqq(wx_user_now) = 0) { cout << "bind QQ account with" << qq_user_now << endl; }
					else if (wcusermanage.returnmBlog(wx_user_now) = 0) { cout << "bind QQ account with" << mb_user_now << endl; }
					else { cout << "can't bind QQ account" << endl; }
					break;
				case'b':
					if ((qq_user_now == 0) && (mb_user_now == 0)) {
						cout << "please enter the QQ account you want to bind with" << endl;
						cin >> number1;
						if (qqusermanage.Searching(number1)) {
							qqusermanage.changewechat(number1, wx_user_now);
							wcusermanage.changeqq(wx_user_now, number1);
							qq_user_now = number1;
							if (mbusermanage.Searching(number1)) { 						
								mbusermanage.changewechat(number1, wx_user_now);							
								wcusermanage.changemblog(wx_user_now, number1);
								mb_user_now = number1;
							}
							cout << "succeed binding the account" << endl;
						}
						else if (mbusermanage.Searching(number1)) {
							mbusermanage.changewechat(number1, wx_user_now);
							wcusermanage.changemblog(wx_user_now, number1);
							mb_user_now = number1;
							if (qqusermanage.Searching(number1)) { 
								qqusermanage.changewechat(number1, wx_user_now); 
								qq_user_now = number1; 							
								wcusermanage.changeqq(wx_user_now, number1);
							}
							cout << "succeed binding the account" << endl;
						}
						else { cout << "can't find the QQ account" << endl; }
					}
					else { cout << "can't bind the QQ account because already binded" << endl; }
					break;
				case'c':
					if ((qq_user_now = 0) || (mb_user_now = 0)) {
						if (qq_user_now = 0) qqusermanage.changewechat(qq_user_now, 0);
						if (mb_user_now = 0) mbusermanage.changewechat(mb_user_now, 0);
						wcusermanage.changeqq(wx_user_now, 0);
						wcusermanage.changemblog(wx_user_now, 0);
						qq_user_now = 0;
						mb_user_now = 0;
						cout << "already unbound" << endl;
					}
					else { cout << "unbound, and can't remove the binding relations" << endl; }
					break;
				case'e':
					if (qq_user_now == 0)
						cout << "haven't bound with QQ，can't use the function" << endl;
					else {
						qqusermanage.showfriendlist(qq_user_now);
						cout << "please enter QQ friends you want to add as Wechat friend(enter 0 exit）：" << endl;
						cin >> number1;
						if (number1 == 0) break;
						if (qqusermanage.isFriend(qq_user_now, number1)) {
							if (qqusermanage.returnWeChat(number1) == 0) cout << "he don't have account in Wechat，can't add him as friend" << endl;
							else { number1 = qqusermanage.returnWeChat(number1)->ID(); wcusermanage.becomefriends(wx_user_now, number1); cout << "success adding the friend" << endl; wcusermanage.showfriendlist(wx_user_now); }
						}
						else { cout << "he's not your QQ friends，can't add him as your Wechat friends" << endl; }
					}
					break;
				case'f':
					if (mb_user_now == 0)
						cout << "haven't bound with MicroBlog，can't use the function" << endl;
					else {
						mbusermanage.showfriendlist(qq_user_now);
						cout << "please enter MicroBlog friends you want to add as Wechat friend（enter 0 exit）：" << endl;
						cin >> number1;
						if (number1 == 0) break;
						if (mbusermanage.isFriend(mb_user_now, number1)) {
							if (mbusermanage.returnWeChat(number1) == 0) cout << "he don't have account in Wechat，can't add him as friend" << endl;
							else { number1 = mbusermanage.returnWeChat(number1)->ID(); wcusermanage.becomefriends(wx_user_now, number1); cout << "success adding the friend" << endl; wcusermanage.showfriendlist(wx_user_now); }
						}
						else { cout << "he's not your MicroBlog friends，can't add him as your Wechat friends" << endl; }
					}
					break;
				case'0':status_online = false; qq_user_now = 0; mb_user_now = 0; wx_user_now = 0; social_platform = 0; cout << endl; break;
				default:cout << "invalid common" << endl;
				}
			} while (status_online == true);
		}
	}while (1);
}