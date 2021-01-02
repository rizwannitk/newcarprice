import numpy as np
from flask import Flask, request, make_response
import json
import pickle
import logging
from logging.handlers import RotatingFileHandler
from flask_cors import cross_origin

app = Flask(__name__)
model = pickle.load(open('rf.pkl', 'rb'))

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
	   	no_year=2020-int(modelyear)
	   	Present_Price= result.get("outputContexts")[2].get("parameters").get("price")
	   	Kms_Driven= result.get("outputContexts")[2].get("parameters").get("kilometer")
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
	   	
	   	fulfillmentText= "The Iris type seems to be..   !"
	   	return {
            "fulfillmentText": fulfillmentText
        }
        
            #log.write_log(sessionID, "Bot Says: "+fulfillmentText)
                
    #user_says=result.get("queryText")
    #log.write_log(sessionID, "User Says: "+user_says)
    parameters = result.get("parameters")
    Petal_length=parameters.get("number")
    Petal_width = parameters.get("number1")
    Sepal_length=parameters.get("number2")
    Sepal_width=parameters.get("number3")
    int_features = [Petal_length,Petal_width,Sepal_length,Sepal_width]
    
    final_features = [np.array(int_features)]
	 
    intent = result.get("intent").get('displayName')
    
    if (intent=='irisdata'):
        prediction = model.predict(final_features)
    
        output = round(prediction[0], 2)
    
    	
        if(output==0):
            flowr = 'Setosa'
    
        if(output==1):
            flowr = 'Versicolour'
        
        if(output==2):
            flowr = 'Virginica'
       
        fulfillmentText= "The Iris type seems to be..  {} !".format(flowr)
        #log.write_log(sessionID, "Bot Says: "+fulfillmentText)
        return {
            "fulfillmentText": fulfillmentText
        }
	       
if __name__ == '__main__':
    app.run()
#if __name__ == '__main__':
#    port = int(os.getenv('PORT', 5000))
#    print("Starting app on port %d" % port)
#    app.run(debug=False, port=port, host='0.0.0.0')

