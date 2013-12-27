  //*************  PHOTO ADD ALERT  ***************//
  var album_name = '未分类';
  $('#add_new_photo').uploadifive({
    method       : 'post',
    dnd          : false,
    fileType     : 'image',
    formData     : {'album_name' : album_name},
    uploadScript : '/admin/album/detail/' + album_name,
    onQueueComplete: function(e) {
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