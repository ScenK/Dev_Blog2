define(function(require, exports, module) {

   var $            = require('jquery'),
       alerts       = require('alerts'),
       uploadifive  = require('uploadifive');

  //*******************  Add New Album  *******************//
  $('#add_new_album').click(function(){
    jPrompt('新相册名称:', '', '添加新相册', function(r) {
      if(r) {
        $.ajax({
          type   : 'POST',
          url    : '/admin/gallery/list',
          data   : {'title': r},
          success: function(e) {
            console.log(e);
          }
        });
      }
    });
  });

  //*************  PHOTO ADD ALERT  ***************//
  $('#add_new_photo').uploadifive({
    method       : 'post',
    dnd          : false,
    fileType     : 'image',
    uploadScript : window.location.href
  });
  
});
