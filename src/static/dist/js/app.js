jQuery.validator.addMethod("label", function (value, element) {
    return this.optional(element) || /^[\w\s\(\)\.\-\$#]+$/i.test(value);
}, "Labels may only contain letters, numbers, spaces, and these characters: ( ) . - # $");

jQuery.validator.addMethod('phone_e164', function (value) {
    return (value.match(/^((\+)?[1-9]{1,2})?([-\s\.])?((\(\d{1,4}\))|\d{1,4})(([-\s\.])?[0-9]{1,12}){1,2}(\s*(ext|x)\s*\.?:?\s*([0-9]+))?$/));
}, 'Please enter a valid phone number in E.164 format.');

let numberOnlyNormalizer = function (value) {
    return $.trim(value.replace(/\D+/g, ''))
}

let alphaNumericOnlyNormalizer = function (value) {
    return $.trim(value.replace(/[^a-z0-9]+/gi, ''))
}

let getRootElement = function (el, selector) {
    el = $(el)
    if (!el.is(selector))
        el = el.parents(selector)
    return el
}

let validateErrorPlacement = function (error, element) {
    error.appendTo(element.parents('.form-group'))
}

$.fn.spnRecordList = function (options, callback) {
    let defaults = {
        url: '',
        method: 'POST',
        csrf_token: '',
        columns: [],
    }

    let settings = $.extend({}, defaults, options)

    // Inject text search inputs into the footer of each applicable column
    this.find('tfoot th.search').each(function () {
        $(this).html('<input class="form-control" type="text" placeholder="Search ' + $(this).text() + '" />');
    });

    // Initialize DataTables
    this.DataTable({
        dom: "<'row'<'col-sm-12 col-md-6'B><'col-sm-12 col-md-6'f>>" +
            "<'row'<'col-sm-12'tr>>" +
            "<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>",
        responsive: true, lengthChange: false, autoWidth: false, processing: true, serverSide: true,
        buttons: ['pageLength', 'copy', 'csv', 'excel', 'pdf', 'print', 'colvis'],
        lengthMenu: [
            [10, 25, 50, 100, 250, 500],
            [10, 25, 50, 100, 250, 500],
        ],
        ajax: {
            url: settings.url,
            type: settings.method,
            data: function (d) {
                d.csrfmiddlewaretoken = settings.csrf_token
            }
        },
        columns: settings.columns,
        initComplete: function () {
            this.api()
                .columns()
                .every(function () {
                    let that = this;
                    $('input', this.footer()).on('keyup change clear', function () {
                        if (that.search() !== this.value) {
                            that.search(this.value).draw();
                        }
                    });
                });
        },
        fnDrawCallback: function () {
            if (callback) {
                callback()
            }
        },
    }).buttons().container().appendTo('#' + this.attr('id') + '_wrapper .col-md-6:eq(0)');
}