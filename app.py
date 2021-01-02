import numpy as np
from flask import Flask, request, make_response
import json
import pickle
import logging
from logging.handlers import RotatingFileHandler
from flask_cors import cross_origin

app = Flask(__name__)
model = pickle.load(open('random_forest_regression_model.pkl', 'rb'))

@app.route('/')
def hello():
    print('this is logging appplication')
    return 'Hello World'

@app.route('/webhook', methods=['POST'])
@cross_origin()
def webhook():

    req = request.get_json(silent=True, force=True)

    #print("Request:")
    #print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    #print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def processRequest(req):
	
    result = req.get("queryResult")

    #app.logger.info('logged in successfully')
    print(result)

    intent = result.get("intent").get('displayName')
	
	#log.write_log(sessionID, "Bot Says: "+intent)
    
    if (intent=='final'):
	   	Owner = result.get("outputContexts")[2].get("parameters").get("owner")
	   	dealer= result.get("outputContexts")[2].get("parameters").get("dealer")
	   	modelyear= result.get("outputContexts")[2].get("parameters").get("modelyear")
	   	Year=2020-int(modelyear)
	   	Present_Price= result.get("outputContexts")[2].get("parameters").get("price")
	   	Kms_Driven= result.get("outputContexts")[2].get("parameters").get("kilometer")
	   	Kms_Driven2=np.log(Kms_Driven)
	   	fueltype= result.get("outputContexts")[2].get("parameters").get("fueltype")
	   	transmission= result.get("outputContexts")[2].get("parameters").get("transmission")
	  
	   	if (fueltype=="Petrol"):
	   	    Fuel_Type_Petrol=1;
	   	    Fuel_Type_Diesel=0;
	   	else :
	   	    if (fueltype=="Desiel"):
	   	        Fuel_Type_Petrol=0;
	   	        Fuel_Type_Diesel=1;
	   	    else :
	   	        Fuel_Type_Petrol=0;
	   	        Fuel_Type_Diesel=0;
	   	if (dealer=="Individual") :
	   	    Seller_Type_Individual=1;
	   	else :
	   	    Seller_Type_Individual=0;
	   	if (transmission=="Individual") :
	   	    Transmission_Manual=1;
	   	else :
	   	    Transmission_Manual=0;
	   	print ('owner is ' + str(Owner) )
	   	
	   	
	   	prediction=model.predict([[Present_Price,Kms_Driven2,Owner,Year,Fuel_Type_Diesel,Fuel_Type_Petrol,Seller_Type_Individual,Transmission_Mannual]])
	   	output=round(prediction[0],2)
	   	
	   	fulfillmentText= "You Can Sell The Car at {}".format(output)
	   	return {
            "fulfillmentText": fulfillmentText
        }
        
            #log.write_log(sessionID, "Bot Says: "+fulfillmentText)
                
    #user_says=result.get("queryText")
    #log.write_log(sessionID, "User Says: "+user_says)
    
    
       
if __name__ == '__main__':
    app.run()
#if __name__ == '__main__':
#    port = int(os.getenv('PORT', 5000))
#    print("Starting app on port %d" % port)
#    app.run(debug=False, port=port, host='0.0.0.0')

