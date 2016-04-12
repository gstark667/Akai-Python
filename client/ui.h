class FriendsList: public QListWidget
{
private:
   QListWidgetItem *friend_items;

public:
   FriendsList(const FriendManager&);
   ~FriendsList();

   void addFriend(std::string userName, std::string iconPath std::string publicKey);
   void removeFriend(std::string userName);
};

class UI
{
private:
   
};
