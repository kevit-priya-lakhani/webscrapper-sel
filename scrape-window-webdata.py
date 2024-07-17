from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains 

options = Options()

service = Service("/usr/bin/chromedriver")
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://www.gordijnen.nl/wiki")
action = ActionChains(driver) 
  

WebDriverWait(driver,10).until(
    ec.presence_of_element_located((By.ID,"CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"))
)

close_cookies=driver.find_element(By.ID,"CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll")
close_cookies.click()


close_popup=driver.find_element(By.XPATH,'//*[@id="wrap"]/div[4]/div[3]/div/a')
close_popup.click()

data=''
y=0

while True:
    try:
        y+=1
        faqs=driver.find_element(By.XPATH,f'/html/body/main/div[4]/div[1]/div[1]/div/div/div[2]/div[{y}]/h2/button')
        driver.execute_script("arguments[0].scrollIntoView();", faqs)
        faqs.click()
        # print("Type: ",faqs.text)
        data+=faqs.text+'\n\n'
        x=1
        while True:
            try:
                WebDriverWait(driver,2).until(
                ec.element_to_be_clickable((By.XPATH,f'/html/body/main/div[4]/div[1]/div[1]/div/div/div[2]/div[{y}]/div/div/div[{x}]/p/a')))
                qn=driver.find_element(By.XPATH,f'/html/body/main/div[4]/div[1]/div[1]/div/div/div[2]/div[{y}]/div/div/div[{x}]/p/a')
                driver.execute_script("arguments[0].scrollIntoView();", qn)
                action.move_to_element(qn)
                action.click(qn).perform()
                # print('Question: ',qn.text)
                data+='Question: '+ qn.text+'\n'
                ans=driver.find_element(By.XPATH,f'/html/body/main/div[4]/div[1]/div[1]/div/div/div[2]/div[{y}]/div/div/div[{x}]/div')
                # print('Answer: ',ans.text)
                data+='Answer: '+ ans.text+'\n'
                x+=1        
            except Exception as e: 
                break
    except Exception as e: 
        break
data+='\tYOU HAVE REACHED THE END OF FILE'
f = open("faq-content.txt", "w")
f.write(data)
f.close()

driver.quit()