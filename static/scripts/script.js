(function($) {
    function onFormSubmit(event) {
        var data = $(event.target).serializeArray();

        var t = {};
        for (var i = 0; i < data.length; i++) {
            var key = data[i].name;
            var value = data[i].value;
            t[key] = value
        }

        var thesis_create_api = '/api/thesis'
        $.post(thesis_create_api, t, function(response){
            if (response.status = 'OK'){
                $('table tr:first').after('<tr></tr>');
                $('tr:eq(1)').append('<td class="yr">'+ response.data.year + '</td>');
                $('tr:eq(1)').append('<td class="yr">'+ response.data.title + '</td>');
                //$('tr:eq(1)').append('<td class="yr">'+ response.data.abstract + '</td>');
                //$('tr:eq(1)').append('<td class="yr">'+ response.data.adviser + '</td>');
                //$('tr:eq(1)').append('<td class="yr">'+ response.data.section + '</td>');
                $('.form-section').trigger("reset");
            }
            else {
                alert("Can't access database.")
            }
        });
        return false;
    }
    function loadAllStudents(){
        var thesis_api = '/api/thesis';
        $.get(thesis_api, {}, function(response){
            console.log('thesis', response)
            response.data.forEach(function(thesis){
                $('table tr:first').after('<tr></tr>');
                $('tr:eq(1)').append('<td class="yr">'+ thesis.year + '</td>');
                $('tr:eq(1)').append('<td class="yr">'+ thesis.title + '</td>');
                /*
                $('tr:eq(1)').append('<td class="yr">'+ thesis.abstract + '</td>');
                $('tr:eq(1)').append('<td class="yr">'+ thesis.adviser + '</td>');
                $('tr:eq(1)').append('<td class="yr">'+ thesis.section + '</td>');
                */
            });
        });
    }
    $('.form-section').submit(onFormSubmit)
    loadAllStudents()
    $('.button').mouseenter(function(){
        $(this).addClass('hover')
    })
    $('.button').mouseleave(function(){
        $(this).removeClass('hover')
    })
})(jQuery)