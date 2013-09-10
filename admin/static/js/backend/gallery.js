
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
    uploadScript : '/admin/album/detail/' + album_id,
    onQueueComplete: function() {
      window.location.reload();
    }
  });

  //*******************  Fancybox  *******************//
  $(document).ready(function() {
    $("a.fancybox").fancybox({
      'titlePosition'   : 'outside',
      'overlayColor'    : '#000',
      'overlayOpacity'  : 0.8
    });
  });


