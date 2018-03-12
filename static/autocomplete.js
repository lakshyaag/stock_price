var options = {
        url: "https://api.iextrading.com/1.0/ref-data/symbols",
        getValue: "name",
        theme: "blue-light",
        list: {
            onSelectItemEvent: function(){
                var value = $('#stock').getSelectedItemData().symbol;
                console.log(value)
                $('#stock_code').val(value);

            },
            match: {
                enabled: true
            }
        },
        requestDelay: 500

    };

$("#stock").easyAutocomplete(options);
