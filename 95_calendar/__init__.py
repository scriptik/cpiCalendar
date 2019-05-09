# -*- coding: utf-8 -*- 

import pygame
import os


import time
import calendar
from datetime import datetime, date, timedelta

## local UI import
from UI.page  import Page
from UI.skin_manager import MySkinManager
from UI.constants import ICON_TYPES,Width,Height
from UI.icon_item import IconItem
from UI.icon_pool import MyIconPool
from UI.label  import Label
from UI.util_funcs import midRect
from UI.fonts  import fonts
from UI.multi_icon_item import MultiIconItem
from UI.keys_def   import CurKeys, IsKeyStartOrA, IsKeyMenuOrB

from libs.roundrects import aa_round_rect

class CalendarPage(Page):

    _Icons = {}
    _BGpng  = None
    _BGwidth = 320
    _BGheight = 200
    _BGlabel  = None
    _FreeLabel = None
    month = 5
    year = 2019
    nuTxtMonth = {}


    _HighColor = MySkinManager.GiveColor('High')
    #_FootMsg    = ["Nav.","","","Back",""]
    _FootMsg    = ["Nav","","","Back","Today"]

    def __init__(self):
        Page.__init__(self)

        self._Icons = {}



    def CurMonth(self):
        global month
        global year
        global cur_monyear
        global nuTxtMonth

        nuTxtMonth = {1 : "Jan", 2 : "Feb", 3 : "Mar",
                      4 : "Apr", 5 : "May", 6 :"Jun",
                      7 : "Jul", 8 : "Aug", 9 : "Sep",
                     10 : "Oct", 11 :"Nov", 12 :"Dec",
                     }

        time = datetime.now()
        month = int(time.now().strftime('%-m'))
        year = int(time.now().strftime('%Y'))
        cur_monyear = (nuTxtMonth[month])+" "+str(year)
        cal_list = calendar.monthcalendar(time.year, time.month)
        return cur_monyear, cal_list

    def NextMonth(self):
        global month
        global year
        global cur_monyear
        global nuTxtMonth

        if month !=12:
           month = month+1
        elif month == 12:
           month = 1
           year = year+1

        cur_monyear = (nuTxtMonth[month])+" "+str(year)
        self._monyearlabel.SetText(cur_monyear)
        self._callist = calendar.monthcalendar(year, month)

    def PreMonth(self):
        global month
        global year
        global cur_monyear
        global nuTxtMonth

        if month !=1:
           month = month-1
        elif month == 1:
           month = 12
           year = year-1

        cur_monyear = (nuTxtMonth[month])+" "+str(year)
        self._monyearlabel.SetText(cur_monyear)
        self._callist = calendar.monthcalendar(year, month)

    def NextYear(self):
        global month
        global year
        global cur_monyear
        global nuTxtMonth

        year = year+1
        cur_monyear = (nuTxtMonth[month])+" "+str(year)
        self._monyearlabel.SetText(cur_monyear)
        self._callist = calendar.monthcalendar(year, month)

    def PreYear(self):
        global month
        global year
        global cur_monyear
        global nuTxtMonth

        year = year-1
        cur_monyear = (nuTxtMonth[month])+" "+str(year)
        self._monyearlabel.SetText(cur_monyear)
        self._callist = calendar.monthcalendar(year, month)

    def MarkToDay(self):
        time = datetime.now()
        dayslist = calendar.monthcalendar(time.year, time.month)
        days = []
        for x in dayslist:
            for y in x:
                day.append(y)


    def GoToDay(self):
        self.CurMonth()
        self._monyearlabel.SetText(cur_monyear)
        self._callist = calendar.monthcalendar(year, month)

    def Init(self):


        self._dialog_index = 22

        self._CanvasHWND = self._Screen._CanvasHWND
        self._Width =  self._Screen._Width
        self._Height = self._Screen._Height

        self._BGpng = IconItem()
        self._BGpng._ImgSurf = MyIconPool._Icons["cpiCalbg5"]
        self._BGpng._MyType = ICON_TYPES["STAT"]
        self._BGpng._Parent = self

        self._monyearlabel = Label()
        self._monyearlabel.SetCanvasHWND(self._CanvasHWND)
        self._monyear, self._callist = self.CurMonth()
        self._monyearlabel.Init(self._monyear,fonts["varela15"])


        calnum = MultiIconItem()
        calnum._ImgSurf = MyIconPool._Icons["calnum"]
        calnum._MyType = ICON_TYPES["STAT"]
        calnum._Parent = self
        calnum._IconWidth = 35
        calnum._IconHeight = 26
        calnum.Adjust(0,0,134,372,0)
        self._Icons["calnum"] = calnum


    def KeyDown(self,event):
        if IsKeyMenuOrB(event.key):
            self.ReturnToUpLevelPage()
            self._Screen.Draw()
            self._Screen.SwapAndShow()

        if IsKeyStartOrA(event.key):
            self.GoToDay()
            self._Screen.Draw()
            self._Screen.SwapAndShow()

        if event.key == CurKeys["Right"]:
            self.NextMonth()
            self._Screen.Draw()
            self._Screen.SwapAndShow()

        if event.key == CurKeys["Left"]:
            self.PreMonth()
            self._Screen.Draw()
            self._Screen.SwapAndShow()

        if event.key == CurKeys["Up"]:
            self.NextYear()
            self._Screen.Draw()
            self._Screen.SwapAndShow()

        if event.key == CurKeys["Down"]:
            self.PreYear()
            self._Screen.Draw()
            self._Screen.SwapAndShow()

    def Draw(self):
        self.ClearCanvas()

        self._BGpng.NewCoord(5,-30)
        self._BGpng.Draw()

        self._monyearlabel.NewCoord(230,5)
        self._monyearlabel.Draw()

        #self._Icons["calnum"].NewCoord(157,45)
        #self._Icons["calnum"]._IconIndex = self._dialog_index
        #self._Icons["calnum"].DrawTopLeft()

        ydic = {0:45, 1:74, 2:106, 3:137, 4:167}
        calrow = {0:0, 1:1, 2:2, 3:3, 4:4}
        if len(self._callist) is 4:
          for j in range(4):
              x = 40
              y = ydic[j]
              row = calrow[j]
              for numbers in self._callist[row]:
                  if numbers != 0:
                     self._Icons["calnum"].NewCoord(x,y)
                     self._Icons["calnum"]._IconIndex = numbers
                     self._Icons["calnum"].DrawTopLeft()
                  x = x+39

        else:
          for j in range(5):
              x = 40
              y = ydic[j]
              row = calrow[j]
              for numbers in self._callist[row]:
                  if numbers != 0:
                     self._Icons["calnum"].NewCoord(x,y)
                     self._Icons["calnum"]._IconIndex = numbers
                     self._Icons["calnum"].DrawTopLeft()
                  x = x+39
          if len(self._callist) is 6:
             x = 40
             for numbers in self._callist[5]:
                 if numbers != 0:
                    self._Icons["calnum"].NewCoord(x,48)
                    self._Icons["calnum"]._IconIndex = numbers
                    self._Icons["calnum"].DrawTopLeft()
                 x = x+39




class APIOBJ(object):

    _CalendarPage = None
    def __init__(self):
        pass
    def Init(self,main_screen):
        self._CalendarPage = CalendarPage()

        self._CalendarPage._Screen = main_screen
        self._CalendarPage._Name ="Calendar"
        self._CalendarPage.Init()

    def API(self,main_screen):
        if main_screen !=None:
            main_screen.PushPage(self._CalendarPage)
            main_screen.Draw()
            main_screen.SwapAndShow()



OBJ = APIOBJ()
def Init(main_screen):
    OBJ.Init(main_screen)
def API(main_screen):
    OBJ.API(main_screen)
