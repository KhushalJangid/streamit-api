const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const { RTCPeerConnection, RTCSessionDescription, RTCIceCandidate } = require('wrtc');

const app = express();
const server = http.createServer(app);
const io = socketIo(server);

let broadcasters = {};
let watchers = {};

io.on('connection', socket => {
  socket.on('broadcaster', () => {
    broadcasters[socket.id] = socket;
    socket.broadcast.emit('broadcaster');
  });

  socket.on('watcher', () => {
    watchers[socket.id] = socket;
    socket.broadcast.emit('watcher', socket.id);
  });

  socket.on('offer', async (data) => {
    const watcherSocket = watchers[data.id];
    watcherSocket.emit('offer', { offer: data.offer, broadcasterId: socket.id });
  });

  socket.on('answer', async (data) => {
    const broadcasterSocket = broadcasters[data.broadcasterId];
    broadcasterSocket.emit('answer', { answer: data.answer });
  });

  socket.on('candidate', async (data) => {
    const targetSocket = data.id ? watchers[data.id] : broadcasters[socket.id];
    targetSocket.emit('candidate', data.candidate);
  });

  socket.on('disconnect', () => {
    delete broadcasters[socket.id];
    delete watchers[socket.id];
  });
});

server.listen(3000, () => console.log('Server is running on port 3000'));
