define(function(require, exports, module) {

   var $          = require('jquery'),
       dataTable  = require('dataTable');

  //********************* TABLE (NEWS) *********************//
  $('#example').dataTable({
    "sPaginationType": "full_numbers"
  });

  //*******************  MENU HEADER  *******************//
  $('#login-trigger').click(function(){
    $(this).next('#login-content').slideToggle();
    $(this).toggleClass('active');
  });

  //*******************  POST  *******************//
  var str = $('input[name="tags"]').val();
  str = str.replace(/\,$/, '');
  $('input[name="tags"]').val(str);

});
