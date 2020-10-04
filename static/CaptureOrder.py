from static.PayPalClient import PayPalClient
from paypalcheckoutsdk.orders import OrdersGetRequest
from paypalcheckoutsdk.orders import OrdersCaptureRequest

class CaptureOrder(PayPalClient):

  #2. Set up your server to receive a call from the client
  """this sample function performs payment capture on the order.
  Approved order ID should be passed as an argument to this function"""

  def capture_order(self, order_id, orders, app, _id, key_type,debug=False):
    """Method to capture order using order_id"""
    request = OrdersCaptureRequest(order_id)
    #3. Call PayPal to capture an order
    response = self.client.execute(request)
    #4. Save the capture ID to your database. Implement logic to save capture to your database for future reference.
    order = {"Status Code":response.status_code,
    		 "Status":response.result.status,
    		 "Order ID": response.result.id,
    		 "Buyer Name":response.result.payer.name.given_name + " " + response.result.payer.name.surname,
    		 "Buyer Email":response.result.payer.email_address}
    links=[]
    for link in response.result.links:
    	links.append('{}: {} Call Type: {}'.format(link.rel, link.href, link.method))
    capture_ids=[]
    for purchase_unit in response.result.purchase_units:
    	for capture in purchase_unit.payments.captures:
    		capture_ids.append(capture.id)
    
    order["Links"] = links
    order["Capture IDs"] = capture_ids

    if key_type == 1:
            limit = 10000
    elif key_type == 2:
        limit = 100000
    elif key_type == 3:
        limit = 1000000

    query = app["Applications"].find_one({"_id":ObjectId(_id)})
    app["Applications"].update_one(query,{"$set":{"order_id":response.result.id,
                                                "key":hex(round(time.time()))+"_"+secrets.token_hex(32),
                                                "key_status":True,
                                                "key_type":key_type,
                                                "requisitions":0,
                                                "limit":limit}})
    orders["Orders"].insert_one(order)
    return response