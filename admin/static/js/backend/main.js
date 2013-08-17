var Helper = {

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
    return time < 10 ? "0" + time : time;
  }

}
