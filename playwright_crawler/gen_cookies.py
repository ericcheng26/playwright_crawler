from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()

    # Open new page
    page = context.new_page()

    # Go to https://yamol.tw/main.php
    page.goto("https://yamol.tw/main.php")

    # Click text=登入
    page.click("text=登入")
    # assert page.url == "https://yamol.tw/mylogin.php"

    # Click [placeholder="請輸入Email"]
    page.click("[placeholder=\"請輸入Email\"]")

    # Fill [placeholder="請輸入Email"]
    page.fill("[placeholder=\"請輸入Email\"]", "ericcheng26@gmail.com")

    # Press Tab
    page.press("[placeholder=\"請輸入Email\"]", "Tab")

    # Fill [placeholder="請輸入密碼"]
    page.fill("[placeholder=\"請輸入密碼\"]", "hacker26")

    # Press Enter
    # with page.expect_navigation(url="https://yamol.tw/user.php?id=100006037091347"):
    with page.expect_navigation():
        page.press("[placeholder=\"請輸入密碼\"]", "Enter")
    # assert page.url == "https://yamol.tw/mylogin.php"

    # Close page
    page.close()

    # Open new page
    page = context.new_page()

    # Go to https://yamol.tw/
    page.goto("https://yamol.tw/")

    # Go to https://www.facebook.com/
    page.goto("https://www.facebook.com/")

    # Go to https://tpc.googlesyndication.com/
    page.goto("https://tpc.googlesyndication.com/")

    # Go to https://accounts.google.com/
    page.goto("https://accounts.google.com/")

    # Close page
    page.close()

    # ---------------------
    context.storage_state(path="cookies")
    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)