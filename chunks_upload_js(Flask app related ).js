var $ = require('jquery');
var uploadHost = "http://127.0.0.1:4000";
var ChunkUploader = function (file, options) {
  options = options || {};
  if (!this instanceof ChunkUploader) {
    return new ChunkUploader(file, options);
  }

  this.file = file;

  this.options = $.extend({
    url: uploadHost + '/upload'
  }, options);

  this.fileSize = this.file.size;
  console.log ('>>> ' + this.fileSize) ;
  this.chunkSize = (10 * 1); // 10 octet
  this.rangeStart = 0;
  this.rangeEnd = this.chunkSize;

  if ('mozSlice' in this.file) {
    this.sliceMethod = 'mozSlice';
  }
  else if ('webkitSlice' in this.file) {
    this.sliceMethod = 'webkitSlice';
  }
  else {
    this.sliceMethod = 'slice';
  }
  if (options.start) {
    this.start();
  }
};
/**
 *
 * @type {{_upload: Function, _onChunkComplete: Function, start: Function, pause: Function, resume: Function}}
 */
ChunkUploader.prototype = {

// Internal Methods __________________________________________________

  _upload: function () {
    var self = this;
    var chunk;
    // Slight timeout needed here (File read / AJAX readystate conflict?)
    setTimeout(function () {
      // Prevent range overflow
      if (self.rangeEnd > self.fileSize) {
        self.rangeEnd = self.fileSize;
      }

      chunk = self.file[self.sliceMethod](self.rangeStart, self.rangeEnd);

      var headers = {
        "Content-Info" : 'name=' + self.file.name,
        // @see https://github.com/swagger-api/swagger-ui/issues/1576
        /*W3 tells us - Any HTTP/1.1 message containing an entity-body SHOULD include a
         Content-Type header field defining the media type of that body. If and only if
         the media type is not given by a Content-Type field, the recipient MAY attempt to guess
         the media type via inspection of its content and/or the name extension(s) of the URI used to
         identify the resource. If the media type remains unknown, the recipient SHOULD treat it
         as type "application/octet-stream".*/
        "Content-Type": "application/octet-stream"
      };
      if (self.rangeStart !== 0) {
        if (!self.id){
          alert ('no id');
          return ;
        }
        headers['Content-Info'] += ';id=' + self.id  + ';seek=' + self.rangeEnd + ';size=' + self.fileSize ;
      }
      $.ajax(self.options.url, {
        data: chunk,
        type: 'POST',
        processData: false,
        mimeType: 'application/octet-stream',
        headers: headers,
        success: self._onChunkComplete.bind(self),
        error: function (error) {
          console.log(error);
        }
      });
    }, 20);
  },

// Event Handlers ____________________________________________________
  /**
   *
   * @param response
   * @private
   */
  _onChunkComplete: function (response) {
    // If the end range is already the same size as our file, we
    // can assume that our last chunk has been processed and exit
    // out of the function.
    if (this.rangeEnd === this.fileSize) {
      //alert ('rangeEnd >>' + this.rangeEnd);
      //alert ('fileSize >>' + this.fileSize );
      return;
    }
    // get the current temp file id
    this.id = JSON.parse(response).id ;
    // Update our ranges
    this.rangeStart = this.rangeEnd;
    this.rangeEnd = this.rangeStart + this.chunkSize;

    // Continue as long as we aren't paused
    if (!this.is_paused) {
      this._upload();
    }
  },

// Public Methods ____________________________________________________

  start: function () {
    this._upload();
  },
  /**
   *
   */
  pause: function () {
    this.is_paused = true;
  },
  /**
   *
   */
  resume: function () {
    this.is_paused = false;
    this._upload();
  }
};


export default ChunkUploader;
