import requests
import csv

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
categories= [("export-prices",2004,2021), ("merchant-prices",2000,2021), ("uk-domestic-mill-prices",2000,2021)]
with open("data.csv", "w") as writefile:
    csvwriter=csv.writer(writefile)
    csvwriter.writerow(["category","product","month","year","price"])
    for cat in categories:
        for year in range(cat[1], cat[2]+1):
            #adjustments needed because page names are not consistent
            adjustedCat = 'domestic-mill-prices' if cat[0]=="uk-domestic-mill-prices" and year >=2016 else cat[0]
            adjustedCat = 'merchant-prices-2' if cat[0]=="merchant-prices" and year==2016 else adjustedCat

            res = requests.get(f"https://www.letsrecycle.com/prices/waste-paper/{cat[0]}/{year}-{adjustedCat}/", headers=headers).text
            goodlines = [line for line in res.split("\n") if line.find("first odd")!=-1]
            removedumbshit = goodlines[0] \
                .replace("</i>","") \
                .replace("</span>","") \
                .replace("<span class='minus'><i>","")
            clean = [entry for entry in [c.split("<")[0] for c in removedumbshit.split(">")][2:-2] if len(entry)]
            for i, val in enumerate(clean[13:]):
                if (i % 13 == 0):
                    prod = val
                else:
                    #print(f"{cat[0]},{prod},{clean[i%13]},{year},{val}")
                    csvwriter.writerow([cat[0],prod,clean[i%13],year,val])