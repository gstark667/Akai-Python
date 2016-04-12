GCC_COMPILER=gcc
GXX_COMPILER=g++
LINKER=g++

GCC_ARGUMENTS=-c -I/usr/include/qt4 -I/usr/include/qt4/QtCore -I/usr/include/qt4/QtGui
GXX_ARGUMENTS=-c -I/usr/include/qt4 -I/usr/include/qt4/QtCore -I/usr/include/qt4/QtGui

LINKER_ARGUMENTS=-lQtCore -lQtGui

GCC_COMMAND=$(GCC_COMPILER) $(GCC_ARGUMENTS)
GXX_COMMAND=$(GXX_COMPILER) $(GXX_ARGUMENTS)

LINKER_COMMAND=$(LINKER) $(LINKER_ARGUMENTS)

OBJDIR=./objects

$(OBJDIR)/akai.a: $(OBJDIR) $(OBJDIR)/main.o
	$(LINKER_COMMAND) $(OBJDIR)/*.o -o $(OBJDIR)/akai.a 

$(OBJDIR)/main.o: $(OBJDIR) main.cpp
	$(GXX_COMMAND) main.cpp -o $(OBJDIR)/main.o

$(OBJDIR):
	mkdir $(OBJDIR)
