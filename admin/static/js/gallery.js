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
            window.location.reload();
          }
        });
      }
    });
  });

  //*************  PHOTO ADD ALERT  ***************//
  var album_id = $('#add_new_photo').data('albumid');
  $('#add_new_photo').uploadifive({
    method       : 'post',
    dnd          : false,
    fileType     : 'image',
    formData     : {'album_id' : album_id},
    uploadScript : '/admin/album/detail/' + album_id
  });
  
});
