## 查看PowerShell 版本

```shell
$PSVersionTable.PSVersion
```



## PowerShell和PowerShell核心的区别

下表描述了PowerShell和PowerShell核心之间的区别：

| 比较项                      | PowerShell                     | PowerShell核心                                            |
| --------------------------- | ------------------------------ | --------------------------------------------------------- |
| 版本                        | 1.0 至 5.1                     | 6.0                                                       |
| 平台支持                    | Windows                        | Linux, MacOS 和 Windows                                   |
| 依赖                        | .NET Framework                 | .NET Core                                                 |
| 启动为                      | `powershell.exe`               | 对于MacOS和Linux启动为`pwsh`；对于Windows启动为`pwsh.exe` |
| 使用/运行时环境             | 它依赖于.NET Framework运行时。 | 它依赖于.NET Core运行时。                                 |
| `$PSVersionTable.PSEdition` | 设置为Desktop                  | 它设置为Core。                                            |



get-command

get-help

Get-processor

