define(function(require, exports, module) {

   var  u = require('underscore'),
        $ = require('jquery');

   function tabSlide(container) {
     this.container = $(container);
     this.parents = this.container.find('.parent');
     this.children = this.container.find('.children');
     this.tree = [];
   }

   tabSlide.prototype.render = function () {
     this.init();
   }

   tabSlide.prototype.init = function () {
     var self = this;
     var parents = this.parents;
     var children = this.children;

     parents.each(function (n) {
       $(this).click(function () {
         var parent_id = $(this).attr('id');
         self.readCache(parent_id);
         children.slideUp('fast');
         $(this).find('.children').slideDown('fast');
       });
     });

     return this;
   }

   tabSlide.prototype.readCache = function (parent_id) {
     var self = this;
     var result;
     
     var exist = _.filter(self.tree, { 'parent_id': parent_id });

     exist.length > 0 ? result = exist : result = self.ajax(parent_id); 

     return result;
   } 

   tabSlide.prototype.ajax = function (parent_id) {
     var tree = this.tree;
     var self = this;

     $.ajax({
       type: 'POST',
       url: "/admin/sidebar",
       data: {
         parent_id : parent_id
       },
       success: function(resp){
         resp = $.parseJSON(resp);
         tree.push(resp);
         self.buildChildren(resp);
       }
     });

     return this;
   }

   tabSlide.prototype.buildChildren = function (json) {
     var html = '';
     var parent_id = '#' + json.parent_id;

     _.forEach(json.children, function(n){
        html += '<li><a href="' + n.url + '">' + n.name + '</a></li>';
     }); 

     $(parent_id).find('.children').append(html);
   }

   module.exports = tabSlide;
});
