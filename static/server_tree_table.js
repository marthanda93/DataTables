$(function(){
    var dataGrid = $("#gridContainer").dxDataGrid({
        dataSource: "/api/tree_data",
        keyExpr: "ID",
        allowColumnReordering: true,
        showBorders: true,
        grouping: {
            autoExpandAll: false,
        },
        searchPanel: {
            visible: true
        },
        paging: {
            pageSize: 10
        },  
        groupPanel: {
            visible: true
        },
        columns: [
            "CompanyName",
            "Phone",
            "Fax",
            "City",
            {
                dataField: "State",
                groupIndex: 0
            }
        ]
    }).dxDataGrid("instance");
    
    $("#autoExpand").dxCheckBox({
        value: false,
        text: "Expand All Groups",
        onValueChanged: function(data) {
            dataGrid.option("grouping.autoExpandAll", data.value);
        }
    });
});