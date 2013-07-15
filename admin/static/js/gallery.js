define(function(require, exports, module) {

   var $            = require('jquery'),
       alerts       = require('alerts'),
       uploadifive  = require('uploadifive');

  //*******************  Add New Album  *******************//
  $('#add_new_album').click(function(){
    jPrompt('新相册名称:', '', '添加新相册', function(r) {
      if(r) {
        $.ajax({
          type: 'POST',
          url: '/admin/gallery/list',
          data: {'title': r},
          success: function(e) {
            console.log(e);
          }
        });
      }
    });
  });

  $('#add_new_photo').uploadifive({
    'method': 'post',
    'uploadScript' : window.location.href
  });
  //*************  PHOTO ADD ALERT  ***************//
  /*
  $('#add_new_photo').fineUploader({
    autoUpload: false,
    request: {
      endpoint: window.location.href
    },
    template: '<div class="qq-uploader">' +
                '<pre class="qq-upload-drop-area"><span>拖动文件至此</span></pre>' +
                '<span class="qq-upload-button picture icon-white-text">上传新相片</span>' +
                '<span class="qq-drop-processing"><span>上传中...</span><span class="qq-drop-processing-spinner"></span></span>' +
                '<ul class="qq-upload-list" style="margin-top: 10px; text-align: center;"></ul>' +
              '</div>'
  }); 
  */
});
