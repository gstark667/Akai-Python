#include <fstream>
#include <iostream>

#include "friend.h"

using namespace std;

Friend::Friend(string iconPath, string userName, string publicKey)
{
   m_userName = userName;
   m_iconPath = iconPath;
   m_publicKey = publicKey;
}

istream& operator>>(istream &in, Friend &target)
{
   in >> target.m_userName;
   in >> target.m_iconPath;
   in >> target.m_publicKey;

   return in;
}

ostream& operator<<(ostream &out, const Friend &target)
{
   out << target.m_userName << ' ';
   out << target.m_iconPath << ' ';
   out << target.m_publicKey << endl;

   return out;
}


FriendManager::FriendManager()
{
   // this will be populated by a config manager call once it's implemented
   m_friendsFilePath = "/home/octalus/.config/akai/friendslist";

   readFriendsList();
}

FriendManager::~FriendManager()
{
   writeFriendsList();
}

void FriendManager::readFriendsList()
{
   Friend temp;
   ifstream friendsFile(m_friendsFilePath.c_str());

   if (friendsFile.good())
   {

      while (friendsFile >> temp)
      {
         m_friends.push_back(temp);
      }

      friendsFile.close();
   }
   else
   {
      cout << "Unable to open friends file" << endl;
   }
}

void FriendManager::writeFriendsList()
{
   ofstream friendsFile(m_friendsFilePath.c_str());

   for (vector<Friend>::iterator i = m_friends.begin(); i != m_friends.end(); ++i)
   {
      friendsFile << *i;
   }

   friendsFile.close();
}
