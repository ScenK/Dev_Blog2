
  //*********************  FORMS   *********************//
  $(".chzn-select").chosen();

  //*******************  TAGS  *******************//
  if($('input[name="tags"]').length > 0 ){
    var str = $('input[name="tags"]').val(); str = str.replace(/\,$/, '');
    $('input[name="tags"]').val(str);
  }

  //*******************  CATEGORIES  *******************//
  $('#categories_select').change(function(){
    var self = $(this);
    if(self.val() === '创建新分类'){
      jPrompt('新分类名称:', '', '添加新分类', function(cat) {
        $('#categories_select :selected').text(cat);
        $('#categories_select').append('<option>创建新分类</option>');
        $(".chzn-select").trigger("liszt:updated");
      });
    }
  });

  if($('#categories_select').val() === '创建新分类') {
      $('#categories_select').trigger('change');
  }


  //*******************  EDITOR  *******************//
  $('#wysiwyg_target').wysiwyg({
    autoGrow         : true,
    rmUnusedControls : true,
    createLink       : true,
    controls         : {
      bold                : { visible : true },
      italic              : { visible : true },
      strikeThrough       : { visible : true },
      code                : { visible : true },
      underline           : { visible : true },
      insertOrderedList   : { visible : true },
      insertUnorderedList : { visible : true },
      createLink          : { visible : true },
      removeFormat        : { visible : true },
      html                : { visible : true },
      insertImage         : {
        visible : true,
        exec: function () {
        }
      }
    }
  });

  // always make editor toolbar visible
  $(window).scroll(function () {
    var top = $(document).scrollTop();
    if ( top > 279 )
      $('.toolbar').css('top', top - 279 );
    else
      $('.toolbar').removeAttr('style');
  });

  //*************  PHOTO ADD ALERT  ***************//
  if($('.insertImage').length > 0){
    new AjaxUpload($('.insertImage'), {
      action: '/admin/diary/add-photo',
      onComplete: function(file, responseJSON){
        var obj = $.parseJSON(responseJSON);
        $('#wysiwyg_target').wysiwyg('insertHtml', '<img src="' + obj.url + '">');
      }
    });
  }

