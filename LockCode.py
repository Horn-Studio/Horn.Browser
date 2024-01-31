import sys #line:5
from PyQt6 .QtWidgets import *#line:6
from PyQt6 .QtCore import *#line:7
from PyQt6 .QtGui import *#line:8
from PyQt6 .QtWebEngineWidgets import QWebEngineView #line:9
class MainWindow (QMainWindow ):#line:13
    def __init__ (OOO0O00OO00OO000O ,*OO0OOOO00000O0O00 ,**OO00O00000OO0O0O0 ):#line:15
        super ().__init__ (*OO0OOOO00000O0O00 ,**OO00O00000OO0O0O0 )#line:16
        OOO0O00OO00OO000O .setWindowTitle ('号角浏览器_Horn.Browser')#line:18
        OOO0O00OO00OO000O .resize (1600 ,900 )#line:20
        OOO0O00OO00OO000O .show ()#line:21
        OOO0O00OO00OO000O .tabWidget =QTabWidget ()#line:23
        OOO0O00OO00OO000O .tabWidget .setDocumentMode (True )#line:24
        OOO0O00OO00OO000O .tabWidget .setMovable (False )#line:25
        OOO0O00OO00OO000O .tabWidget .setTabsClosable (True )#line:26
        OOO0O00OO00OO000O .tabWidget .tabCloseRequested .connect (OOO0O00OO00OO000O .close_Tab )#line:27
        OOO0O00OO00OO000O .setCentralWidget (OOO0O00OO00OO000O .tabWidget )#line:28
        OOO0O00OO00OO000O .webview =WebEngineView (OOO0O00OO00OO000O )#line:31
        OOO0O00OO00OO000O .webview .load (QUrl ("file:///C:/Program%20Files/Horn.Browser/Stable.html"))#line:32
        OOO0O00OO00OO000O .create_tab (OOO0O00OO00OO000O .webview )#line:33
        O000O0O0O000OO0OO =QToolBar ('点击隐藏导航栏')#line:37
        O000O0O0O000OO0OO .setIconSize (QSize (32 ,32 ))#line:39
        OOO0O00OO00OO000O .addToolBar (O000O0O0O000OO0OO )#line:41
        O000OOO00OO000000 =QAction (QIcon ('icons/back.png'),'后退',OOO0O00OO00OO000O )#line:45
        OOOO0O0O000O00OO0 =QAction (QIcon ('icons/go.png'),'前进',OOO0O00OO00OO000O )#line:46
        O00O00OO0OO0000O0 =QAction (QIcon ('icons/refresh.png'),'刷新',OOO0O00OO00OO000O )#line:48
        O000OOO00OO000000 .triggered .connect (OOO0O00OO00OO000O .webview .back )#line:51
        OOOO0O0O000O00OO0 .triggered .connect (OOO0O00OO00OO000O .webview .forward )#line:52
        O00O00OO0OO0000O0 .triggered .connect (OOO0O00OO00OO000O .webview .reload )#line:54
        O000O0O0O000OO0OO .addAction (O000OOO00OO000000 )#line:57
        O000O0O0O000OO0OO .addAction (OOOO0O0O000O00OO0 )#line:58
        O000O0O0O000OO0OO .addAction (O00O00OO0OO0000O0 )#line:60
        OOO0O00OO00OO000O .urlbar =QLineEdit ()#line:63
        OOO0O00OO00OO000O .urlbar .returnPressed .connect (OOO0O00OO00OO000O .navigate_to_url )#line:65
        O000O0O0O000OO0OO .addSeparator ()#line:67
        O000O0O0O000OO0OO .addWidget (OOO0O00OO00OO000O .urlbar )#line:68
        OOO0O00OO00OO000O .webview .urlChanged .connect (OOO0O00OO00OO000O .renew_urlbar )#line:71
    def navigate_to_url (O00OOO0O0OOO000OO ):#line:74
        OO00OOOOO0O0000OO =QUrl (O00OOO0O0OOO000OO .urlbar .text ())#line:75
        if OO00OOOOO0O0000OO .scheme ()=='':#line:76
            OO00OOOOO0O0000OO .setScheme ('http')#line:77
        O00OOO0O0OOO000OO .webview .setUrl (OO00OOOOO0O0000OO )#line:78
    def renew_urlbar (O000O0O0O00O0OO00 ,OOO00000O000O000O ):#line:81
        O000O0O0O00O0OO00 .urlbar .setText (OOO00000O000O000O .toString ())#line:83
        O000O0O0O00O0OO00 .urlbar .setCursorPosition (0 )#line:84
    def create_tab (O00O00OOO0OOOOOOO ,O0OOOOO000OO0O00O ):#line:87
        O00O00OOO0OOOOOOO .tab =QWidget ()#line:88
        O00O00OOO0OOOOOOO .tabWidget .addTab (O00O00OOO0OOOOOOO .tab ,"标签页")#line:89
        O00O00OOO0OOOOOOO .tabWidget .setCurrentWidget (O00O00OOO0OOOOOOO .tab )#line:90
        O00O00OOO0OOOOOOO .Layout =QHBoxLayout (O00O00OOO0OOOOOOO .tab )#line:93
        O00O00OOO0OOOOOOO .Layout .setContentsMargins (0 ,0 ,0 ,0 )#line:94
        O00O00OOO0OOOOOOO .Layout .addWidget (O0OOOOO000OO0O00O )#line:95
    def close_Tab (OOO00O000O00O000O ,O0000000OO00OO0O0 ):#line:98
        if OOO00O000O00O000O .tabWidget .count ()>1 :#line:99
            OOO00O000O00O000O .tabWidget .removeTab (O0000000OO00OO0O0 )#line:100
class WebEngineView (QWebEngineView ):#line:107
    def __init__ (OOO0O0OOOOO000OO0 ,OOO00000O0O0O0O00 ,parent =None ):#line:109
        super (WebEngineView ,OOO0O0OOOOO000OO0 ).__init__ (parent )#line:110
        OOO0O0OOOOO000OO0 .mainwindow =OOO00000O0O0O0O00 #line:111
    def createWindow (OO000OO0OO000O00O ,OOOOOO00O00OO0000 ):#line:114
        OOO000O00O00000OO =WebEngineView (OO000OO0OO000O00O .mainwindow )#line:115
        OO000OO0OO000O00O .mainwindow .create_tab (OOO000O00O00000OO )#line:116
        return OOO000O00O00000OO #line:117
if __name__ =="__main__":#line:121
    app =QApplication (sys .argv )#line:122
    browser =MainWindow ()#line:124
    browser .show ()#line:125
    sys .exit (app .exec ())#line:127
