// The only time the user data (account balances) and order execution websockets will fire, is if you create or cancel an order, or an order gets filled or partially filled
import { createRequire } from 'module';
const require = createRequire(import.meta.url);

const Binance = require('node-binance-api');
const binance = new Binance().options({
  APIKEY: 'SFa5lhBmfAvoxRZ5B7uG8GaTqHuOTjq3uKCr84X0glpEF2sRUPlVeuPZvIK6SMhZ',
  APISECRET: 'GFYSHgI4J6VlbFIgqfkjXkKX30AgNzPIiS994RqnuYbg7yTsjLc5kbh6RiXXALfc'
});

function balance_update(data) {
	console.log("Balance Update");
	for ( let obj of data.B ) {
		let { a:asset, f:available, l:onOrder } = obj;
		if ( available === "0.00000000" ) continue;
		console.log(asset+"\tavailable: "+available+" ("+onOrder+" on order)");
	}
}
function execution_update(data) {
	let { x:executionType, s:symbol, p:price, q:quantity, S:side, o:orderType, i:orderId, X:orderStatus } = data;
	if ( executionType === "NEW" ) {
		if ( orderStatus === "REJECTED" ) {
			console.log("Order Failed! Reason: "+data.r);
		}
		console.log(symbol+" "+side+" "+orderType+" ORDER #"+orderId+" ("+orderStatus+")");
		console.log("..price: "+price+", quantity: "+quantity);
		return;
	}
	//NEW, CANCELED, REPLACED, REJECTED, TRADE, EXPIRED
	console.log(symbol+"\t"+side+" "+executionType+" "+orderType+" ORDER #"+orderId);
}
binance.websockets.userData(balance_update, execution_update);