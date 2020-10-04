paypal.Buttons({
		createOrder: function(data, actions) {
		  // This function sets up the details of the transaction, including the amount and line item details.
		  return actions.order.create({
		    purchase_units: [{
		      amount: {
		      	currency: 'BRL',
		        value: '{{value}}'
		      }
		    }]
		  });
		},
		onApprove: function(data, actions) {
		  // This function captures the funds from the transaction.
		  return actions.order.capture().then(function(details) {
		    // This function shows a transaction success message to your buyer.
		    //alert('Transaction completed by ' + details.payer.name.given_name);
		    var xhttp = new XMLHttpRequest();
		    xhttp.open("POST","/confirmPayment",true)
		    xhttp.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
		    xhttp.send(JSON.stringify({"_id":"{{app}}","key_type":{{key_type}} }))
		  });
		}
		}).render('#paypal-button-container');
		//This function displays Smart Payment Buttons on your web page.