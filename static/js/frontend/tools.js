var Tools = {
  
  emailCheck: function (target) {
    var rule = /^[a-zA-Z0-9]+[a-zA-Z0-9_.-]+[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+[a-zA-Z0-9_-]+.[a-z]{2,4}$/;
    if(!rule.test(target.val())){
      target.addClass('email-error');
      return false;
    }else{
      target.removeClass('email-error');
      return true;
    }
  },

  emptyCheck: function (array) {
    var flag = true;
    $.each(array, function(){
      var self = $(this);
      if(self.val().length == 0){
        self.addClass('error');
        flag = false;
        return;
      }else{
        self.removeClass('error');
        return true;
      }
    });
    return flag;
  },

  getTime: function () {
    var date = new Date();
    var year, month, day, hour, minute, second;
    hour = this.jsTimeFix(date.getHours());
    minute = this.jsTimeFix(date.getMinutes());
    second = this.jsTimeFix(date.getSeconds());
    year = date.getFullYear();
    month = this.jsTimeFix(date.getMonth()+1);
    day = this.jsTimeFix(date.getDate());
    var time = year + '-' + month + '-' + day + ' ' + hour +':' + minute + ':' + second;
    return time;
  },

  jsTimeFix: function (time) {
    return time<10 ? "0"+time : time;
  },

  buildCommentHtml: function (name, time, content) {
    var html="";
    html += '<small class="commentmetadata"><a>' +
            time +
            '</a></small><cite>' +
            name +
            '<span>:</span></cite><div class="comment-content"><p>' +
            content +
            '</p></div>';
    return html;
  }
}
