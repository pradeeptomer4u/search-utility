Build an Intelligent Online Shopping Assistant that will help you get the best deal for the product that you want to buy. 

Framwork Django 3.0

Language Python 3.8

Database Sqlite3

Reuse API : Shopclues,Paytm Mall,Tata Cliq

product list url : /product 

• When user enters the search string and clicks on search, then it searches all the three API providers simultaneously (using multi-threading) 
 Select the product that closely matches the Users’s search string 

▪ E.g. If I have searched for Asus Zenfone Max M1, so it may be able to get Asus Zenfone Max M1 or M2 but not other phones or covers. 

▪ If I search for Mi Note 8 Pro Case, it may get results for Mi Note Pro Case but should not bring in phones or other cases 

▪ This should be closest match to user’s query 

 All Item should have Product Name, URL, Image and Price o All the results should be aggregated into a local database – Product Name, URL, 
Image and Price are the mandatory fields 

o These APIs use pagination, so you need to ensure all records are retrieved o If the results already exist in local database, update existing records o Display matching records from your local database (first time nothing would be 

