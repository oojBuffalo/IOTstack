#!/usr/bin/env python3
import signal

def main():
  from blessed import Terminal
  from deps.chars import specialChars, commonTopBorder, commonBottomBorder, commonEmptyLine
  import math
  import time
  import subprocess

  global dockerCommandsSelectionInProgress
  global renderMode
  global signal
  global mainMenuList
  global currentMenuItemIndex
  term = Terminal()
  hotzoneLocation = [7, 0] # Top text
  
  def onResize(sig, action):
    global mainMenuList
    global currentMenuItemIndex
    mainRender(1, mainMenuList, currentMenuItemIndex)

  def startStack():
    print("Start Stack:")
    print("docker-compose up -d")
    subprocess.call("docker-compose up -d", shell=True)
    print("")
    print("Stack Started")
    time.sleep(2)
    return True
  
  def restartStack():
    print("Restart Stack:")
    print("docker-compose restart")
    subprocess.call("docker-compose restart", shell=True)
    print("")
    print("Stack Restarted")
    time.sleep(2)
    return True

  def stopStack():
    print("Stop Stack:")
    print("docker-compose down")
    subprocess.call("docker-compose down", shell=True)
    print("")
    print("Stack Stopped")
    time.sleep(2)
    return True

  def stopAllStack():
    print("Stop All Stack:")
    print("docker container stop $(docker container ls -aq)")
    subprocess.call("docker container stop $(docker container ls -aq)", shell=True)
    print("")
    print("Stack Stopped. Press [Up] or [Down] arrow key to show the menu if it has scrolled too far.")
    time.sleep(2)
    return True

  def pruneVolumes():
    print("Stop All Stack:")
    print("docker container stop $(docker container ls -aq)")
    subprocess.call("docker container stop $(docker container ls -aq)", shell=True)
    print("")
    print("Stack Stopped. Press [Up] or [Down] arrow key to show the menu if it has scrolled too far.")
    time.sleep(2)
    return True

  def updateAllContainers():
    print("Update All Containers:")
    print("docker-compose down")
    subprocess.call("docker-compose down", shell=True)
    print("")
    print("docker-compose pull")
    subprocess.call("docker-compose pull", shell=True)
    print("")
    print("docker-compose build")
    subprocess.call("docker-compose build", shell=True)
    print("")
    print("docker-compose up -d")
    subprocess.call("docker-compose up -d", shell=True)
    print("")
    print("Stack Updated. Press [Up] or [Down] arrow key to show the menu if it has scrolled too far.")
    time.sleep(0.5)
    return True

  def deleteAndPruneVolumes():
    print("Delete and prune volumes:")
    print("docker system prune --volumes")
    subprocess.call("docker system prune --volumes", shell=True)
    print("")
    print("Volume pruning completed. Press [Up] or [Down] arrow key to show the menu if it has scrolled too far.")
    time.sleep(0.5)
    return True

  def deleteAndPruneImages():
    print("Delete and prune volumes:")
    print("docker image prune -a")
    subprocess.call("docker image prune -a", shell=True)
    print("")
    print("Image pruning completed. Press [Up] or [Down] arrow key to show the menu if it has scrolled too far.")
    time.sleep(0.5)
    return True

  def goBack():
    global dockerCommandsSelectionInProgress
    global needsRender
    dockerCommandsSelectionInProgress = False
    needsRender = 1
    print("Back to main menu")
    return True

  mainMenuList = [
    ["Start stack", startStack],
    ["Restart stack", restartStack],
    ["Stop stack", stopStack],
    ["Stop ALL running docker containers", stopAllStack],
    ["Update all containers (may take a long time)", updateAllContainers],
    ["Delete all stopped containers and docker volumes (prune volumes)", deleteAndPruneVolumes],
    ["Delete all images not associated with container", deleteAndPruneImages],
    ["Back", goBack]
  ]

  dockerCommandsSelectionInProgress = True
  currentMenuItemIndex = 0
  menuNavigateDirection = 0

  # Render Modes:
  #  0 = No render needed
  #  1 = Full render
  #  2 = Hotzone only
  needsRender = 1

  def renderHotZone(term, menu, selection, hotzoneLocation):
    print(term.move(hotzoneLocation[0], hotzoneLocation[1]))
    lineLengthAtTextStart = 75

    for (index, menuItem) in enumerate(menu):
      toPrint = ""
      if index == selection:
        toPrint += ('{bv}   {t.blue_on_green} {title} {t.normal}'.format(t=term, title=menuItem[0], bv=specialChars[renderMode]["borderVertical"]))
      else:
        toPrint += ('{bv}   {t.normal} {title} '.format(t=term, title=menuItem[0], bv=specialChars[renderMode]["borderVertical"]))

      for i in range(lineLengthAtTextStart - len(menuItem[0])):
        toPrint += " "

      toPrint += "{bv}".format(bv=specialChars[renderMode]["borderVertical"])

      toPrint = term.center(toPrint)
      
      print(toPrint)


  def mainRender(needsRender, menu, selection):
    term = Terminal()

    if needsRender == 1:
      print(term.clear())

      print(term.clear())
      print(term.move_y(6 - hotzoneLocation[0]))
      print(term.black_on_cornsilk4(term.center('IOTstack Docker Commands')))
      print("")
      print(term.center(commonTopBorder(renderMode)))
      print(term.center(commonEmptyLine(renderMode)))
      print(term.center("{bv}      Select Docker Command to run                                              {bv}".format(bv=specialChars[renderMode]["borderVertical"])))
      print(term.center(commonEmptyLine(renderMode)))
      print(term.center(commonEmptyLine(renderMode)))
      print(term.center(commonEmptyLine(renderMode)))

    if needsRender >= 1:
      renderHotZone(term, menu, selection, hotzoneLocation)

    if needsRender == 1:
      print(term.center(commonEmptyLine(renderMode)))
      print(term.center(commonEmptyLine(renderMode)))
      print(term.center("{bv}      Controls:                                                                 {bv}".format(bv=specialChars[renderMode]["borderVertical"])))
      print(term.center("{bv}      [Up] and [Down] to move selection cursor                                  {bv}".format(bv=specialChars[renderMode]["borderVertical"])))
      print(term.center("{bv}      [Enter] to run command                                                    {bv}".format(bv=specialChars[renderMode]["borderVertical"])))
      print(term.center("{bv}      [Escape] to go back to main menu                                          {bv}".format(bv=specialChars[renderMode]["borderVertical"])))
      print(term.center(commonEmptyLine(renderMode)))
      print(term.center(commonEmptyLine(renderMode)))
      print(term.center(commonBottomBorder(renderMode)))




  def runSelection(selection):
    import types
    if len(mainMenuList[selection]) > 1 and isinstance(mainMenuList[selection][1], types.FunctionType):
      mainMenuList[selection][1]()
    else:
      print(term.green_reverse('IOTstack Error: No function assigned to menu item: "{}"'.format(mainMenuList[selection][0])))

  def isMenuItemSelectable(menu, index):
    if len(menu) > index:
      if len(menu[index]) > 2:
        if menu[index][2]["skip"] == True:
          return False
    return True

  if __name__ == 'builtins':
    term = Terminal()
    signal.signal(signal.SIGWINCH, onResize)
    with term.fullscreen():
      menuNavigateDirection = 0
      mainRender(needsRender, mainMenuList, currentMenuItemIndex)
      dockerCommandsSelectionInProgress = True
      with term.cbreak():
        while dockerCommandsSelectionInProgress:
          menuNavigateDirection = 0

          if not needsRender == 0: # Only rerender when changed to prevent flickering
            mainRender(needsRender, mainMenuList, currentMenuItemIndex)
            needsRender = 0

          key = term.inkey()
          if key.is_sequence:
            if key.name == 'KEY_TAB':
              menuNavigateDirection += 1
            if key.name == 'KEY_DOWN':
              menuNavigateDirection += 1
            if key.name == 'KEY_UP':
              menuNavigateDirection -= 1
            if key.name == 'KEY_ENTER':
              runSelection(currentMenuItemIndex)
              if dockerCommandsSelectionInProgress == False:
                return True
            if key.name == 'KEY_ESCAPE':
              dockerCommandsSelectionInProgress = False
              return True
          elif key:
            print("got {0}.".format(key))

          if menuNavigateDirection != 0: # If a direction was pressed, find next selectable item
            currentMenuItemIndex += menuNavigateDirection
            currentMenuItemIndex = currentMenuItemIndex % len(mainMenuList)
            needsRender = 2

            while not isMenuItemSelectable(mainMenuList, currentMenuItemIndex):
              currentMenuItemIndex += menuNavigateDirection
              currentMenuItemIndex = currentMenuItemIndex % len(mainMenuList)
    return True

  return True

originalSignalHandler = signal.getsignal(signal.SIGINT)
main()
signal.signal(signal.SIGWINCH, originalSignalHandler)