  //*************  PHOTO ADD ALERT  ***************//
  $('#add_new_photo').uploadifive({
    method       : 'post',
    dnd          : false,
    fileType     : 'image',
    uploadScript : '/admin/gallery',
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