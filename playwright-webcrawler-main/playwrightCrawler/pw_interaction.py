class Interaction:
    def __init__(self,):

    def yamol(self):
        list_lv0element_handle = page.query_selector_all(
            "text=\"私人筆記( (?!0))\"")
        while True:
            try:
                for lv0element_handle in list_lv0element_handle:
                    lv0element_handle.click()
            except:
                break
        list_lv1element_handle = page.query_selector_all(
            "text=\"詳解卡解鎖\"")
        while True:
            try:
                for lv1element_handle in list_lv1element_handle:
                    lv1element_handle.click()
            except:
                break
