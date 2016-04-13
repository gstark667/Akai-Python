GCC_COMPILER=gcc
GXX_COMPILER=g++
LINKER=g++

GCC_ARGUMENTS=-c -g -I/usr/include/qt4 -I/usr/include/qt4/QtCore -I/usr/include/qt4/QtGui
GXX_ARGUMENTS=-c -g -std=c++11 -I/usr/include/qt4 -I/usr/include/qt4/QtCore -I/usr/include/qt4/QtGui

LINKER_ARGUMENTS=-lQtCore -lQtGui -lpthread

GCC_COMMAND=$(GCC_COMPILER) $(GCC_ARGUMENTS)
GXX_COMMAND=$(GXX_COMPILER) $(GXX_ARGUMENTS)

LINKER_COMMAND=$(LINKER) $(LINKER_ARGUMENTS)

OBJDIR=./objects

$(OBJDIR)/akai.a: $(OBJDIR) \
   $(OBJDIR)/main.o \
   $(OBJDIR)/ui.o \
   $(OBJDIR)/friend.o
	$(LINKER_COMMAND) $(OBJDIR)/*.o -o $(OBJDIR)/akai.a 

$(OBJDIR)/main.o: $(OBJDIR) main.cpp
	$(GXX_COMMAND) main.cpp -o $(OBJDIR)/main.o

$(OBJDIR)/ui.o: $(OBJDIR) ui.cpp ui.h friend.h
	$(GXX_COMMAND) ui.cpp -o $(OBJDIR)/ui.o

$(OBJDIR)/friend.o: $(OBJDIR) friend.cpp friend.h
	$(GXX_COMMAND) friend.cpp -o $(OBJDIR)/friend.o

$(OBJDIR):
	mkdir $(OBJDIR)
