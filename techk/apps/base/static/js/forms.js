var $datetimePicker = $('.datetime-picker');
if ($datetimePicker.datetimepicker) {
  $datetimePicker.datetimepicker({
    date: $datetimePicker.val(),
    format: 'DD/MM/YYYY HH:mm',
    locale: 'es'
  });
}

var $datePicker = $('.date-picker');
if ($datePicker.datetimepicker) {
  $datePicker.datetimepicker({
    date: $datePicker.val(),
    format: 'DD/MM/YYYY',
    locale: 'es'
  });
}

var $timePicker = $('.time-picker');
if ($timePicker.datetimepicker) {
  $timePicker.datetimepicker({
      date: $timePicker.val(),
      format: 'HH:mm',
      locale: 'es'
    });
}

// activate select2
$('select').not('.not-select2, *[id*=__prefix__]')
  .select2({
    width: '100%'
  });

$('.add-item').click(function(ev) {
    ev.preventDefault();
    var prefix = $(this).attr('prefix').split('-')[0];
    var count = $('#' + prefix + '-formset-container').children().length;
    var tmplMarkup = $('#' + prefix + '-formset-template').html();
    var compiledTmpl = tmplMarkup.replace(/__prefix__/g, count++);

    // append new form
    $('div#' + prefix + '-formset-container').append(compiledTmpl);

    // new formset
    var $formset = $('#' + prefix + '-formset-container').children().last();

    // replace formset title
    var title = $formset.find('h4').attr('text');
    $formset.find('h4').text(title + ' ' + count);

    // activate select2 in choice fields
    var $selects = $formset.find('select');

    // for each new select
    $selects.each(function() {
      // activate select2
      $(this).select2({
        width: '100%'
      });
    });

    // TODO supports multiple-selects

    // update form count
    $('#id_' + prefix + '-TOTAL_FORMS').attr('value', count);

    // some animate to scroll to view our new form
    $('html, body').animate({
          scrollTop: $formset.position().top - 200
        }, 800);
  });
