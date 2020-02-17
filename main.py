# Libs
import machine
import utime
import neopixel
import gc

# region Color

'''
Color
Aufabe:
  Save RGB Color

Func GetRGB | None | list[R:int, G:int, B:int]
Func SetRGB | Write RGB | None
'''
class Color():
    def __init__(self, r, g, b):
        self.R = r
        self.G = g
        self.B = b

    def GetRGB(self) -> list: return [self.R, self.G, self.B]

    def SetRGB(self, RGBList) -> None:
        self.R = RGBList[0]
        self.G = RGBList[1]
        self.B = RGBList[2]

    def SetRGB1(self, r, g, b):
        self.R = r
        self.G = g
        self.B = b


# endregion


# region OnLineCode

def Millis() -> int:  return utime.ticks_ms()  # static Func


def Sleep(ms) -> None: utime.sleep_ms(ms)  # static Func


# endregion


# region GUI_Enums

''' 
__MenuOisuEnum__ 
Aufgabe:
Ein Enum type für Menu / UI um zu wissen wo grade das Menu ist
'''
class __MenuPosiEnum__(object):
    def __init__(self):
        self.Null = 0
        self.Off = 1
        self.Option = 2
        self.SetColor1 = 3
        self.SetColor2 = 4
        self.SetColorOff = 5
        self.SetBlockTimeDown = 6
        self.SetOverBlockTimeDown = 7
        self.SetOverBlockHoldTime = 8
        self.SetColor1_R = 9
        self.SetColor1_G = 10
        self.SetColor1_B = 11
        self.SetColor2_R = 12
        self.SetColor2_G = 13
        self.SetColor2_B = 14
        self.SetColorOff_R = 15
        self.SetColorOff_G = 16
        self.SetColorOff_B = 17

'''
__MenuColorTypeEnum__
Augabe:
Ein Enum type für Menu / UI um zuwissen welche RGB Farbe geendert werden soll.
'''
class __MenuColorTypeEnum__(object):
    def __init__(self):
        self.Null = 0
        self.R = 1
        self.G = 2
        self.B = 3


'''
__MenuSaveEnum__
Ein Enum type für Menu / UI um zuwissen was mit den returnWert zuthuhen ist.
'''
class __MenuSaveEnum__(object):
    def __init__(self):
        self.Null = 0
        self.Save = 1
        self.NotSave = 2


MenuPosiEnum = __MenuPosiEnum__()
MenuColorTypeEnum = __MenuColorTypeEnum__()
MenuSaveEnum = __MenuSaveEnum__()

# endregion


# region LedWriter

'''
LED
Aufgabe:
Write LED Pixel

Func SetNewColor | Chance old RGB Colors to new RGB Colors and Write | None
'''
class LED():
    def __init__(self, size, high, dataPinAsInt):
        self.BarLedList = []
        self.Size = size
        self.High = high

        num = 0

        for s in range(size):
            left = []
            right = []
            leftRight = []

            for i in range(high):
                left.append(num)
                num += 1

            for i in range(high):
                right.append(num)
                num += 1

            right.reverse()

            for i in zip(left, right): leftRight.append((i, Color(0, 0, 0)))

            self.BarLedList.append(leftRight)

        if num != 0:
            self.Neo = neopixel.NeoPixel(machine.Pin(dataPinAsInt), num + 1)

    def SetNewColor(self, eqbarListColor):
        for barListNum in range(len(eqbarListColor)):

            for blockNum in range(len(barListNum)):

                rgbOld = self.BarLedList[barListNum][blockNum][2].GetRGB()
                rgbNew = eqbarListColor[barListNum][blockNum].GetRGB()

                if rgbOld[0] != rgbNew[0] or rgbOld[1] != rgbNew[1] or rgbOld[2] != rgbNew[2]:

                    self.BarLedList[barListNum][blockNum][2].SetRGB([rgbNew[0], rgbNew[1], rgbNew[2]])

                    self.neo[self.BarLedList[barListNum][blockNum][0]] = (rgbNew[0], rgbNew[1], rgbNew[2])
                    self.neo[self.BarLedList[barListNum][blockNum][1]] = (rgbNew[0], rgbNew[1], rgbNew[2])

                else:
                    pass

        self.neo.write()

        return


# endregion


# region ProgrammParas

'''
ProgrammParas
Augabe: Load Save Get Put => base Paras

Func Load | | None
Func SaveParas | | None
Func WriteDefault | | None
Func PrintParas | | None
'''
class ProgrammParas():
    def __init__(self, _self=False, default=False):
        self.pathToFile = "userParas"

        # Use Default
        if _self == True:
            self.size = 8  # Breite des Audioanalyzer
            self.high = 10  # Höre des Audioanalyzer
            self.colorList = [Color(0, 0, 255),  # Block Color1
                              Color(255, 0, 0),  # Block Color2
                              Color(0, 0, 0)  # Block ColorOff
                              ]
            self.blockFallTime = 200  # Fall des Block Pro Block in Ms
            self.overBlockFallTime = 250  # Fall des OverBlock Pro Block in Ms
            self.overBlockHoldTime = 500  # Warte es bis Fall gild für OverBlock
            self.dataPinAsInt = 21  # DATA Pin für LED

            # userParas gibt es nicht Or
            # Load Default
            # Create New userParas File with Default Paras
            if default == True:
                self.WriteDefault()

        else:
            try:
                reader = open(self.pathToFile, "r")
                reader.close()

                # File gibt es
                self.Load()
                return
            except:
                # File gibt es nicht
                ProgrammParas(_self=True, default=True)
                self.Load()
                return

    def Load(self) -> None:
        reader = open(self.pathToFile, "r")
        textList = []
        for i in reader:
            textList.append(i)

        self.size = int(textList[0])  # Breite des Audioanalyzer
        self.high = int(textList[1])  # Höre des Audioanalyzer
        self.colorList = [Color(int(textList[2]), int(textList[3]), int(textList[4])),  # Block Color1
                          Color(int(textList[5]), int(textList[6]), int(textList[7])),  # Block Color2
                          Color(int(textList[8]), int(textList[9]), int(textList[10]))  # Block ColorOff
                          ]
        self.blockFallTime = int(textList[11])  # Fall des Block Pro Block in Ms
        self.overBlockFallTime = int(textList[12])  # Fall des OverBlock Pro Block in Ms
        self.overBlockHoldTime = int(textList[13])  # Warte es bis Fall gild für OverBlock
        self.dataPinAsInt = int(textList[14])  # DATA Pin für LED

    def SaveParas(self) -> None:
        writer = open(self.pathToFile, "w")
        text = ""

        text += str(self.size) + "\n"
        text += str(self.high) + "\n"

        text += str(self.colorList[0].R) + "\n"
        text += str(self.colorList[0].G) + "\n"
        text += str(self.colorList[0].B) + "\n"
        text += str(self.colorList[1].R) + "\n"
        text += str(self.colorList[1].G) + "\n"
        text += str(self.colorList[1].B) + "\n"
        text += str(self.colorList[2].R) + "\n"
        text += str(self.colorList[2].G) + "\n"
        text += str(self.colorList[2].B) + "\n"

        text += str(self.blockFallTime) + "\n"
        text += str(self.overBlockFallTime) + "\n"
        text += str(self.overBlockHoldTime) + "\n"
        text += str(self.dataPinAsInt)

        writer.write(text)
        writer.close()

        return

    def WriteDefault(self) -> None:
        writer = open(self.pathToFile, "w")

        text = "8\n10\n0\n0\n255\n255\n0\n0\n0\n0\n0\n200\n250\n500\n21"

        writer.write(text)
        writer.close()
        return

    def PrintParas(self) -> None:
        text = ""

        text += str(self.size) + "\n"
        text += str(self.high) + "\n"

        text += str(self.colorList[0].R) + "\n"
        text += str(self.colorList[0].G) + "\n"
        text += str(self.colorList[0].B) + "\n"
        text += str(self.colorList[1].R) + "\n"
        text += str(self.colorList[1].G) + "\n"
        text += str(self.colorList[1].B) + "\n"
        text += str(self.colorList[2].R) + "\n"
        text += str(self.colorList[2].G) + "\n"
        text += str(self.colorList[2].B) + "\n"

        text += str(self.blockFallTime) + "\n"
        text += str(self.overBlockFallTime) + "\n"
        text += str(self.overBlockHoldTime) + "\n"
        text += str(self.dataPinAsInt)

        print(text)


# endregion


# region GUI

"""
Button
Aufagabe:
  Button With Correction

Func IFButtonDown | if Button Press | bool

private Func __ReadPin__ | if Button Press | bool
"""


class Button:
    def __init__(self, delay, pin):
        self.DelayMs = delay
        self.DelayAktive = False
        self.DelayEnd = 0
        self.Pin = machine.Pin(pin, machine.Pin.IN)

    def __ReadPin__(self) -> bool:
        val = self.Pin.value()
        if val == 0: return False

        return True

    def IFButtonDown(self) -> bool:
        if self.DelayAktive:
            if self.DelayEnd < Millis():
                self.DelayAktive = False

                return self.__ReadPin__()
            else:
                return False

        elif self.__ReadPin__():
            self.DelayAktive = True
            self.DelayEnd = self.DelayMs + Millis()

            return True


'''
MenuPressButton

Func UpdateButtons | Update Status of Buttons| None
Func OnButtonIsPressUpdate | Update Status of Buttons And return If One Button Press | None
Func OnButtonIsPress | return If One Button Press | bool
Func WaitOneButtonPress | wait If One Button Press | bool
'''
class MenuPressButton:
    def __init__(self, delayMs, pinLeft, pinRight, pinUp, pinDown, pinOnOff):
        self.ButtonLeft = Button(delayMs, pinLeft)
        self.ButtonRight = Button(delayMs, pinRight)
        self.ButtonUp = Button(delayMs, pinUp)
        self.ButtonDown = Button(delayMs, pinDown)
        self.ButtonOnOff = Button(delayMs, pinOnOff)
        self.Up = False
        self.Down = False
        self.Right = False
        self.Left = False
        self.OnOff = False

    def UpdateButtons(self) -> None:
        self.Left = self.ButtonLeft.IFButtonDown()
        self.Right = self.ButtonRight.IFButtonDown()
        self.Up = self.ButtonUp.IFButtonDown()
        self.Down = self.ButtonDown()
        self.OnOff = self.ButtonOnOff()

    def OnButtonIsPressUpdate(self) -> bool:
        self.UpdateButtons()
        return self.OnButtonIsPress()

    def OnButtonIsPress(self) -> bool:
        if self.Up or self.Down or self.Right or self.Left or self.OnOff():
            return True

        return False

    def WaitOneButtonPress(self) -> bool:
        while self.OnButtonIsPressUpdate() == False: pass
        return True


'''
Menu 
Aufabe:
Hier sind die Func um das UI zu erstellen oder Update zu erstellen.

Func private __SetClearList__ | Saubert das Display mit ColorOff | None
Func private __GetClearList__ | Create Liste mit ColorOff | list[Color]
Func private __GetListClearBar__ | Mit oldColorList und Saubert nur eine Bar mit ColorOff | list[Color]
Func private __SetUI_To_Option__ | Set UI to Option | None
Func private __SetUI_To_Option_UpdateUserPosi__ | Update UI as Option | None
Func private __SetUI_To_SetColor1__ | Set UI to SetColor1 | None
Func private __SetUI_To_SetColor1_UpdateUserPosi__ | Update UI as SetColor1 | None
Func private __SetUI_To_SetColor1_ChangeRGB__ | Set UI to SetColor1_ChangeRGB | None
Func private __SetUI_To_SetColor1_ChangeRGB__UpdateUserPosi__ | Update UI as SetColor1_ChangeRGB | None
Func private __SetUI_To_SetColor2__ | Set UI to SetColor1 | None
Func private __SetUI_To_SetColor2_UpdateUserPosi__ | Update UI as SetColor1 | None
Func private __SetUI_To_SetColor2_ChangeRGB__ | Set UI to SetColor1_ChangeRGB | None
Func private __SetUI_To_SetColor2_ChangeRGB__UpdateUserPosi__ | Update UI as SetColor1_ChangeRGB | None
Func private __SetUI_To_SetColorOff__ | Set UI to SetColor1 | None
Func private __SetUI_To_SetColorOff_UpdateUserPosi__ | Update UI as SetColor1 | None
Func private __SetUI_To_SetColorOff_ChangeRGB__ | Set UI to SetColor1_ChangeRGB | None
Func private __SetUI_To_SetColorOff_ChangeRGB__UpdateUserPosi__ | Update UI as SetColor1_ChangeRGB | None
'''
class Menu():
    __aktiveSelect__ = Color(255, 255, 255)
    __oldSelect__ = Color(0, 255, 0)
    __CanSelect__ = Color(0, 200, 200)
    __Bold__ = Color(255, 0, 0)

    def __SetClearList__(self, ledWriter: LED) -> None:
        ledWriter.SetNewColor(self.__GetClearList__(ledWriter))

    '''           Color 1'''

    def __GetClearList__(self, ledWriter: LED) -> list:
        returnWert = ledWriter.BarLedList

        for i_bar in range(len(returnWert)):
            for i_block in range(len(i_bar)):
                returnWert[i_bar][i_block][2].SetRGB1(0, 0, 0)

        return returnWert

    def __GetListClearBar__(self, barNum, ledWriter: LED) -> list:
        returnWert = ledWriter.BarLedList

        for i in range(len(returnWert[0])):
            returnWert[barNum][i][2] = Color(0, 0, 0)

        return returnWert

    def __SetUI_To_Option__(self, UserPosi, ledWriter: LED, colorList) -> None:
        self.__SetClearList__(ledWriter)
        newColor = ledWriter.BarLedList

        newColor[0][0][2] = self.__Bold__
        newColor[0][-1][2] = self.__Bold__

        for i in range(1, (6)):  # Size of Options
            newColor[0][i][2] = self.__CanSelect__

        newColor[0][0][UserPosi] = self.__aktiveSelect__
        ledWriter.SetNewColor(newColor)

    def __SetUI_To_Option_UpdateUserPosi__(self, UserPosi, oldUserPosi, ledWriter: LED, colorList) -> None:
        newColor = ledWriter.BarLedList

        newColor[0][oldUserPosi][2] = self.__CanSelect__
        newColor[0][UserPosi][2] = self.__aktiveSelect__

        ledWriter.SetNewColor(newColor)

    def __SetUI_To_SetColor1__(self, UserPosi, ledWriter: LED) -> None:
        newColor = ledWriter.BarLedList

        newColor[0][UserPosi][2] = self.__oldSelect__

        newColor[1][0][2] = self.__Bold__
        newColor[1][-1][2] = self.__Bold__

        newColor[1][1][2] = Color(130, 0, 0)  # R
        newColor[1][2][2] = Color(0, 130, 0)  # G
        newColor[1][3][2] = Color(0, 0, 130)  # B

        newColor[1][UserPosi][2] = self.__aktiveSelect__
        ledWriter.SetNewColor(newColor)

    def __SetUI_To_SetColor1_UpdateUserPosi__(self, UserPosi, oldUserPosi, ledWriter: LED) -> None:
        newColor = ledWriter.BarLedList

        newColor[1][1][2] = Color(130, 0, 0)  # R
        newColor[1][2][2] = Color(130, 0, 0)  # G
        newColor[1][3][2] = Color(130, 0, 0)  # B

        newColor[1][UserPosi][2] = self.__aktiveSelect__
        ledWriter.SetNewColor(newColor)

    def __SetUI_To_SetColor1_ChangeRGB__(self, UserPosi, typeRGB: MenuColorTypeEnum, ledWriter: LED) -> None:
        newColor = ledWriter.BarLedList

        newColor[2][0][2] = self.__Bold__
        newColor[2][-1][2] = self.__Bold__

        if typeRGB == MenuColorTypeEnum.R:
            newColor[2][1][2] = Color(32, 0, 0)
            newColor[2][2][2] = Color(64, 0, 0)
            newColor[2][3][2] = Color(96, 0, 0)
            newColor[2][4][2] = Color(128, 0, 0)
            newColor[2][5][2] = Color(160, 0, 0)
            newColor[2][6][2] = Color(224, 0, 0)
            newColor[2][7][2] = Color(255, 0, 0)

        elif typeRGB == MenuColorTypeEnum.G:
            newColor[2][1][2] = Color(0, 32, 0)
            newColor[2][2][2] = Color(0, 64, 0)
            newColor[2][3][2] = Color(0, 96, 0)
            newColor[2][4][2] = Color(0, 128, 0)
            newColor[2][5][2] = Color(0, 160, 0)
            newColor[2][6][2] = Color(0, 224, 0)
            newColor[2][7][2] = Color(0, 255, 0)

        elif typeRGB == MenuColorTypeEnum.B:
            newColor[2][1][2] = Color(0, 0, 32)
            newColor[2][2][2] = Color(0, 0, 64)
            newColor[2][3][2] = Color(0, 0, 96)
            newColor[2][4][2] = Color(0, 0, 128)
            newColor[2][5][2] = Color(0, 0, 160)
            newColor[2][6][2] = Color(0, 0, 224)
            newColor[2][7][2] = Color(0, 0, 255)

        newColor[1][UserPosi][2] = self.__oldSelect__
        newColor[2][UserPosi][2] = self.__aktiveSelect__
        ledWriter.SetNewColor(newColor)

    def __SetUI_To_SetColor1_ChangeRGB__UpdateUserPosi__(self, UserPosi, oldUserPosi, typeRGB: MenuColorTypeEnum, ledWriter: LED) -> None:
        newColor = ledWriter.BarLedList

        if typeRGB == MenuColorTypeEnum.R:
            newColor[2][1][2] = Color(32, 0, 0)
            newColor[2][2][2] = Color(64, 0, 0)
            newColor[2][3][2] = Color(96, 0, 0)
            newColor[2][4][2] = Color(128, 0, 0)
            newColor[2][5][2] = Color(160, 0, 0)
            newColor[2][6][2] = Color(224, 0, 0)
            newColor[2][7][2] = Color(255, 0, 0)

        elif typeRGB == MenuColorTypeEnum.G:
            newColor[2][1][2] = Color(0, 32, 0)
            newColor[2][2][2] = Color(0, 64, 0)
            newColor[2][3][2] = Color(0, 96, 0)
            newColor[2][4][2] = Color(0, 128, 0)
            newColor[2][5][2] = Color(0, 160, 0)
            newColor[2][6][2] = Color(0, 224, 0)
            newColor[2][7][2] = Color(0, 255, 0)

        elif typeRGB == MenuColorTypeEnum.B:
            newColor[2][1][2] = Color(0, 0, 32)
            newColor[2][2][2] = Color(0, 0, 64)
            newColor[2][3][2] = Color(0, 0, 96)
            newColor[2][4][2] = Color(0, 0, 128)
            newColor[2][5][2] = Color(0, 0, 160)
            newColor[2][6][2] = Color(0, 0, 224)
            newColor[2][7][2] = Color(0, 0, 255)

        newColor[2][UserPosi][2] = self.__aktiveSelect__
        ledWriter.SetNewColor(newColor)

    '''            Color 2          '''

    def __SetUI_To_SetColor2__(self, UserPosi, ledWriter: LED) -> None:
        self.__SetUI_To_SetColor1__(UserPosi, ledWriter)

    def __SetUI_To_SetColor2_UpdateUserPosi__(self, UserPosi, oldUserPosi, ledWriter: LED) -> None:
        self.__SetUI_To_SetColor1_UpdateUserPosi__(UserPosi, oldUserPosi, ledWriter)

    def __SetUI_To_SetColor2_ChangeRGB__(self, UserPosi, typeRGB: MenuColorTypeEnum, ledWriter: LED) -> None:
        self.__SetUI_To_SetColor1_ChangeRGB__(UserPosi, typeRGB, ledWriter)

    def __SetUI_To_SetColor2_ChangeRGB__UpdateUserPosi__(self, UserPosi, oldUserPosi, typeRGB: MenuColorTypeEnum, ledWriter: LED) -> None:
        self.__SetUI_To_SetColor1_ChangeRGB__UpdateUserPosi__(UserPosi, oldUserPosi, typeRGB, ledWriter)

    '''            Color On off          '''

    def __SetUI_To_SetColorOff__(self, UserPosi, ledWriter: LED) -> None:
        self.__SetUI_To_SetColor1__(UserPosi, ledWriter)

    def __SetUI_To_SetColorOff_UpdateUserPosi__(self, UserPosi, oldUserPosi, ledWriter: LED) -> None:
        self.__SetUI_To_SetColor1_UpdateUserPosi__(UserPosi, oldUserPosi, ledWriter)

    def __SetUI_To_SetColorOff_ChangeRGB__(self, UserPosi, typeRGB: MenuColorTypeEnum, ledWriter: LED) -> None:
        self.__SetUI_To_SetColor1_ChangeRGB__(UserPosi, typeRGB, ledWriter)

    def __SetUI_To_SetColorOff_ChangeRGB__UpdateUserPosi__(self, UserPosi, oldUserPosi, typeRGB: MenuColorTypeEnum, ledWriter: LED) -> None:
        self.__SetUI_To_SetColor1_ChangeRGB__UpdateUserPosi__(UserPosi, oldUserPosi, typeRGB, ledWriter)


'''
UI + vererbung von Menu
Aufabe:
  Ist das UI für den User um sachen zu endern und zu speichern
  Func + value

Update | Update Menu | None
MenuAktive | if User in Menu | bool
LoopUpdate | Loop Update and break if User not more User Menu | None
'''
class UI(Menu):
    def __init__(self, buttons: MenuPressButton, ledWriter:LED, menuParas: ProgrammParas):
        self.ledWriter: LED = ledWriter
        self.MenuParas = ProgrammParas
        self.Tasten = buttons

        self.MenuStatus = MenuPosiEnum.Off

        self.UserPosi_UP = 1
        self.UserPosi_RIGH = 0
        self.MenuSchicht = 0
        self.MenuOptions = 0

    def Update(self, ledWriter: LED) -> None:
        self.Tasten.UpdateButtons()

        if self.MenuStatus == MenuPosiEnum.Null: # MenuStatus is Null
            print("MenuStatus is Null")
            return

        if self.MenuStatus == MenuPosiEnum.Null:
            self.Tasten.UpdateButtons()
            if self.Tasten.OnButtonIsPress():
                self.MenuStatus == MenuPosiEnum.Option


        if self.MenuStatus == MenuPosiEnum.Option: self.__StatusOption__()

        elif self.MenuStatus == MenuPosiEnum.SetColor1: self.SetColor()

        elif self.MenuStatus == MenuPosiEnum.SetColor2: self.SetColor()

        elif self.MenuStatus == MenuPosiEnum.SetColorOff: self.SetColor()



    def __StatusOption__(self) -> None:
        self.__SetUI_To_Option__(ledWriter=self.ledWriter)

        self.UserPosi_RIGH = 0
        self.UserPosi_UP = 1
        maxHigh = 6
        minHigh = 1
        oldUserPosi = 1

        while True:
            oldUserPosi = self.UserPosi_UP
            self.Tasten.OnButtonIsPressUpdate()

            if self.Tasten.Left:
                self.MenuStatus = MenuPosiEnum.Null
                return

            elif self.Tasten.Up:
                if maxHigh == self.UserPosi_UP: pass
                elif minHigh == self.UserPosi_UP: pass
                else:
                    self.UserPosi_UP += 1

            elif self.Tasten.Down:
                if maxHigh == self.UserPosi_UP: pass
                elif minHigh == self.UserPosi_UP: pass
                else:
                    self.UserPosi_UP += -1


            self.Tasten.OnButtonIsPressUpdate(self, self.UserPosi_UP, oldUserPosi, self.ledWriter,
                                              self.MenuParas.colorList)


            if self.Tasten.Right:
                if self.UserPosi_UP == 1: self.MenuStatus = MenuPosiEnum.SetColor1

                elif self.UserPosi_UP == 2: self.MenuStatus = MenuPosiEnum.SetColor2

                elif self.UserPosi_UP == 3: self.MenuStatus = MenuPosiEnum.SetColorOff

                elif self.UserPosi_UP == 4: self.MenuStatus = MenuPosiEnum.SetBlockTimeDown

                elif self.UserPosi_UP == 5: self.MenuStatus = MenuPosiEnum.SetOverBlockTimeDown

                elif self.UserPosi_UP == 6: self.MenuStatus = MenuPosiEnum.SetOverBlockHoldTime

                return





    # kommt noch


    def __SetColorR_orG_orB__(self, ColorType: MenuColorTypeEnum, listPosi: int):
        pass

    def SetColorR_orG_orB(self, ColorType: MenuColorTypeEnum, oldColor: Color) -> (MenuSaveEnum, int):
        listPosi = 0
        colorDessList = []  # Liste | UserPosi
        colorDessList.append(32)  # 0 > 1
        colorDessList.append(64)  # 1 > 2
        colorDessList.append(96)  # 2 > 3
        colorDessList.append(128)  # 3 > 4
        colorDessList.append(160)  # 4 > 5
        colorDessList.append(192)  # 5 > 6
        colorDessList.append(224)  # 6 > 7
        colorDessList.append(255)  # 7 > 8

        if ColorType == MenuColorTypeEnum.R: pass
        if ColorType == MenuColorTypeEnum.G: pass

        if ColorType == MenuColorTypeEnum.B:  # Ser Color for B
            # Set UserPosi to Aktive Color
            for num in range(len(colorDessList)):
                if oldColor.R <= colorDessList[num]:
                    listPosi = num
                    self.UserPosiUp = num + 1
                    break

            # Set UI to ColorType
            if True: self.__SetColorR_orG_orB__(ColorType, listPosi)

            while True:
                buttons = self.GetUsetInput()

                if buttons.OnOff:
                    self.IfPressOnOffButton()
                elif buttons.Left:
                    return (MenuSaveEnum.NotSave, colorDessList[0])

                elif buttons.Right:
                    return (MenuSaveEnum.Save, colorDessList[listPosi])

                elif buttons.Up:
                    if self.UserPosiUp == 8:
                        self.UserPosiUp = 1
                        listPosi = 0

                    else:
                        self.UserPosiUp += 1
                        listPosi += 1

                elif buttons.Down:
                    if self.UserPosiUp == 1:
                        self.UserPosiUp += -1
                        listPosi += -1

                # Update UI
                if True: self.__SetColorR_orG_orB__(ColorType, listPosi)

        elif ColorType == MenuColorTypeEnum.G:
            if True:  # Set UserPosi AND Set colorListPosi
                for num in range(len(colorDessList)):
                    if oldColor.G <= colorDessList[num]:
                        listPosi = num
                        self.UserPosiUp = num + 1
                        break

            # Set UI to ColorType
            if True: self.__SetColorR_orG_orB__(ColorType, listPosi)

            while True:
                buttons = self.GetUsetInput()

                if buttons.OnOff:
                    self.IfPressOnOffButton()
                elif buttons.Left:
                    return (MenuSaveEnum.NotSave, colorDessList[0])

                elif buttons.Right:
                    return (MenuSaveEnum.Save, colorDessList[listPosi])

                elif buttons.Up:
                    if self.UserPosiUp == 8:
                        self.UserPosiUp = 1
                        listPosi = 0

                    else:
                        self.UserPosiUp += 1
                        listPosi += 1

                elif buttons.Down:
                    if self.UserPosiUp == 1:
                        self.UserPosiUp += -1
                        listPosi += -1

                # Update UI
                if True: self.__SetColorR_orG_orB__(ColorType, listPosi)

        elif ColorType == MenuColorTypeEnum.B:
            if True:  # Set UserPosi AND Set colorListPosi
                for num in range(len(colorDessList)):
                    if oldColor.B <= colorDessList[num]:
                        listPosi = num
                        self.UserPosiUp = num + 1
                        break

            # Set UI to ColorType
            if True: self.__SetColorR_orG_orB__(ColorType, listPosi)

            while True:
                buttons = self.GetUsetInput()

                if buttons.OnOff:
                    self.IfPressOnOffButton()
                elif buttons.Left:
                    return (MenuSaveEnum.NotSave, colorDessList[0])

                elif buttons.Right:
                    return (MenuSaveEnum.Save, colorDessList[listPosi])

                elif buttons.Up:
                    if self.UserPosiUp == 8:
                        self.UserPosiUp = 1
                        listPosi = 0

                    else:
                        self.UserPosiUp += 1
                        listPosi += 1

                elif buttons.Down:
                    if self.UserPosiUp == 1:
                        self.UserPosiUp += -1
                        listPosi += -1

                # Update UI
                if True: self.__SetColorR_orG_orB__(ColorType, listPosi)

    def SetColor(self) -> None:
        returnUserPosiIFLeft = self.UserPosi_UP

        self.UserPosiUp = 1

        while True:
            self.Tasten.OnButtonIsPressUpdate()

            # MenuStatus => off
            if self.Tasten.OnOff:
                self.MenuStatus = MenuPosiEnum.Off
                return

            # not Save
            elif self.Tasten.Left:
                self.MenuStatus = MenuPosiEnum.Option
                return



            # Save
            # Change color R
            # Change color G
            # Change color B
            elif buttons.Right:
                if self.UserPosiUp == 4:  # Save
                    returnWertSave = MenuSaveEnum.Save
                    return

                elif self.UserPosiUp == 3:  # Set R
                    buff = self.SetColorR_orG_orB(MenuColorTypeEnum.R)
                    if buff[0] == MenuSaveEnum.Save:
                        newColor.R = buff[1]
                    else:
                        pass

                elif self.UserPosiUp == 2:  # Set G
                    buff = self.SetColorR_orG_orB(MenuColorTypeEnum.G)
                    if buff[0] == MenuSaveEnum.Save:
                        newColor.G = buff[1]
                    else:
                        pass

                elif self.UserPosiUp == 1:  # Set B
                    buff = self.SetColorR_orG_orB(MenuColorTypeEnum.B)
                    if buff[0] == MenuSaveEnum.Save:
                        newColor.B = buff[1]
                    else:
                        pass

            # Go Up
            elif buttons.Up:
                if self.UserPosiUp == 4:
                    pass  # Is Max Up
                else:
                    self.UserPosiUp += 1

            # Go Down
            elif buttons.Down:
                if self.UserPosiUp == 1:
                    pass  # Is Max Down
                else:
                    self.UserPosiUp += -1

    def LoopUpdate(self, ledWriter: LED) -> None:
        pass


# endregion


# region main


'''
Class InputAudio
Aufgabe:
Read ADC Pin and write to a List

Func Update | Update die HightList für die HzBender | None
Func UpdateReturn  | Update die HightList für die HzBender | list[int]
PrintAudioHigh | Printet die Liste AudioHightList | None
GetHighList | Return HighList | list[int]
'''
class InputAudio():
    def __init__(self, high, size, hzADCPinMachine):
        self.high = high
        self.hzADCPinList = hzADCPinMachine

        self.HighList = []

        for i in range(size): self.HighList.append(0)

    def Update(self) -> None:
        for i in range(len(self.hzADCPinList)):
            self.HighList[i] = int(self.high / 4000 * self.hzADCPinList[i].read())

    def UpdateReturn(self) -> list:
        self.Update()

        return self.HighList

    def PrintAudioHigh(self):
        for i in range(len(self.HighList)):
            print(i, "=>", self.HighList[i].read())

    def GetHighList(self) -> list:
        return self.HighList


'''
Block
Aufgabe:
Save 3 Colors for 1 LED Grup

Func SetAktive | Set Block to Aktive | None
Func SetOff | Set Block to Off | None
Func ChanceColor | Chance Color Mode | None
'''
class Block():
    def __init__(self, color1, color2, colorOff):
        self.Color1 = color1 # Color 1 is the main Color 
        self.Color2 = color2 # Color 2 ist der Block der langsam fehlt
        self.ColorOff = colorOff # ColorOff ist sind die Blocke die aus sind

        self.AktiveColor = colorOff # Welche Frabe grade Aktive ist
        self.Status = False # Ob der Block Aktive ist oder nicht

    def SetAktive(self) -> None: self.Status = True

    def SetOff(self) -> None: self.Status = False

    def ChanceColor(self, colorInt) -> None:
        if colorInt == 1: self.AktiveColor = self.Color1

        elif colorInt == 2: self.AktiveColor = self.Color2

        elif colorInt == 3: self.AktiveColor = self.ColorOff


'''
Bar
Aufgabe:
Save Block and Chance the Color

Func FirstStart | Set Blocks Aktive and Chance the Color to Off | None
Func Update | Chance Colors Mode from Blocks | None
'''
class Bar():
    def __init__(self, high, colorList, blockFallTime, overBlockFallTime, overBlockHoldTime):
        self.BlockList = []

        for i in range(high):
            self.BlockList.append(Block(colorList[0], colorList[1], colorList[2]))

        self.BlockFallTime = blockFallTime
        self.OverBlockFallTime = overBlockFallTime
        self.OverBlockHoldTime = overBlockHoldTime

        self.BlockNextDown_Ms = 0
        self.OverBlockNextDown_Ms = 0

        self.OverBlockHoldAktive = False
        self.OverBlockHoldEnd_Ms = 0

        self.MaxHigh = high + 1
        self.PosiBlock = 0
        self.PosiOverBlock = 1

    def FirstStart(self) -> None:
        for i in self.BlockList: # Geht alle Block durch 
            i.SetAktive()        # Set all Block to Aktive
            i.ChanceColor(3)     # Chance the Color to ColorOff

    def Update(self, audioHigh) -> None:
        # ------------------------------------------------ Block
        # If audioHigh Higher then self.PosiBlock
        if self.PosiBlock <= audioHigh: # Wenn die audioHigh Higher ist als self.PosiBlock
            self.BlockNextDown_Ms = Millis() + self.BlockFallTime # Set new time self.BlockNextDown_Ms

            if self.MaxHigh <= audioHigh: # If audio to High as self.MaxHigh 
                self.PosiBlock = self.MaxHigh - 1

            else: self.PosiBlock = audioHigh

        # If self.BlockNextDown_Ms lower as Millis()
        # Then self.PosiBlock foll
        elif self.BlockNextDown_Ms < Millis(): 
            self.BlockNextDown_Ms = Millis() + self.BlockFallTime

            if self.PosiBlock <= 1:
                self.PosiBlock = 0

            else:
                self.PosiBlock += -1

        # ------------------------------------------------ OverBlock
        # If self.Posi higher then self.PosiOverBlock
        # Then Set self.PosiOverBlock Higher
        if self.PosiBlock + 1 >= self.PosiOverBlock:
            self.PosiOverBlock = self.PosiBlock + 1

            if self.PosiOverBlock != 1:
                self.OverBlockHoldAktive = True
                self.OverBlockHoldEnd_Ms = Millis() + self.OverBlockHoldTime
        
        # If self.OverBlockHoldAktive Aktive
        # Then If 
        elif self.OverBlockHoldAktive:
            if self.OverBlockHoldEnd_Ms < Millis():
                self.OverBlockHoldAktive = False
                self.OverBlockNextDown_Ms = Millis() + self.OverBlockFallTime

                if self.PosiOverBlock <= 2:
                    self.PosiOverBlock = 1

                else:
                    self.PosiOverBlock += -1

        elif self.OverBlockNextDown_Ms < Millis():
            self.OverBlockNextDown_Ms = Millis() + self.OverBlockFallTime

            if self.PosiOverBlock <= 2:
                self.PosiOverBlock = 1

            else:
                self.PosiOverBlock += -1

        return


'''
EQ
Aufgabe:
Die Zusammenfassung der Classen in einer und Update alle Classen

Func FirstStart | Set all Class To FirstStart | None
Func Update | Update all Class | None
Func PrintEQ | Print all Bars | None
Func LoopUpdate | Loop Update Func | None
'''
class EQ():
    def __init__(self, machineADCPinList, dataPinAsInt, buttons: MenuPressButton):
        self.LedWriter = LED(self.MainParas.size, self.MainParas.high, dataPinAsInt)
        self.MainParas = ProgrammParas()

        self.Ui = UI(buttons, self.LedWriter, self.MainParas)  # UI

        self.BarList = []
        self.Audio = InputAudio(self.MainParas.high + 1, self.MainParas.size, machineADCPinList)
        self.High = self.MainParas.high


        for i in range(self.MainParas.size):
            self.BarList.append(Bar(self.MainParas.high, self.MainParas.colorList,
                                    self.MainParas.blockFallTime, self.MainParas.overBlockFallTime,
                                    self.MainParas.overBlockHoldTime))

    def FirstStart(self) -> None:
        for i in range(len(self.BarList)):
            self.BarList[i].FirstStart()

    def Update(self) -> None:
        self.Audio.Update()

        for i in range(len(self.BarList)):
            self.BarList[i].Update(self.Audio.HighList[i])

    def PrintEQ(self) -> None:
        text = ""

        for bar in self.BarList:
            for textPosiHigh in range(self.High):
                if 0 == textPosiHigh:
                    text += "#"
                elif bar.PosiBlock > textPosiHigh:
                    text += "#"
                elif bar.PosiOverBlock == textPosiHigh:
                    text += "|"
                else:
                    text += " "

            text += "\n"
        print(text)

    def LoopUpdate(self) -> None:
        while True:
            try:
                self.Update()
                gc.collect()
            except:
                pass


# ------------------------------------------------------ ClassS End


# Enable automatic garbage collection.
gc.enable()

# Pins for IN Hz AS Int
hzID = [32,
        33,
        34,
        35,
        36,
        37,
        38,
        39
        ]

# Pins for IN Hz AS machine.ADC
__hzADCPin__ = []

for i in hzID: __hzADCPin__.append(machine.ADC(machine.Pin(i)))

# Pin DATA_LED OUT
dataPinAsInt = 22

# Buttons
buttons = MenuPressButton(delayMs=300,
                          pinLeft=1,
                          pinRight=2,
                          pinUp=3,
                          pinDown=3,
                          pinOnOff=4)
eq = EQ(machineADCPinList=__hzADCPin__, dataPinAsInt=dataPinAsInt, buttons=buttons)

eq.FirstStart()
eq.PrintEQ()

# Run a garbage collection.
gc.collect()

eq.Update()
print("---")

eq.BarList[1].PosiOverBlock = 0
eq.BarList[1].PosiBlock = 7

# ---------------------------

# endregion
