#ifndef H_UI
#define H_UI

#include <QApplication>
#include <QWidget>
#include <QSplitter>
#include <QListWidget>
#include <QTextEdit>
#include <QVBoxLayout>
#include <string>
#include <thread>

#include "friend.h"

class FriendsList: public QListWidget
{
private:
   size_t m_friendCount;
   QListWidgetItem **m_friendItems;

public:
   FriendsList(const FriendManager*);
   ~FriendsList();

   void addFriend(std::string userName, std::string iconPath, std::string publicKey);
   void removeFriend(std::string userName);
};

class MainSplit: public QSplitter
{
private:
   FriendsList *m_friendsList;

public:
   MainSplit(const FriendManager *friendManager);
   MainSplit(const FriendManager *friendManager, QWidget *parent);
};

class MainWindow: public QWidget
{
private:
   MainSplit *m_mainSplit;
   QVBoxLayout *m_vboxLayout;

public:
   MainWindow(const FriendManager*);
};

class UI: public QApplication
{
private:
   MainWindow *m_mainWindow;

public:
   UI(int argc, char *argv[], const FriendManager *friendManager);
};

#endif
