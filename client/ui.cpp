#include "ui.h"

using namespace std;

MessageCompose::MessageCompose(QWidget *parent): QTextEdit(parent)
{

}

MessageHistory::MessageHistory(QWidget *parent): QScrollArea(parent)
{

}

MessagePane::MessagePane(QWidget *parent): QSplitter(Qt::Horizontal)
{

}

FriendsList::FriendsList(const FriendManager *friendManager): QListWidget()
{
   m_friendCount = friendManager->getFriendCount();
   m_friendItems = new QListWidgetItem*[friendManager->getFriendCount()];

   for (int i = 0; i < friendManager->getFriendCount(); ++i)
   {
      const Friend *curFriend = friendManager->getFriend(i);
      m_friendItems[i] = new QListWidgetItem(QIcon(curFriend->getIconPath().c_str()),
         curFriend->getUserName().c_str(), this);
   }
}

FriendsList::~FriendsList()
{
   delete[] m_friendItems;
   m_friendItems = nullptr;
}

MainSplit::MainSplit(const FriendManager *friendManager, QWidget *parent): QSplitter(parent)
{
   m_friendsList = new FriendsList(friendManager);
   addWidget(m_friendsList);
   addWidget(new QTextEdit());
}

MainSplit::MainSplit(const FriendManager *friendManager): QSplitter()
{
   m_friendsList = new FriendsList(friendManager);
   addWidget(m_friendsList);
   addWidget(new QTextEdit());
}

MainWindow::MainWindow(const FriendManager *friendManager)
{
   resize(500, 500);
   setWindowTitle("Akai");

   m_vboxLayout = new QVBoxLayout(this);
   m_mainSplit = new MainSplit(friendManager, this);
   m_vboxLayout->addWidget(m_mainSplit);
   m_vboxLayout->setSpacing(0);
   m_vboxLayout->setMargin(0);
}

UI::UI(int argc, char *argv[], const FriendManager *friendManager): QApplication(argc, argv)
{
   m_mainWindow = new MainWindow(friendManager);
   m_mainWindow->show();
}
