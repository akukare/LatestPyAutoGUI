

import os
import pygetwindow as gw
import pyautogui, subprocess, time, os
print(os.path.exists(r"C:\pyautogui\assets\images\file_menu.png"))
print(os.path.exists(r"C:\pyautogui\assets\images\manage_session.png"))
print(os.path.exists(r"C:\pyautogui\assets\images\server_management.png"))




CREO_PATH = r"C:\Program Files\PTC\Creo 12.4.0.0\Parametric\bin\parametric.exe"


# def bring_creo_to_front():
#     """Brings the Creo Parametric window to the front."""
#     try:
#         for win in gw.getWindowsWithTitle("Creo"):
#             if win.isMinimized:
#                 win.restore()
#             win.activate()
#             print(" Creo window activated.")
#             return True
#         print(" Creo window not found.")
#         return False
#     except Exception as e:
#         print(f" Could not activate Creo window: {e}")
#         return False

def open_creo():
    if not os.path.exists(CREO_PATH):
        print(f" Creo not found at {CREO_PATH}")
        return False
    print(" Launching Creo...")
    subprocess.Popen(CREO_PATH, shell=True)
    time.sleep(15)
   
    # bring_creo_to_front()
    # pyautogui.hotkey('alt', 'tab')
    print("Creo launched successfully.")
    return True

def click_file_and_manage_session():
    pyautogui.FAILSAFE = True
    print("Searching for File menu icon...")
    pyautogui.hotkey('alt')

    try:
        file_btn = pyautogui.locateOnScreen(
            r"C:\pyautogui\assets\images\server_tab.png", confidence=0.7)
    except pyautogui.ImageNotFoundException:
        file_btn = None

    if file_btn:
        pyautogui.click(pyautogui.center(file_btn))
        print("File menu clicked.")
        time.sleep(2)
    else:
        print(" File menu not found, pressing Alt+F as fallback.")
        pyautogui.hotkey('alt', 'f')
        time.sleep(2)
  

    print("🔍 Searching for Manage Session option...")
    try:
        manage_btn = pyautogui.locateOnScreen(
        r"C:\pyautogui\assets\images\server_tab.png", confidence=0.7)
    except pyautogui.ImageNotFoundException:
        manage_btn = None

    if manage_btn:
        pyautogui.click(pyautogui.center(manage_btn))
        print(" Manage Session clicked.")
    else:
        print(" Manage Session not detected; check screenshot or UI state.")
        pyautogui.hotkey('alt', 'm')
        time.sleep(2)

    try:
        server_btn = pyautogui.locateOnScreen(
        r"C:\pyautogui\assets\images\server_management.png", confidence=0.7)
    except pyautogui.ImageNotFoundException:
        server_btn = None

    if server_btn:
        pyautogui.click(pyautogui.center(server_btn))
        print("server clicked")
        time.sleep(4)
    else:
        print("pressing Alt+s as fallback.")
        pyautogui.hotkey('alt', 's')
        time.sleep(2)

    """server connection"""
    try:
        server_tab = pyautogui.locateOnScreen(
        r"C:\pyautogui\assets\images\title_sev.png", confidence=0.7)
    except pyautogui.ImageNotFoundException:
        server_btn = None

    if server_tab:
        pyautogui.click(pyautogui.center(server_tab))
        print("server clicked")
        time.sleep(2)
    else:
        time.sleep(2)

    try:
        registry_tab = pyautogui.locateOnScreen(
        r"C:\pyautogui\assets\images\register_new_server.png", confidence=0.7)
    except pyautogui.ImageNotFoundException:
        registry_tab = None

    if registry_tab:
        pyautogui.click(pyautogui.center(registry_tab))
        print("registry new server was clicked")
        time.sleep(4)
    else:
        time.sleep(2)


def register_new_server(name="windchill", location="https://plmtvdr3.plmtestlab.com/Windchill"):
    """
    Handles the 'Register New Server' popup:
    - Waits for the popup to appear
    - Enters Name and Location
    - Clicks OK
    """
    print("📝 Registering new server...")

    # Wait until popup appears
    popup_found = pyautogui.locateOnScreen(
        r"C:\pyautogui\assets\images\register_new_popup.png", confidence=0.8
    )

    if not popup_found:
        print("⚠️ Register popup not found. Please verify the image or delay.")
        pyautogui.screenshot("debug_popup.png")
        return False

    # Move to 'Name' textbox and type
    print("Typing server name...")
    pyautogui.click(pyautogui.center(popup_found))
    # pyautogui.press('tab')  
    pyautogui.typewrite(name, interval=0.05)

    # Move to 'Location' textbox and type
    print("Typing server location...")
    pyautogui.press('tab')
    pyautogui.typewrite(location, interval=0.05)
    time.sleep(4)

    check_btn = pyautogui.locateOnScreen(
        r"C:\pyautogui\assets\images\check.png", confidence=0.8
    )
    if check_btn:
        pyautogui.click(pyautogui.center(check_btn))
        print("checking.")
    else:
        print("Check not Found.")
        time.sleep(2)


    """enter creditionals"""
    time.sleep(5)
    pyautogui.typewrite("demouser")
    pyautogui.press('tab')
    pyautogui.typewrite("demouser")
    time.sleep(2)

    ok_btn = pyautogui.locateOnScreen(
        r"C:\pyautogui\assets\images\ok_button.png", confidence=0.7
    )
    if ok_btn:
        pyautogui.click(pyautogui.center(ok_btn))
        print("✅ Server registered successfully.")
    else:
        print("⚠️ OK button not found; please check the image or confidence level.")
    time.sleep(5)

    confirm_btn = pyautogui.locateOnScreen(
        r"C:\pyautogui\assets\images\confirm_ok.png", confidence=0.7
    )
    if confirm_btn:
        pyautogui.click(pyautogui.center(confirm_btn))
        print("server ok button clicked")
    else:
        print("no clicked confirm button")
        time.sleep(3)


    return True
    

def setting_workspace():
    """checking and setting windchill connected with workspace"""


    select_windchill = pyautogui.locateOnScreen(
        r"C:\pyautogui\assets\images\set_online.png", confidence=0.7
    )
    if select_windchill:
        pyautogui.click(pyautogui.center(select_windchill))
        print("windchill select")
        time.sleep(2)
    else:
        print("no succuess")


    test_btn = pyautogui.locateOnScreen(
        r"C:\pyautogui\assets\images\set_online.png", confidence=0.7
    )
    if test_btn:
        pyautogui.doubleClick(pyautogui.center(test_btn))
        print("testwork profile clicked")
        time.sleep(2)
    else:
        print("no succuess")

    data_verfiy = pyautogui.locateOnScreen(
        r"C:\pyautogui\assets\images\data_ve.png", confidence= 0.7
    )
    if data_verfiy:
        pyautogui.moveTo(pyautogui.center(data_verfiy))
        print("workspace set ")
        time.sleep(2)
    else:
        print("no succuess")

    work_space = pyautogui.locateOnScreen(
        r"C:\pyautogui\assets\images\workspace.png", confidence= 0.7
    )
    if work_space:
        pyautogui.doubleClick(pyautogui.center(work_space))
        print("workspace set ")
        time.sleep(5)
    else:
        print("no succuess")

    
def creating_part():
    """creating the part in workspace of windchill"""

    create_new = pyautogui.locateOnScreen(
        r"C:\pyautogui\assets\images\new.png", confidence=0.7
    )
    if create_new:
        pyautogui.click(pyautogui.center(create_new))
        time.sleep(5)
    else:
        print("it was not clicked on part")

    # select_part = pyautogui.locateOnScreen(
    #     r"C:\pyautogui\assets\images\part_select.png", confidence=0.7
    # )
    # if select_part:
    #     pyautogui.click(pyautogui.center(select_part))
    #     time.sleep(3)
    #     pyautogui.typewrite("new_part12")
    #     time.sleep(3)
    # else:
    #     print("it was not selected on part")

    pyautogui.typewrite("new_part12")
    
    click_ok = pyautogui.locateOnScreen(
        r"C:\pyautogui\assets\images\confirm_ok.png", confidence=0.7
    )
    if click_ok:
        pyautogui.click(pyautogui.center(click_ok))
        time.sleep(5)
    else:
        print("it was not selected on part")

    save_btn = pyautogui.locateOnScreen(
        r"C:\pyautogui\assets\images\save_button.png", confidence=0.7
    )
    if save_btn:
        pyautogui.doubleClick(pyautogui.center(save_btn))
        time.sleep(5)
    else:
        print("it was not selected on part")

    time.sleep(1)
    
    close_btn = pyautogui.locateOnScreen(
        r"C:\pyautogui\assets\images\close_button.png", confidence=0.7
    )
    if close_btn:
        pyautogui.click(pyautogui.center(close_btn))
        time.sleep(5)
    else:
        print("it was not selected on part")
    pyautogui.hotkey('ctrl', 's')
        
    time.sleep(5)
    

    
    


    # close_part = pyautogui.locateOnScreen(
    #     r"C:\pyautogui\assets\images\close.png", confidence=0.7
    # )
    # if close_part:
    #     pyautogui.click(pyautogui(close_part))
    #     time.sleep(3)
    # else:
    #     print(" part closed")
    
    work_space = pyautogui.locateOnScreen(
        r"C:\pyautogui\assets\images\workspace.png", confidence= 0.7
    )
    if work_space:
        pyautogui.doubleClick(pyautogui.center(work_space))
        print("workspace set ")
        time.sleep(5)
    else:
        print("no succuess")

    select_box = pyautogui.locateOnScreen(
        r"C:\pyautogui\assets\images\select_box.png", confidence= 0.7
    )

    if select_box:
        pyautogui.click(pyautogui.center(select_box))
        time.sleep(2)
    else:
        print("not deleted")

    delete_part = pyautogui.locateOnScreen(
        r"C:\pyautogui\assets\images\delete.png", confidence= 0.7
    )
    if delete_part:
        pyautogui.doubleClick(pyautogui.center(delete_part))
        print("workspace set ")
        time.sleep(5)
    else:
        print("no succuess")

    select_ok = pyautogui.locateOnScreen(
        r"C:\pyautogui\assets\images\select_ok.png", confidence= 0.7
    )
    if select_ok:
        pyautogui.click(pyautogui.center(select_ok))
    else:
        delete_part

    select_yes = pyautogui.locateOnScreen(
        r"C:\pyautogui\assets\images\select_ok.png", confidence= 0.7
    )
    if select_yes:
        pyautogui.click(pyautogui.center(select_yes))
    else:
        select_ok
    

    

if __name__ == "__main__":
    if         open_creo():
        click_file_and_manage_session()
        register_new_server()
        setting_workspace()
        creating_part()


