#ifndef H_FRIEND
#define H_FRIEND

#include <string>
#include <istream>
#include <ostream>
#include <vector>

class Friend
{
private:
   std::string m_userName;
   std::string m_iconPath;
   std::string m_publicKey;

public:
   Friend(): m_iconPath(""), m_userName(""), m_publicKey("") {};
   Friend(std::string userName, std::string iconPath, std::string publicKey);
   ~Friend() {};

   const std::string getUserName() const { return m_userName; };
   const std::string getIconPath() const { return m_iconPath; };
   const std::string getPublicKey() const { return m_publicKey; };

   friend std::istream& operator>>(std::istream&, Friend&);
   friend std::ostream& operator<<(std::ostream&, const Friend&);
};

class FriendManager
{
private:
   std::vector<Friend> m_friends;

   std::string m_friendsFilePath;

public:
   FriendManager();
   ~FriendManager();

   void readFriendsList();
   void writeFriendsList();

   void addFriend(std::string userName, std::string iconPath, std::string publicKey);
   void removeFriend(std::string userName);

   const std::vector<Friend> getFriends() const;
};

#endif
