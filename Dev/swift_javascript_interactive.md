在开发过程中，我们可能遇到ios代码与js交互的情况,本人第一次使用遇到了很多坑，这里纪录一下，方便自己，也方便需要的人。

### 1. 第一步先建一个接口（协议）并继承JSExport

这里实现两个方法提供给js调用的方法

```swift
import JavaScriptCore

@objc protocol SwiftJavaScriptDelegate:JSExport{

    func show()

    func showAlert(_ str:String,_ msg:String)

}
```

### 2. 第二步需要写一个类去实现上一步的接口（协议）


*注意：*

1. 这里必须要继承 `nsobject` 否则会报错

2. 如果要传参数的话一定要写成类似与  
   ```
   func showAlert(_ str:String,_ msg:String)
   ```
   `_ str:String` 这个 `_` 一定要加不然无法调用（调用无效果），在 `swift3.0` 中就这样，其他版本没有测试就不清楚了。

```swift
@objc class SwiftJavaScriptModel:NSObject,SwiftJavaScriptDelegate {

    func show() {
        print("js调用我了")
    }

    func showAlert(_ str:String,_ msg:String){
        print("js调用我了:",str,msg)
    }

}
```

### 3. 开始在控制器中测试

```swift
//
//  ViewController.swift
//  WEBJSTest
//
//  Created by admin on 17/8/5.
//  Copyright © 2017年 tdin360. All rights reserved.
//

import UIKit
import WebKit
import JavaScriptCore

class ViewController: UIViewController,UIWebViewDelegate{
    var  context:JSContext!

    override func viewDidLoad() {
        super.viewDidLoad()
        self.setupUI()
    }

    func setupUI() {
        self.view.addSubview(webView)
        let url = Bundle.main.path(forResource: "index", ofType: "html")
        self.webView.loadRequest(URLRequest(url: URL(string:url!)!))
        self.webView.delegate=self
        self.view.addSubview(btn)
    }

    lazy var webView:UIWebView={
        let webView = UIWebView(frame:self.view.bounds)
        return webView
    }()

    //用于点击调用js的按钮
    lazy var btn:UIButton={
        let btn = UIButton(frame:CGRect(x:0,y:300,width:100,height:40))
        btn.backgroundColor=UIColor.blue
        btn.setTitle("调用js", for: .normal)
        btn.addTarget(self, action: #selector(onClick), for: .touchUpInside)
        return btn
    }()

    // swift 调用 js
    func onClick()  {
        let f = context?.objectForKeyedSubscript("swift")
        _=f?.call(withArguments: [["name":"admin","pass":"fdsfds"]])
    }

    func webViewDidFinishLoad(_ webView: UIWebView) {
        let model = SwiftJavaScriptModel()
        //获取context
        context = self.webView.value(forKeyPath: "documentView.webView.mainFrame.javaScriptContext") as! JSContext
        //这里注册一个标示给js访问
        context.setObject(model, forKeyedSubscript:"model" as (NSCopying & NSObjectProtocol)!)
        let url = Bundle.main.url(forResource: "index", withExtension: "html")
        context.evaluateScript(try? String(contentsOf: url!, encoding: String.Encoding.utf8))
        context.exceptionHandler = {(context, exception) in
            print("exception 错误@", exception ?? "")
        }

    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
    }

}
```

### 4. html代码

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Title</title>
<script>
    //这个提交给swift调用并传参数
    function swift(obj){
        alert("swift调用我了"+obj["name"]+"--"+obj["pass"]);
    }
</script>
</head>

<body>
<h1>html</h1>
    <button onclick="model.showAlert('参数1','参数2')">调用swift(有参数)代码</button>
    <button onclick="model.show()">调用swift(无参数)代码</button>
</body>
</html>
```

这里贴了源码，如果遇到问题欢迎留言，有什么更好的方法欢迎一起交流。