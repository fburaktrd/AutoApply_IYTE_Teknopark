import requests
import bs4
from lets_mail import EmailSender

content = requests.get("https://teknoparkizmir.com.tr/tr/firma-listesi/").text

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

soup = bs4.BeautifulSoup(content,"html.parser")

companies = []


def showCompanyInfos(company) -> None:

    print(f"Company's name: {company['name']}\n\nProfessions of company: {company['professions']}\n\nCompany's email: {company['informations']['email']}\n\nCompany's web site: {company['informations']['web']}")
    

def filterCompany(companies,keywords) -> list:
    
    filteredCompanies = []
    
    for keyword in keywords:
        for company in companies:
            
            if keyword.lower() in company['professions'].lower():

                try:
                    url = company["informations"]["web"]
                    
                    if not url.startswith("http"):
                            
                        url = f"https://{url}"

                    
                    requests.get(url,headers=headers)
                
                except requests.exceptions.SSLError:
                    
                    pass #SSLErrors is inherited from ConnectionError. If we do not check it then python automaticly assume as it is a ConnectionError
                         # but SSLError is about the security. It does not mean that the web site does not response. Thus we should add this exception.
                    
                except requests.exceptions.ConnectionError:
                    
                    continue # If the company's web site does not response then we skip to the next company.
                
                    
                filteredCompanies.append(company)
            
                
    
    return filteredCompanies


for comp in soup.find_all("div",{'class':'col-md-12 firmaListe holder'}): 
    
    company = dict()

    company['name'] = comp.find('h3',{'class':'title line'}).text 
    
    company['professions'] = comp.find('span',{'style':'padding-left:0px;font-size: 14px;'}).text.strip()
    
    company['informations'] = {"address":comp.find('div',{'class':'firmaAdres'}),
                                "tel":comp.find('div',{'class':'tel'}),
                                "web":comp.find('div',{'class':'web'}),
                                "email":comp.find('div',{'class':'eposta'})}

    for k,v in company['informations'].items():
        
        try:
            
            company['informations'][k] = v.text.strip()
        
        except:

            company['informations'][k] = 'No information found'
    
    companies.append(company)



user_keywords = []



while True:
    
    keyword = input("Please enter your keywords: ")
    
    if keyword == "":break

    user_keywords.append(keyword)

print("Here is the companies that I found for you !")

companies = filterCompany(companies,user_keywords)

for company in companies:
    
    print("\n\n"+"*-----------------------*"*5+"\n\n")
    
    showCompanyInfos(company)

print(f"There are {len(companies)} companies for your taste !")





sender = EmailSender("Your email","Your password")

sender.session_login()# we logged in.

with open("mail.txt","r") as file:
    
    text = "".join(file.readlines())

with open("sent.txt","r+") as file:
    
    sent = {e_mail.strip("\n") for e_mail in file.readlines()}
    
    for company in companies:
        
        if company["informations"]["email"] not in sent:

            sender.sendEmail(company["informations"]["email"],"Staj Başvurusu",text,["your_cv.pdf"])
            
            file.write(company["informations"]["email"]+"\n") # We write the emails in a text file because you might use the bot by searching diffrent keywords after the first run.
                                                            # And the company might have other keywords that you inputed. We do not want to send email to same company again.
                     
sender.killSession()# At the end we end the session.




#all_keywords = {keyword.strip() for keyword_list in [i.text.split(",") for i in soup.find_all('span',{'style':'padding-left:0px;font-size: 14px;'})] for keyword in keyword_list}

#This list comprehension was a good challange for me. I tried to get all those companies professions that given in the teknopark's web site in single line.
#And I did :P

