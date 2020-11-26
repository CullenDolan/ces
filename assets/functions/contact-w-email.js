var AWS = require('aws-sdk');
var ses = new AWS.SES();
 
var RECEIVER = 'cullen@cloudengineeringsolutions.com';
var SENDER = 'cullen@cloudengineeringsolutions.com';

var response = {
 "isBase64Encoded": false,
 "headers": { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': 'cloudengineeringsolutions.com'},
 "statusCode": 200,
 "body": "{\"result\": \"Success.\"}"
 };

exports.handler = function (event, context) {
    console.log('Received event:', event);
    sendEmail(event, function (err, data) {
        context.done(err, null);
    });
};
 
function sendEmail (event, done) {
    var params = {
        Destination: {
            ToAddresses: [
                RECEIVER
            ]
        },
        Message: {
            Body: {
                Text: {
                    Data: 'name: ' + event.name + '\nemail: ' + event.email + '\ndesc: ' + event.desc,
                    Charset: 'UTF-8'
                }
            },
            Subject: {
                Data: 'Website Referral Form: ' + event.name,
                Charset: 'UTF-8'
            }
        },
        Source: SENDER
    };
    ses.sendEmail(params, done);
}