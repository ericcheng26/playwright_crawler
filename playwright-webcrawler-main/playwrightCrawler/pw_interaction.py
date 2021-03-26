class Interaction:
    def __init__(self,):

    def yamol(self):
        list_lv1element_handle = page.query_selector_all(
            "text=\"詳解卡解鎖\"")
        while True:
            try:
                for lv1element_handle in list_lv1element_handle:
                    lv1element_handle.click()
            except:
                break
