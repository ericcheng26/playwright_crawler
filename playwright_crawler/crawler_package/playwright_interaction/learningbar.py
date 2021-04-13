from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(storage_state="/home/eric/文件/github/cookies_pack/learningbar_cookies")

    # Open new page
    page = context.new_page()

    # Go to https://www.learningbar.tw/
    page.goto("https://www.learningbar.tw/")

    # Click text=登入學Bar
    page.frame(name="LBR_Banner").click("text=登入學Bar")

    # Click [placeholder="E-mail"]
    page.frame(name="LBR_Body").click("[placeholder=\"E-mail\"]")

    # Fill [placeholder="E-mail"]
    page.frame(name="LBR_Body").fill("[placeholder=\"E-mail\"]", "ericcheng26@gmail.com")

    # Press Tab
    page.frame(name="LBR_Body").press("[placeholder=\"E-mail\"]", "Tab")

    # Fill [placeholder="Password"]
    page.frame(name="LBR_Body").fill("[placeholder=\"Password\"]", "HACKER26")

    # Check [placeholder="Password tabindex="]
    page.frame(name="LBR_Body").check("[placeholder=\"Password tabindex=\"]")

    # Click input:has-text("登入")
    page.frame(name="LBR_Body").click("input:has-text(\"登入\")")

    # Click text=分類瀏覽
    page.frame(name="LBR_Body").click("text=分類瀏覽")

    # Select SUB-044
    page.frame(name="LBR_Body").select_option("select[name=\"s_Question_Subject\"]", "SUB-044")

    # Click text=送出
    page.frame(name="LBR_Body").click("text=送出")

    # Click img
    page.frame(name="LBR_Body").click("img")

    # Select SUB-045
    page.frame(name="LBR_Body").select_option("select[name=\"s_Question_Subject\"]", "SUB-045")

    # Click text=送出
    page.frame(name="LBR_Body").click("text=送出")

    # Click img
    page.frame(name="LBR_Body").click("img")

    # Select SUB-097
    page.frame(name="LBR_Body").select_option("select[name=\"s_Question_Subject\"]", "SUB-097")

    # Click text=送出
    page.frame(name="LBR_Body").click("text=送出")

    # Click img
    page.frame(name="LBR_Body").click("img")


    # Close page
    page.close()

    # ---------------------
    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
