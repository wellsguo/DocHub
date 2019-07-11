
## [Android录音--AudioRecord、MediaRecorder (音频文件格式处理)](https://www.cnblogs.com/MMLoveMeMM/articles/3444718.html)
 

Android提供了两个API用于实现录音功能：android.media.AudioRecord、android.media.MediaRecorder。

网上有很多谈论这两个类的资料。现在大致总结下：

### 1、AudioRecord

主要是实现边录边播（AudioRecord+AudioTrack）以及对音频的实时处理（如会说话的汤姆猫、语音）

优点：语音的实时处理，可以用代码实现各种音频的封装

缺点：输出是PCM语音数据，如果保存成音频文件，是不能够被播放器播放的，所以必须先写代码实现数据编码以及压缩

> 示例：

使用AudioRecord类录音，并实现WAV格式封装。录音20s，输出的音频文件大概为3.5M左右（已写测试代码）

### 2、MediaRecorder

已经集成了录音、编码、压缩等，支持少量的录音音频格式，大概有.aac（API = 16） .amr .3gp

优点：大部分以及集成，直接调用相关接口即可，代码量小

缺点：无法实时处理音频；输出的音频格式不是很多，例如没有输出mp3格式文件

> 示例：

使用MediaRecorder类录音，输出amr格式文件。录音20s，输出的音频文件大概为33K（已写测试代码）

### 3、音频格式比较

WAV格式：录音质量高，但是压缩率小，文件大

AAC格式：相对于mp3，AAC格式的音质更佳，文件更小；有损压缩；一般苹果或者Android SDK4.1.2（API 16）及以上版本支持播放

AMR格式：压缩比比较大，但相对其他的压缩格式质量比较差，多用于人声，通话录音

至于常用的mp3格式，使用MediaRecorder没有该视频格式输出。一些人的做法是使用AudioRecord录音，然后编码成wav格式，再转换成mp3格式

 

再贴上一些测试工程。

功能描述：

1、点击“录音WAV文件”，开始录音。录音完成后，生成文件/sdcard/FinalAudio.wav

2、点击“录音AMR文件”，开始录音。录音完成后，生成文件/sdcard/FinalAudio.amr

3、点击“停止录音”，停止录音，并显示录音输出文件以及该文件大小。

 

大致代码如下：

## 1、AudioRecord录音，封装成WAV格式.

```java
package com.example.audiorecordtest; 
  
import java.io.File; 
import java.io.FileInputStream; 
import java.io.FileNotFoundException; 
import java.io.FileOutputStream; 
import java.io.IOException; 
  
import android.media.AudioFormat; 
import android.media.AudioRecord; 
  
public class AudioRecordFunc {  
    // 缓冲区字节大小   
    private int bufferSizeInBytes = 0; 
      
    //AudioName裸音频数据文件 ，麦克风 
    private String AudioName = "";   
      
    //NewAudioName可播放的音频文件   
    private String NewAudioName = ""; 
      
    private AudioRecord audioRecord;   
    private boolean isRecord = false;// 设置正在录制的状态   
      
      
    private static AudioRecordFunc mInstance;  
           
    private AudioRecordFunc(){ 
          
    }    
      
    public synchronized static AudioRecordFunc getInstance() 
    { 
        if(mInstance == null)  
            mInstance = new AudioRecordFunc();  
        return mInstance;  
    } 
      
    public int startRecordAndFile() { 
        //判断是否有外部存储设备sdcard 
        if(AudioFileFunc.isSdcardExit()) 
        { 
            if(isRecord) 
            { 
                return ErrorCode.E_STATE_RECODING; 
            } 
            else
            { 
                if(audioRecord == null) 
                    creatAudioRecord(); 
                  
                audioRecord.startRecording();   
                // 让录制状态为true   
                isRecord = true;   
                // 开启音频文件写入线程   
                new Thread(new AudioRecordThread()).start();   
                  
                return ErrorCode.SUCCESS; 
            } 
              
        }        
        else
        { 
            return ErrorCode.E_NOSDCARD;             
        }        
  
    }   
    
    public void stopRecordAndFile() {   
        close();   
    } 
      
      
    public long getRecordFileSize(){ 
        return AudioFileFunc.getFileSize(NewAudioName); 
    } 
      
    
    private void close() {   
        if (audioRecord != null) {   
            System.out.println("stopRecord");   
            isRecord = false;//停止文件写入   
            audioRecord.stop();   
            audioRecord.release();//释放资源   
            audioRecord = null;   
        }   
    } 
      
      
    private void creatAudioRecord() {   
        // 获取音频文件路径 
        AudioName = AudioFileFunc.getRawFilePath(); 
        NewAudioName = AudioFileFunc.getWavFilePath();  
          
        // 获得缓冲区字节大小   
        bufferSizeInBytes = AudioRecord.getMinBufferSize(AudioFileFunc.AUDIO_SAMPLE_RATE,   
                AudioFormat.CHANNEL_IN_STEREO, AudioFormat.ENCODING_PCM_16BIT);   
          
        // 创建AudioRecord对象   
        audioRecord = new AudioRecord(AudioFileFunc.AUDIO_INPUT, AudioFileFunc.AUDIO_SAMPLE_RATE,   
                AudioFormat.CHANNEL_IN_STEREO, AudioFormat.ENCODING_PCM_16BIT, bufferSizeInBytes);   
    } 
      
      
    class AudioRecordThread implements Runnable {   
        @Override  
        public void run() {   
            writeDateTOFile();//往文件中写入裸数据   
            copyWaveFile(AudioName, NewAudioName);//给裸数据加上头文件   
        }   
    }   
    
    /**  
     * 这里将数据写入文件，但是并不能播放，因为AudioRecord获得的音频是原始的裸音频，  
     * 如果需要播放就必须加入一些格式或者编码的头信息。但是这样的好处就是你可以对音频的 裸数据进行处理，比如你要做一个爱说话的TOM  
     * 猫在这里就进行音频的处理，然后重新封装 所以说这样得到的音频比较容易做一些音频的处理。  
     */  
    private void writeDateTOFile() {   
        // new一个byte数组用来存一些字节数据，大小为缓冲区大小   
        byte[] audiodata = new byte[bufferSizeInBytes];   
        FileOutputStream fos = null;   
        int readsize = 0;   
        try {   
            File file = new File(AudioName);   
            if (file.exists()) {   
                file.delete();   
            }   
            fos = new FileOutputStream(file);// 建立一个可存取字节的文件   
        } catch (Exception e) {   
            e.printStackTrace();   
        }   
        while (isRecord == true) {   
            readsize = audioRecord.read(audiodata, 0, bufferSizeInBytes);   
            if (AudioRecord.ERROR_INVALID_OPERATION != readsize && fos!=null) {   
                try {   
                    fos.write(audiodata);   
                } catch (IOException e) {   
                    e.printStackTrace();   
                }   
            }   
        }   
        try { 
            if(fos != null) 
                fos.close();// 关闭写入流   
        } catch (IOException e) {   
            e.printStackTrace();   
        }   
    }   
    
    // 这里得到可播放的音频文件   
    private void copyWaveFile(String inFilename, String outFilename) {   
        FileInputStream in = null;   
        FileOutputStream out = null;   
        long totalAudioLen = 0;   
        long totalDataLen = totalAudioLen + 36;   
        long longSampleRate = AudioFileFunc.AUDIO_SAMPLE_RATE;   
        int channels = 2;   
        long byteRate = 16 * AudioFileFunc.AUDIO_SAMPLE_RATE * channels / 8;   
        byte[] data = new byte[bufferSizeInBytes];   
        try {   
            in = new FileInputStream(inFilename);   
            out = new FileOutputStream(outFilename);   
            totalAudioLen = in.getChannel().size();   
            totalDataLen = totalAudioLen + 36;   
            WriteWaveFileHeader(out, totalAudioLen, totalDataLen,   
                    longSampleRate, channels, byteRate);   
            while (in.read(data) != -1) {   
                out.write(data);   
            }   
            in.close();   
            out.close();   
        } catch (FileNotFoundException e) {   
            e.printStackTrace();   
        } catch (IOException e) {   
            e.printStackTrace();   
        }   
    }   
    
    /**  
     * 这里提供一个头信息。插入这些信息就可以得到可以播放的文件。  
     * 为我为啥插入这44个字节，这个还真没深入研究，不过你随便打开一个wav  
     * 音频的文件，可以发现前面的头文件可以说基本一样哦。每种格式的文件都有  
     * 自己特有的头文件。  
     */  
    private void WriteWaveFileHeader(FileOutputStream out, long totalAudioLen,   
            long totalDataLen, long longSampleRate, int channels, long byteRate)   
            throws IOException {   
        byte[] header = new byte[44];   
        header[0] = 'R'; // RIFF/WAVE header   
        header[1] = 'I';   
        header[2] = 'F';   
        header[3] = 'F';   
        header[4] = (byte) (totalDataLen & 0xff);   
        header[5] = (byte) ((totalDataLen >> 8) & 0xff);   
        header[6] = (byte) ((totalDataLen >> 16) & 0xff);   
        header[7] = (byte) ((totalDataLen >> 24) & 0xff);   
        header[8] = 'W';   
        header[9] = 'A';   
        header[10] = 'V';   
        header[11] = 'E';   
        header[12] = 'f'; // 'fmt ' chunk   
        header[13] = 'm';   
        header[14] = 't';   
        header[15] = ' ';   
        header[16] = 16; // 4 bytes: size of 'fmt ' chunk   
        header[17] = 0;   
        header[18] = 0;   
        header[19] = 0;   
        header[20] = 1; // format = 1   
        header[21] = 0;   
        header[22] = (byte) channels;   
        header[23] = 0;   
        header[24] = (byte) (longSampleRate & 0xff);   
        header[25] = (byte) ((longSampleRate >> 8) & 0xff);   
        header[26] = (byte) ((longSampleRate >> 16) & 0xff);   
        header[27] = (byte) ((longSampleRate >> 24) & 0xff);   
        header[28] = (byte) (byteRate & 0xff);   
        header[29] = (byte) ((byteRate >> 8) & 0xff);   
        header[30] = (byte) ((byteRate >> 16) & 0xff);   
        header[31] = (byte) ((byteRate >> 24) & 0xff);   
        header[32] = (byte) (2 * 16 / 8); // block align   
        header[33] = 0;   
        header[34] = 16; // bits per sample   
        header[35] = 0;   
        header[36] = 'd';   
        header[37] = 'a';   
        header[38] = 't';   
        header[39] = 'a';   
        header[40] = (byte) (totalAudioLen & 0xff);   
        header[41] = (byte) ((totalAudioLen >> 8) & 0xff);   
        header[42] = (byte) ((totalAudioLen >> 16) & 0xff);   
        header[43] = (byte) ((totalAudioLen >> 24) & 0xff);   
        out.write(header, 0, 44);   
    }   
} 
```

## 2、MediaRecorder录音，输出amr格式音频

```java
package com.example.audiorecordtest; 
  
import java.io.File; 
import java.io.IOException; 
  
import android.media.MediaRecorder; 
  
public class MediaRecordFunc {   
    private boolean isRecord = false; 
      
    private MediaRecorder mMediaRecorder; 
    private MediaRecordFunc(){ 
    } 
      
    private static MediaRecordFunc mInstance; 
    public synchronized static MediaRecordFunc getInstance(){ 
        if(mInstance == null) 
            mInstance = new MediaRecordFunc(); 
        return mInstance; 
    } 
      
    public int startRecordAndFile(){ 
        //判断是否有外部存储设备sdcard 
        if(AudioFileFunc.isSdcardExit()) 
        { 
            if(isRecord) 
            { 
                return ErrorCode.E_STATE_RECODING; 
            } 
            else
            { 
                if(mMediaRecorder == null) 
                    createMediaRecord(); 
                  
                try{ 
                    mMediaRecorder.prepare(); 
                    mMediaRecorder.start(); 
                    // 让录制状态为true   
                    isRecord = true; 
                    return ErrorCode.SUCCESS; 
                }catch(IOException ex){ 
                    ex.printStackTrace(); 
                    return ErrorCode.E_UNKOWN; 
                } 
            } 
              
        }        
        else
        { 
            return ErrorCode.E_NOSDCARD;             
        }        
    } 
      
      
    public void stopRecordAndFile(){ 
         close(); 
    } 
      
    public long getRecordFileSize(){ 
        return AudioFileFunc.getFileSize(AudioFileFunc.getAMRFilePath()); 
    } 
      
      
    private void createMediaRecord(){ 
         /* ①Initial：实例化MediaRecorder对象 */
        mMediaRecorder = new MediaRecorder(); 
          
        /* setAudioSource/setVedioSource*/
        mMediaRecorder.setAudioSource(AudioFileFunc.AUDIO_INPUT);//设置麦克风 
          
        /* 设置输出文件的格式：THREE_GPP/MPEG-4/RAW_AMR/Default 
         * THREE_GPP(3gp格式，H263视频/ARM音频编码)、MPEG-4、RAW_AMR(只支持音频且音频编码要求为AMR_NB) 
         */
         mMediaRecorder.setOutputFormat(MediaRecorder.OutputFormat.DEFAULT); 
           
         /* 设置音频文件的编码：AAC/AMR_NB/AMR_MB/Default */
         mMediaRecorder.setAudioEncoder(MediaRecorder.AudioEncoder.DEFAULT); 
           
         /* 设置输出文件的路径 */
         File file = new File(AudioFileFunc.getAMRFilePath()); 
         if (file.exists()) {   
             file.delete();   
         }  
         mMediaRecorder.setOutputFile(AudioFileFunc.getAMRFilePath()); 
    } 
      
      
    private void close(){ 
        if (mMediaRecorder != null) {   
            System.out.println("stopRecord");   
            isRecord = false; 
            mMediaRecorder.stop();   
            mMediaRecorder.release();   
            mMediaRecorder = null; 
        }   
    } 
}
```

## 3、其他文件

> AudioFileFunc.java

```java
package com.example.audiorecordtest; 
  
import java.io.File; 
  
import android.media.MediaRecorder; 
import android.os.Environment; 
  
public class AudioFileFunc { 
    //音频输入-麦克风 
    public final static int AUDIO_INPUT = MediaRecorder.AudioSource.MIC; 
      
    //采用频率 
    //44100是目前的标准，但是某些设备仍然支持22050，16000，11025 
    public final static int AUDIO_SAMPLE_RATE = 44100;  //44.1KHz,普遍使用的频率    
    //录音输出文件 
    private final static String AUDIO_RAW_FILENAME = "RawAudio.raw"; 
    private final static String AUDIO_WAV_FILENAME = "FinalAudio.wav"; 
    public final static String AUDIO_AMR_FILENAME = "FinalAudio.amr"; 
      
    /** 
     * 判断是否有外部存储设备sdcard 
     * @return true | false 
     */
    public static boolean isSdcardExit(){        
        if (Environment.getExternalStorageState().equals(android.os.Environment.MEDIA_MOUNTED)) 
            return true; 
        else
            return false; 
    } 
          
    /** 
     * 获取麦克风输入的原始音频流文件路径 
     * @return 
     */
    public static String getRawFilePath(){ 
        String mAudioRawPath = ""; 
        if(isSdcardExit()){ 
            String fileBasePath = Environment.getExternalStorageDirectory().getAbsolutePath(); 
            mAudioRawPath = fileBasePath+"/"+AUDIO_RAW_FILENAME; 
        }    
          
        return mAudioRawPath; 
    } 
      
    /** 
     * 获取编码后的WAV格式音频文件路径 
     * @return 
     */
    public static String getWavFilePath(){ 
        String mAudioWavPath = ""; 
        if(isSdcardExit()){ 
            String fileBasePath = Environment.getExternalStorageDirectory().getAbsolutePath(); 
            mAudioWavPath = fileBasePath+"/"+AUDIO_WAV_FILENAME; 
        } 
        return mAudioWavPath; 
    } 
      
      
    /** 
     * 获取编码后的AMR格式音频文件路径 
     * @return 
     */
    public static String getAMRFilePath(){ 
        String mAudioAMRPath = ""; 
        if(isSdcardExit()){ 
            String fileBasePath = Environment.getExternalStorageDirectory().getAbsolutePath(); 
            mAudioAMRPath = fileBasePath+"/"+AUDIO_AMR_FILENAME; 
        } 
        return mAudioAMRPath; 
    }    
      
      
    /** 
     * 获取文件大小 
     * @param path,文件的绝对路径 
     * @return 
     */
    public static long getFileSize(String path){ 
        File mFile = new File(path); 
        if(!mFile.exists()) 
            return -1; 
        return mFile.length(); 
    } 
  
} 
```

## 4、其他文件

> ErrorCode.java

```JAVA
package com.example.audiorecordtest; 
  
import android.content.Context; 
import android.content.res.Resources.NotFoundException; 
  
public class ErrorCode { 
    public final static int SUCCESS = 1000; 
    public final static int E_NOSDCARD = 1001; 
    public final static int E_STATE_RECODING = 1002; 
    public final static int E_UNKOWN = 1003; 
      
      
    public static String getErrorInfo(Context vContext, int vType) throws NotFoundException 
    { 
        switch(vType) 
        { 
        case SUCCESS: 
            return "success"; 
        case E_NOSDCARD: 
            return vContext.getResources().getString(R.string.error_no_sdcard); 
        case E_STATE_RECODING: 
            return vContext.getResources().getString(R.string.error_state_record);   
        case E_UNKOWN: 
        default: 
            return vContext.getResources().getString(R.string.error_unknown);            
              
        } 
    } 
  
} 
```

## 5、string.xml

```XML
<?xml version="1.0" encoding="utf-8"?>
<resources>

    <string name="app_name">AudioRecordTest</string>
    <string name="hello_world">测试AudioRecord，实现录音功能</string>
    <string name="menu_settings">Settings</string>
    <string name="view_record_wav">录音WAV文件</string>
    <string name="view_record_amr">录音AMR文件</string>
    <string name="view_stop">停止录音</string>
    
    <string name="error_no_sdcard">没有SD卡，无法存储录音数据</string>
    <string name="error_state_record">正在录音中，请先停止录音</string>
    <string name="error_unknown">无法识别的错误</string>

</resources> 
```

## 6、主程序MainActivity 

```java
package com.example.audiorecordtest; 

import android.app.Activity;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.util.Log;
import android.view.Menu;
import android.view.View;
import android.widget.Button;
import android.widget.TextView; 

public class MainActivity extends Activity {
    private final static int FLAG_WAV = 0;
    private final static int FLAG_AMR = 1;
    private int mState = -1;    //-1:没再录制，0：录制wav，1：录制amr
    private Button btn_record_wav;
    private Button btn_record_amr;
    private Button btn_stop;
    private TextView txt;
    private UIHandler uiHandler;
    private UIThread uiThread; 

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        findViewByIds();
        setListeners();
        init();
    } 

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.activity_main, menu);
        return true;
    }
    private void findViewByIds(){
        btn_record_wav = (Button)this.findViewById(R.id.btn_record_wav);
        btn_record_amr = (Button)this.findViewById(R.id.btn_record_amr);
        btn_stop = (Button)this.findViewById(R.id.btn_stop);
        txt = (TextView)this.findViewById(R.id.text);
    }
    private void setListeners(){
        btn_record_wav.setOnClickListener(btn_record_wav_clickListener);
        btn_record_amr.setOnClickListener(btn_record_amr_clickListener);
        btn_stop.setOnClickListener(btn_stop_clickListener);
    }
    private void init(){
        uiHandler = new UIHandler();        
    }
    private Button.OnClickListener btn_record_wav_clickListener = new Button.OnClickListener(){
        public void onClick(View v){
            record(FLAG_WAV);
        }
    };
    private Button.OnClickListener btn_record_amr_clickListener = new Button.OnClickListener(){
        public void onClick(View v){
            record(FLAG_AMR);
        }
    };
    private Button.OnClickListener btn_stop_clickListener = new Button.OnClickListener(){
        public void onClick(View v){
            stop();     
        }
    };
    /**
     * 开始录音
     * @param mFlag，0：录制wav格式，1：录音amr格式
     */
    private void record(int mFlag){
        if(mState != -1){
            Message msg = new Message();
            Bundle b = new Bundle();// 存放数据
            b.putInt("cmd",CMD_RECORDFAIL);
            b.putInt("msg", ErrorCode.E_STATE_RECODING);
            msg.setData(b); 

            uiHandler.sendMessage(msg); // 向Handler发送消息,更新UI
            return;
        } 
        int mResult = -1;
        switch(mFlag){        
        case FLAG_WAV:
            AudioRecordFunc mRecord_1 = AudioRecordFunc.getInstance();
            mResult = mRecord_1.startRecordAndFile();            
            break;
        case FLAG_AMR:
            MediaRecordFunc mRecord_2 = MediaRecordFunc.getInstance();
            mResult = mRecord_2.startRecordAndFile();
            break;
        }
        if(mResult == ErrorCode.SUCCESS){
            uiThread = new UIThread();
            new Thread(uiThread).start();
            mState = mFlag;
        }else{
            Message msg = new Message();
            Bundle b = new Bundle();// 存放数据
            b.putInt("cmd",CMD_RECORDFAIL);
            b.putInt("msg", mResult);
            msg.setData(b); 

            uiHandler.sendMessage(msg); // 向Handler发送消息,更新UI
        }
    }
    /**
     * 停止录音
     */
    private void stop(){
        if(mState != -1){
            switch(mState){
            case FLAG_WAV:
                AudioRecordFunc mRecord_1 = AudioRecordFunc.getInstance();
                mRecord_1.stopRecordAndFile();
                break;
            case FLAG_AMR:
                MediaRecordFunc mRecord_2 = MediaRecordFunc.getInstance();
                mRecord_2.stopRecordAndFile();
                break;
            }            
            if(uiThread != null){
                uiThread.stopThread();
            }
            if(uiHandler != null)
                uiHandler.removeCallbacks(uiThread); 
            Message msg = new Message();
            Bundle b = new Bundle();// 存放数据
            b.putInt("cmd",CMD_STOP);
            b.putInt("msg", mState);
            msg.setData(b);
            uiHandler.sendMessageDelayed(msg,1000); // 向Handler发送消息,更新UI 
            mState = -1;
        }
    }    
    private final static int CMD_RECORDING_TIME = 2000;
    private final static int CMD_RECORDFAIL = 2001;
    private final static int CMD_STOP = 2002;
    class UIHandler extends Handler{
        public UIHandler() {
        }
        @Override
        public void handleMessage(Message msg) {
            // TODO Auto-generated method stub
            Log.d("MyHandler", "handleMessage......");
            super.handleMessage(msg);
            Bundle b = msg.getData();
            int vCmd = b.getInt("cmd");
            switch(vCmd)
            {
            case CMD_RECORDING_TIME:
                int vTime = b.getInt("msg");
                MainActivity.this.txt.setText("正在录音中，已录制："+vTime+" s");
                break;
            case CMD_RECORDFAIL:
                int vErrorCode = b.getInt("msg");
                String vMsg = ErrorCode.getErrorInfo(MainActivity.this, vErrorCode);
                MainActivity.this.txt.setText("录音失败："+vMsg);
                break;
            case CMD_STOP:                
                int vFileType = b.getInt("msg");
                switch(vFileType){
                case FLAG_WAV:
                    AudioRecordFunc mRecord_1 = AudioRecordFunc.getInstance(); 
                    long mSize = mRecord_1.getRecordFileSize();
                    MainActivity.this.txt.setText("录音已停止.录音文件:"+AudioFileFunc.getWavFilePath()+"\n文件大小："+mSize);
                    break;
                case FLAG_AMR:                    
                    MediaRecordFunc mRecord_2 = MediaRecordFunc.getInstance();
                    mSize = mRecord_2.getRecordFileSize();
                    MainActivity.this.txt.setText("录音已停止.录音文件:"+AudioFileFunc.getAMRFilePath()+"\n文件大小："+mSize);
                    break;
                }
                break;
            default:
                break;
            }
        }
    };
    class UIThread implements Runnable {        
        int mTimeMill = 0;
        boolean vRun = true;
        public void stopThread(){
            vRun = false;
        }
        public void run() {
            while(vRun){
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                }
                mTimeMill ++;
                Log.d("thread", "mThread........"+mTimeMill);
                Message msg = new Message();
                Bundle b = new Bundle();// 存放数据
                b.putInt("cmd",CMD_RECORDING_TIME);
                b.putInt("msg", mTimeMill);
                msg.setData(b); 

                MainActivity.this.uiHandler.sendMessage(msg); // 向Handler发送消息,更新UI
            } 

        }
    } 

}
```
 

 

http://www.cnblogs.com/Amandaliu/archive/2013/02/04/2891604.html