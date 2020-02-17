var b = new Buffer.alloc(10, 'JavaScript');
var s = b.toString('base64');
// SmF2YVNjcmlwdA==
console.log(s);

var b = new Buffer.alloc(10, 'SmF2YVNjcmlwdA==', 'base64')
var s = b.toString();
// JavaScript
console.log(s);


var b = new Buffer.alloc(10, 'SmF2YVNjcmlwdA==', 'base64')
var s = b.toString('hex');
// 4a617661536372697074
console.log(s);

var b = new Buffer.alloc(10, '4a617661536372697074', 'hex')
var s = b.toString('utf8');
// JavaScript
console.log(s);

var fs = require('fs');

// function to encode file data to base64 encoded string
function base64_encode(file) {
    // read binary data
    var bitmap = fs.readFileSync(file);
    // convert binary data to base64 encoded string
    return new Buffer.alloc(bitmap.length, bitmap).toString('base64');
}

// function to create file from base64 encoded string
function base64_decode(base64str, file) {
    // create buffer object from base64 encoded string, it is important to tell the constructor that the string is base64 encoded
    var bitmap = new Buffer.alloc(base64str.length, base64str, 'base64');
    // write buffer to file
    fs.writeFileSync(file, bitmap);
    console.log('******** File created from base64 encoded string ********');
}

// convert image to base64 encoded string
var base64str = base64_encode('logo.png');
console.log(base64str);
// convert base64 string back to image 
base64_decode(base64str, 'copy.jpg');