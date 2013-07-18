define(function(require) {

  var Account = require('./account.js'),
      Post    = require('./post.js'),
      Gallery = require('./gallery.js'),
      Comment = require('./comment.js');

  require.async('./helper/tabSlide', function(t) {
    var s = new t('.menu');
    s.render();
  });

});
