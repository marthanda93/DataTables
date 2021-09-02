$(function(){
    var dataGrid = $("#gridContainer").dxDataGrid({
        dataSource: new DevExpress.data.DataSource({
            load: function(values) {
                return $.ajax({
                    url: "/api/tree_data",
                    method: "POST",
                    data: values
                })
            },
        }),
        keyExpr: "ID",
        allowColumnReordering: true,
        highlightSearchText: true,

        //Filter
        headerFilter: { visible: true },
        filterPanel: { visible: true },

        // pagination
        paging: {
            pageSize: 10
        },

        searchPanel: {
            visible: true
        },

        showBorders: true,

        grouping: {
            autoExpandAll: false,
        },
        groupPanel: {
            visible: true
        },

        allowColumnReordering: true,
        allowColumnResizing: true,
        columnAutoWidth: true,
        columnChooser: {
            enabled: true
        },
        columnFixing: { 
            enabled: true
        },

        columns: [{ 
            dataField: "CompanyName",
            width: 500,
        },{ 
            dataField: "Phone",
            width: 500,
        },{ 
            dataField: "Fax",
            width: 500,
        },{ 
            dataField: "City",
            width: 500,
        },{
            dataField: "State",
            groupIndex: 0
        }]
    }).dxDataGrid("instance");
    
    $("#autoExpand").dxCheckBox({
        value: false,
        text: "Expand All Groups",
        onValueChanged: function(data) {
            dataGrid.option("grouping.autoExpandAll", data.value);
        }
    });
});
