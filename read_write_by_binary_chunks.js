#!/usr/bin/env node
const meow = require('meow');
var path = require('path');
var fs = require('fs');

const CHUNCK_SIZE = 100;

const cli = meow(
    "push " +
    "$filename  " +
    "$host "
);
// console.log (cli.help);
var filename = cli.input[0];
var host = cli.input[1];
if (!filename || !host) {
    throw new Error('no host/filename specified !');
}
var fileDescriptor;
var totalChunks ;

/**
 *
 * @param buffer
 * @param chunkOffset
 * @param chunkSize
 * @param lastChunk
 */
var appendChunk = function (buffer, chunkOffset, chunkSize, lastChunk) {
    if (!fileDescriptor) {
        fileDescriptor = fs.openSync(filename + '_2', 'a');
        totalChunks = 0 ;
    }
    totalChunks++ ;
    // write to created file
    // fs.write(fd, buffer, offset, length[, position], callback)#
    fs.write(fileDescriptor, buffer, 0, buffer.length, (chunkOffset * buffer.length), function (err, num) {
        console.log(buffer.toString('utf-8', 0, num));
        /**
         *
         */
        if (lastChunk) {
            console.log('ended copied \n');
            console.log ('total chunks : ' + totalChunks);
            fs.close(fileDescriptor);
        }
    });

};
/**
 *
 */
fs.open(filename, 'r',
    /**
     *
     * @param status
     * @param fd
     */
    function (status, fd) {
        if (status) {
            console.log(status.message);
            return;
        }
        var buffer;
        var currentOffset = 0;
        /**
         * loop
         */
        (function continueReading() {
            buffer = new Buffer(CHUNCK_SIZE);
            fs.read(fd, buffer, 0, CHUNCK_SIZE, currentOffset * CHUNCK_SIZE, function (err, num) {
                //console.log(buffer.toString('utf-8', 0, num));
                //console.log(buffer);
                if (num < CHUNCK_SIZE) {
                    // we need only copy
                    appendChunk(buffer.slice(0, num), currentOffset++, CHUNCK_SIZE, true);
                }
                else {
                    appendChunk(buffer, currentOffset++, CHUNCK_SIZE);
                    continueReading();
                }
            });
        })();

    });
