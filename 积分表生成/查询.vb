Sub Main
    ' 声明变量
    Dim db As Object
    Dim queryResult As Object
    Dim exportFilePath As String
    Dim sceneInfo As Object
    Dim sheetName As String
    Dim sceneQuery As String
    Dim dataQuery As String
    Dim team1 As String
    Dim team2 As String
    Dim excelApp As Object
    Dim excelWorkbook As Object
    Dim excelSheet As Object
    Dim currentRow As Integer
    
    ' 连接到当前的 IDEA 数据库
    Set db = Client.CurrentDatabase

    ' 定义导出文件路径
    exportFilePath = "C:\Users\YourUsername\Documents\比赛数据汇总.xlsx"

    ' 获取特定时间段内的场次信息
    sceneQuery = "SELECT scene, team1, team2 FROM match_info WHERE match_date BETWEEN '2024-08-01' AND '2024-08-11'"

    Set sceneInfo = db.SqlSelect(sceneQuery)
    
    ' 初始化 Excel 应用程序
    Set excelApp = CreateObject("Excel.Application")
    Set excelWorkbook = excelApp.Workbooks.Add
    excelApp.Visible = False ' 隐藏 Excel 窗口

    ' 遍历每个场次
    sceneInfo.MoveFirst
    Do While Not sceneInfo.EOF
        ' 获取场次编号和队伍信息
        scene = sceneInfo.Fields("scene").Value
        team1 = sceneInfo.Fields("team1").Value
        team2 = sceneInfo.Fields("team2").Value
        sheetName = team1 & "VS" & team2

        ' 执行查询获取该场次的数据
        dataQuery = "SELECT * FROM player_data WHERE scene = " & scene
        Set queryResult = db.SqlSelect(dataQuery)

        ' 添加新的 sheet 并命名
        Set excelSheet = excelWorkbook.Sheets.Add
        excelSheet.Name = sheetName

        ' 将查询结果导入到新的 sheet 中
        currentRow = 1
        queryResult.ExportToExcel excelSheet, currentRow

        ' 移动到下一个场次
        sceneInfo.MoveNext
    Loop

    ' 保存 Excel 文件并关闭
    excelWorkbook.SaveAs exportFilePath
    excelWorkbook.Close False
    excelApp.Quit

    ' 清理对象
    Set excelSheet = Nothing
    Set excelWorkbook = Nothing
    Set excelApp = Nothing

    MsgBox "所有场次的数据已成功导出到: " & exportFilePath

End Sub
