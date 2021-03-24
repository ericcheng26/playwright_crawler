class Interaction:
    def __init__(self,):

    def yamol(self):
        list_lv0element_handle = page.query_selector_all(
            "text=\"私人筆記( ^[1-9]\d*$ )\"")
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
        list_lv2element_handle = page.query_selector_all(
            "text=\"查看完整內容\"")
        while True:
            try:
                for lv2element_handle in list_lv2element_handle:
                    lv2element_handle.click()
            except:
                break
        list_lv3element_handle = page.query_selector_all(
            "text=\"查看全部^[1-9]\d*$則討論\"")
        while True:
            try:
                for lv3element_handle in list_lv3element_handle:
                    lv3element_handle.click()
            except:
                break
