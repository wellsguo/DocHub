```java
public boolean ping(int times, String host) {
    StringBuffer ret = new StringBuffer();
    try {
        Process p = Runtime.getRuntime().exec("/system/bin/ping -c " + times + " " + host); // 10.83.50.111
        int status = p.waitFor();

        BufferedReader buf = new BufferedReader(new InputStreamReader(p.getInputStream()));
        String str;
        // 读出全部信息并显示
        while ((str = buf.readLine()) != null) {
            str = str + "\r\n";
            ret.append(str);
        }
        Log.i("Net", String.format("ping: %s", ret.toString()));

        return status == 0;
    } catch (Exception ex) {
        Log.e("Net", String.format("ping: %s", ex.getMessage()));
    }
    return false;
}

public boolean ping(){
    return ping(4, "14.215.177.38");// baidu
}
```
