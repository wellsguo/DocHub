# [HttpURLConnection response code handling](https://codereview.stackexchange.com/questions/45819/httpurlconnection-response-code-handling)



This snippet from a downloader callable handles HTTP status codes. I need critique on both the style (`for` or `do-while` loop better here?) and functionality. Should I manage the delay differently? Do I need to handle `InterruptedException` specifically?

```java
HttpURLConnection connection = null;
boolean connected = false;
outer:
for (int retry = 0; retry <= RETRIES && !connected; retry++) {
  if (retry > 0) {
    log.warning("retry " + retry + "/" + RETRIES);
    Thread.sleep(RETRY_DELAY_MS);
  }
  connection = (HttpURLConnection) entries.openConnection();
  connection.connect();
  switch (connection.getResponseCode()) {
    case HttpURLConnection.HTTP_OK:
      log.fine(entries + " **OK**");
      connected = true;
      break; // fine, go on  
    case HttpURLConnection.HTTP_GATEWAY_TIMEOUT:
      log.warning(entries + " **gateway timeout**");
      break;// retry
    case HttpURLConnection.HTTP_UNAVAILABLE:
      System.out.println(entries + "**unavailable**");
      break;// retry, server is unstable
    default:
      log.severe(entries + " **unknown response code**.");
      break outer; // abort
  }
}
connection.disconnect();
log.severe("Aborting download of dataset.");
```



Right, how does this code work? There are a few problems I can (now) see in here:

1. On HTTP_OK, it `breaks` out of the switch, then it exits the loop (because `&& !connected`), and then immediately disconnects and logs a severe error? This can't be right?
2. `HTTP_GATEWAY_TIMEOUT` logs a warning.... great, but `HTTP_UNAVAILABLE` does a `System.out.println`

The `InterruptedException` handling is not shown here. There are articles on how to do this properly. Google up on that.

## Suggestion

I recommend a sub-function, with a do-while loop (the following is a quick hack-up - untested):

```java
private static final HttpURLConnection getConnection(URL entries) throws InterruptedException{
    int retry = 0;
    boolean delay = false;
    do {
        if (delay) {
            Thread.sleep(RETRY_DELAY_MS);
        }
        HttpURLConnection connection = (HttpURLConnection)entries.openConnection();
        switch (connection.getResponseCode()) {
            case HttpURLConnection.HTTP_OK:
                log.fine(entries + " **OK**");
                return connection; // **EXIT POINT** fine, go on
            case HttpURLConnection.HTTP_GATEWAY_TIMEOUT:
                log.warning(entries + " **gateway timeout**");
                break;// retry
            case HttpURLConnection.HTTP_UNAVAILABLE:
                log.warning(entries + "**unavailable**");
                break;// retry, server is unstable
            default:
                log.severe(entries + " **unknown response code**.");
                break; // abort
        }
        // we did not succeed with connection (or we would have returned the connection).
        connection.disconnect();
        // retry
        retry++;
        log.warning("Failed retry " + retry + "/" + RETRIES);
        delay = true;

    } while (retry < RETRIES);

    log.severe("Aborting download of dataset.");

}
```



Two things to add:

1. I'd print that response code here to the log:

   > ```
   > log.severe(entries + " **unknown response code**.");
   > ```

   It would help debugging.

2. Retry seems a good idea first but one of the recent Java Posse episode ([#442 Roundup ‘13 - Big Data Bloopers](http://javaposse.com/java-posse-442)) has an interesting thought: This might not be that you really want. If there's a problem on the other side it might just makes the thing worse and it probably performs a DoS attack.



Working Solution

```java
public int callAPI() {
  return 1;
}

public int retrylogic() throws InterruptedException, IOException{
  int retry = 0;
  int status = -1;
  boolean delay = false;
  do {
    if (delay) {
      Thread.sleep(2000);
    }

    try {
      status = callAPI();
    }
    catch (Exception e) {
      System.out.println("Error occured");
      status = -1;
    }
    finally {
      switch (status) {
        case 200:
          System.out.println(" **OK**");
          return status; 
        default:
          System.out.println(" **unknown response code**.");
          break;
      }
      retry++;
      System.out.println("Failed retry " + retry + "/" + 3);
      delay = true;
    } 
  }while (retry < 3);

  return status;
}
```

