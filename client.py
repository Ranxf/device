import sys
import time
import rpyc

if __name__ == '__main__': 
    c = rpyc.classic.connect("192.168.2.174")
    #s = ServerProxy("http://192.168.2.174:8000") 
    #app = s.run_aut("C:\Program Files (x86)\cdxzrs\Xin300Client\XinStraightClient.exe")

    p = "C:\Program Files (x86)\cdxzrs\Xin300Client\XinStraightClient.exe"
    c.modules.clr
    c.modules.sys
    c.modules.sys.path.append(r'D:\IronPython\white')
    c.modules.clr.AddReferenceToFile("TestStack.White.dll")
    White = c.modules.TestStack.White
    InitializeOption = c.modules.TestStack.White.Factory.InitializeOption
    SearchCriteria = White.UIItems.Finders.SearchCriteria
    app = White.Application.Launch(p)
    time.sleep(5)
    win = app.GetWindow("ClientUserLoginWindow",InitializeOption.NoCache)
    login_button = SearchCriteria.ByAutomationId("BtnClientLogin")
    print dir(login_button)
    login = win.Get(login_button)
    login.Click()
    time.sleep(5)
    app.Close()
