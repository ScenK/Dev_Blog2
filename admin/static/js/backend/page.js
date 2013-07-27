$(document).on('submit', '#page_edit_form', function () {

  var self = $(this);
  var url_input = self.find('input[name=url]');

  if(url_input.val().search('/') > 0 || url_input.val().length === 0) {
    url_input.addClass('error');
    return false;
  }

});
