let endInitDate = new Date();
let startInitDate = new Date(endInitDate.getFullYear(), endInitDate.getMonth(), endInitDate.getDate()-5);

let startDate = $('#start_date');
$.datetimepicker.setLocale('zh');
startDate.datetimepicker({
    value: startInitDate.toLocaleDateString(),
    timepicker: false,
    format:'Y-m-d'
});

let endDate = $('#end_date');
endDate.datetimepicker({
    value: endInitDate.toLocaleDateString(),
    timepicker: false,
    format: 'Y-m-d'
});

let date = $("#date");
date.datetimepicker({
    timepicker: false,
    format: 'Y-m-d'
});

let stockTable = $('#stockTable');

//增加按钮事件
function addBtnClick() {
    $('#code').val('');
    $('#date').val('');
    $('#open').val('');
    $('#close').val('');
    $('#zhang_die').val('');
    $('#zhang_die_fu').val('');
    $('#highest').val('');
    $('#lowest').val('');
    $('#cheng_jiao_liang').val('');
    $('#cheng_jiao_e').val('');
    $('#huan_shou_lv').val('');
    $('#addDataLabel').text('增加数据');
    $('#saveBtn').text('增加');
    $('#addData').modal('show');
}

//查询按钮事件
function findBtnClick() {

    let startDateValue = document.getElementById('start_date').value;
    if (startDateValue === "" || startDateValue ===undefined || startDateValue === null){
        startDate.css('borderColor','red');
        return;
    }else {
        startDate.css('borderColor','');
    }
    stockTable.bootstrapTable("destroy");
    //初始化表格,动态从服务器加载数据
    let toolBar = $('#toolbar');
    toolBar.css('visibility', 'visible');
    stockTable.bootstrapTable({
        toolbar: toolBar,
        uniqueId: 'id',
        method: "get",
        url: "/stock/",
        striped: true,  //表格显示条纹
        //sortName: "date",
        showExport: true,
        exportTypes: ['excel', 'xlsx'],
        exportDataType: 'all',
        exportOptions:{
            //ignoreColumn: [0],  //忽略某一列的索引
            fileName: '数据',  //文件名称设置
            worksheetName: 'sheet1',  //表格工作区名称
            tableName: '数据表',
            //excelstyles: ['background-color', 'color', 'font-size', 'font-weight'],
        },
        sortOrder: "asc",
        dataType: "json",
        pagination: true, //启动分页
        pageSize: 10,  //每页显示的记录数
        pageNumber: 1, //当前第几页
        pageList: [5, 10, 15, 20, 25],  //记录数可选列表
        search: true,  //是否启用查询
        showColumns: true,  //显示下拉框勾选要显示的列
        showRefresh: false,  //显示刷新按钮
        sidePagination: "client", //表示服务端请求 前端分页参数为client
        //设置为undefined可以获取pageNumber，pageSize，searchText，sortName，sortOrder
        //设置为limit可以获取limit, offset, search, sort, order
        queryParamsType: "undefined",
        queryParams: function queryParams(params) {   //设置查询参数
            let param = {
                pageNumber: params.pageNumber,
                pageSize: params.pageSize,
                sortName: params.sortName,
                sortOrder: params.sortOrder,
                orderNum: $("#orderNum").val(),
                code: 'cn_' + $('#findCode').val(),
                start: $('#start_date').val().replace(/-/g,''),
                end: $('#end_date').val().replace(/-/g,'')
            };
            return param;
        },
        columns:[
            {
              checkbox:true
            },
            {
                title: 'ID',
                field: 'id',
                sortable: true,
                align: 'center'
            },
            {
                title: '代码',
                field: 'code',
                sortable: true,
                align: 'center'
            },
            {
                title: '名称',
                field: 'name',
                sortable: true,
                align: 'center'
            },
            {
                title: '交易日期',
                field: 'date',
                sortable: true,
                align: 'center'
            },
            {
                title: '开盘价',
                field: 'open',
                sortable: true,
                align: 'center'
            },
            {
                title: '收盘价',
                field: 'close',
                sortable: true,
                align: 'center'
            },
            {
                title: '涨跌',
                field: 'zhang_die',
                sortable: true,
                align: 'center'
            },
            {
                title: '涨跌幅',
                field: 'zhang_die_fu',
                sortable: true,
                align: 'center'
            },
            {
                title: '最高价',
                field: 'highest',
                sortable: true,
                align: 'center'
            },
            {
                title: '最低价',
                field: 'lowest',
                sortable: true,
                align: 'center'
            },
            {
                title: '成交量',
                field: 'cheng_jiao_liang',
                sortable: true,
                align: 'center'
            },
            {
                title: '成交额',
                field: 'cheng_jiao_e',
                sortable: true,
                align: 'center'
            },
            {
                title: '换手率',
                field: 'huan_shou_lv',
                sortable: true,
                align: 'center'
            },
        ],
        responseHandler: function (res) {
            if (res.msg ==='success'){
                return {
                    "total": res.total,
                    "rows": res.rows
                };
            }else {
                return res;
            }
        }
        //onLoadSuccess: function () {  //加载成功时执行
            //alert("加载成功");
       // },
       // onLoadError: function () {  //加载失败时执行
           // alert("加载数据失败");
       // }
    });
}

//保存按钮点击事件
function saveBtnClick() {
    let data = {};
    let jsonData = $('#addStockForm').serializeArray();
    for(let i = 0; i < jsonData.length; i++){
        data[jsonData[i]['name']] = jsonData[i]['value'];
    }
    let url = '/stock/';
    let type = '';
    if ($('#saveBtn').text() === '更新'){
        type = 'put';
        let rows = stockTable.bootstrapTable('getSelections');
        data['id'] = rows[0]['id'];
    }else {
        type = 'post';
    }
    let csrfToken = $("[name='csrfmiddlewaretoken']").val();
    $.ajax({
        type: type,
        url: url,
        beforeSend: function (request) {
            request.setRequestHeader("Content-Type", "application/json");
            request.setRequestHeader("X-CSRFToken", csrfToken);
        },
        data: JSON.stringify(data),
        contentType: "application/json;charset=utf-8",
        dataType: "json",
        success: function (res) {
            if (res.msg === 'success'){
               $("#addData").modal('hide');
               if (type === 'post')
                    stockTable.bootstrapTable('prepend', res.data);
               else
                    stockTable.bootstrapTable('updateByUniqueId', {id: res.data.id, replace: true, row: res.data});
            }else {
                alert(JSON.stringify(res.data));
            }

        },
        error: function (res) {
            $("#addData").modal('hide');
            alert(res);
        }
    })
}

//删除按钮点击事件
function delBtnClick() {
    //获取选中的ID
    let ids = $.map(stockTable.bootstrapTable('getSelections'), function (row) {
              return row.id
            });
    if (ids.length === 0){
        alert('没有选中的行');
        return 0;
    }
    //采用的是前端分页模式，获取所有选中的列
    let csrfToken = $("[name='csrfmiddlewaretoken']").val();
    // 发送请求
    $.ajax({
        type: "delete",
        url: "/stock/",
        beforeSend: function (request) {
            request.setRequestHeader("Content-Type", "application/json");
            request.setRequestHeader("X-CSRFToken", csrfToken);
        },
        data: JSON.stringify(ids),
        contentType: "application/json;charset=utf-8",
        dataType: "json",
        success: function (res) {
            stockTable.bootstrapTable('remove', {field: 'id', values: res});
        },
        error: function (res) {
            alert(res)
        }
    })
}

//更新按钮点击事件
function updateBtnClick() {
//获取选中的行，因为只编辑单行，不做批量，所以先判断是否多选或者没选中
    let rows = stockTable.bootstrapTable('getSelections');
    if (rows.length === 0){
        alert('没有选中的行');
        return 0;
    }
    if (rows.length > 1) {
        alert('请只选中一行');
        return 0;
    }
    let row = rows[0];
    $('#code').val(row.code);
    $('#date').val(row.date);
    $('#open').val(row.open);
    $('#close').val(row.close);
    $('#zhang_die').val(row.zhang_die);
    $('#zhang_die_fu').val(row.zhang_die_fu);
    $('#highest').val(row.highest);
    $('#lowest').val(row.lowest);
    $('#cheng_jiao_liang').val(row.cheng_jiao_liang);
    $('#cheng_jiao_e').val(row.cheng_jiao_e);
    $('#huan_shou_lv').val(row.huan_shou_lv);
    $('#addDataLabel').text('更新数据');
    $('#saveBtn').text('更新');
    $('#addData').modal('show');
}
