define(function(require, exports, module) {

   var $ = require('jquery');

  //*******************  MENU HEADER  *******************//
  $('#login-trigger').click(function(){
    $(this).next('#login-content').slideToggle('fast');
    $(this).toggleClass('active');
  });

});
