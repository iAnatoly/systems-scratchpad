const WebSocket = require('ws');

//This will open the connection*
// const url = 'wss://mtg-ca-1.anymeeting.com/socket.io/?EIO=3&transport=websocket&sid=RWBq1x3wqF6PstggABRt';
//ws = new WebSocket(url); 
const ws = new WebSocket('wss://echo.websocket.org/', {
  origin: 'https://websocket.org'
});
        
ws.on('open', function open() {
  console.log('connected');
  ws.send(Date.now());
});

ws.on('close', function close() {
  console.log('disconnected');
});

ws.on('message', function incoming(data) {
  console.log(`Roundtrip time: ${Date.now() - data} ms`);

  setTimeout(function timeout() {
    ws.send(Date.now());
  }, 500);
});
        
