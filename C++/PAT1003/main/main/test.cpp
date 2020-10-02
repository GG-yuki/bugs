#include <iostream> 
#include <map> 
#include <string> 
using namespace std; 
int main() {    map<string, int> m; // 定义⼀一个空的map m，键是string类型的，值是int类型的    
m["hello"] = 2; // 将key为"hello", value为2的键值对(key-value)存⼊入map中    
cout << m["hello"] << endl; // 访问map中key为"hello"的value, 如果key不不存在，则返 回0    
cout << m["world"] << endl;    m["world"] = 3; // 将"world"键对应的值修改为3    
m[","] = 1; // 设⽴立⼀一组键值对，键为"," 值为1    // ⽤用迭代器器遍历，输出map中所有的元素，键⽤用it->first获取，值⽤用it->second获取    
for (auto it = m.begin(); it != m.end(); it++) {        cout << it->first << " " << it->second << endl;    }    // 访问map的第⼀一个元素，输出它的键和值    
cout << m.begin()->first << " " << m.begin()->second << endl;    // 访问map的后⼀一个元素，输出它的键和值   
cout << m.rbegin()->first << " " << m.rbegin()->second << endl;    // 输出map的元素个数   
cout << m.size() << endl;    return 0; }
