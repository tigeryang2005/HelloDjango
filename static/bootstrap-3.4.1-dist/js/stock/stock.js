    let stockTable = $('#stockTable');
    //查询按钮事件
    function findBtnClick() {
        let startDate = $('#start_date');
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
            method: "get",
            url: "http://127.0.0.1:8000/stock/find",
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
            showRefresh: true,  //显示刷新按钮
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
                    code: 'cn_' + $('#code').val(),
                    start: $('#start_date').val().replace(/-/g,''),
                    end: $('#end_date').val().replace(/-/g,'')
                };
                return param;
            },
            columns:[
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
                if (res.status ==='success'){
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
        let url = $("#addStockForm").attr('action');
        let data = {};
        let jsonData = $('#addStockForm').serializeArray();
        for(let i = 0; i < jsonData.length; i++){
            data[jsonData[i]['name']] = jsonData[i]['value'];
        }
        $.ajax({
            type: "post",
            url: url,
            beforeSend: function (request) {
                request.setRequestHeader("Content-Type", "application/json");
                request.setRequestHeader("X-CSRFToken", data['csrfmiddlewaretoken']);
            },
            data: JSON.stringify(data),
            contentType: "application/json;charset=utf-8",
            dataType: "json",
            success: function (res) {
                $(".modal").modal('hide');
                stockTable.bootstrapTable('prepend', res);
            },
            error: function (res) {
              alert(res)
            }
        })
    }