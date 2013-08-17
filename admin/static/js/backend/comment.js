
  //*******************  Call Comment Reply  *******************//
  $('.comment_back').click(function() {

    var self   = $(this);

    if($('.admin-reply-area').length>0) $('.admin-reply-area').remove();

    var target = self.parent().parent();
    $(reply_html).insertAfter(target);
    $('body').animate({ scrollTop: $('.admin-reply-area').offset().top - 200}, 900);

  });

    var reply_html = '<tr class="item admin-reply-area">'+
                      '<td colspan="6" class="elem">'+
                        '<label>回复:</label>'+
                        '<div class="indent">'+
                         '<textarea class="medium" id="message" name="message" rows="5"></textarea>'+
                         '<br><br>'+
                         '<input id="do_send" name="send" type="submit" class="button-a gray" value="发送"> &nbsp;&nbsp;<button class="button-a dark-blue" id="cancel_send">取消</button>'+
                        '</div>'+
                      '</td>'+
                    '</tr>';

  //*******************  Cancel Comment Reply  *******************//
  $(document).on('click', '#cancel_send', function() {
    $('.admin-reply-area').remove();
  });

  //*******************  Do Comment Reply  *******************//
  $(document).on('click', '#do_send', function() {
    var target = $('.admin-reply-area').prev(),
        email  = target.data('email'),
        did    = target.data('did'),
        author = target.data('author'),
        title  = target.data('title'),
        content= $('#message').val();

    $.ajax({
      type: 'POST',
      url: "/admin/comment/reply",
      data: {
        email   : email,
        author  : author,
        title   : title,
        did     : did,
        content : content
      },
      success: function(e){
        console.log(e);
      }
    });

    $('.admin-reply-area').fadeOut();

    var html =  $('#example tbody').find('tr:first-child').clone().addClass('ajax-new-comment hide');

    $(html.find('td')[1]).text('博主回复');
    $(html.find('td')[2]).text(content);
    $(html.find('td')[3]).text(title);
    $(html.find('td')[4]).text(Helper.getTime());
    $(html.find('td')[5]).text('');

    html.prependTo('#example');
    $('body').animate({ scrollTop: $('.ajax-new-comment').offset().top - 200}, 900);
    $('.ajax-new-comment').fadeIn(1000);
  });
