  //*******************  MENU HEADER  *******************//
  $('#login-trigger').click(function(){
    $(this).next('#login-content').slideToggle('fast');
    $(this).toggleClass('active');
  });
  
  //******************* Form Validation *****************// 
  $('#account_settings_form').on('submit', function() {
    var self = $(this),
        pass1 = self.find('#pass1'),
        pass2 = self.find('#pass2');

    if(pass1.val().length > 0 || pass2.val().length > 0) {
      if(pass1.val() !== pass2.val()) {
        pass1.addClass('error'); 
        pass2.addClass('error'); 
        return false;
      }
    }
  });

  $('input').focus(function () {
    if($(this).hasClass('error')) $(this).removeClass('error');
  });

  //********************* Tooltip *********************// 
  $(".tip-top").tipTip({
    defaultPosition: "top", 
    delay: 100, 
  });

  //*********************  FORMS   *********************//
  if($('#up_avatar_btn').length > 0){
    new AjaxUpload($('#up_avatar_btn'), {
      action: '/admin/account/settings/upload_avatar',
      onSubmit: function () {
        $('.filename').val('uploading...');
      },
      onComplete: function(file, responseJSON){
        var obj = $.parseJSON(responseJSON);
        $('.filename').val(obj.url);
      }
    });
  }
