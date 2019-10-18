
     
主要资料来源： 百度文库的《JNI常用函数》 


   

 

要素  ：
1、 该函数大全是基于C语言方式的，对于 C++ 方式可以直接转换 ，例如，对于生成一个jstring类型的方法转换分别如下：
- C编程环境中使用方法为：`(*env) ->NewStringUTF(env , "123") `;
- C++编程环境中（例如，VC下）则是： `env ->NewStringUTF( "123")` ;             (使用起来更简单)

 

2、关于下列有些函数中：*isCopy 的说明，例如，如下函数：                     

> const char* GetStringUTFChars(JNIEnv \*env, jstring string, jboolean \*isCopy);  

对第三个参数 jboolean \*isCopy说明如下：

当从JNI函数GetStringUTFChars函数中返回得到字符串B时，如果B是原始字符串java.lang.String的一份拷贝，
则isCopy  被赋值为JNI_TRUE。如果B是和原始字符串指向的是JVM中的同一份数据，则isCopy  被赋值为JNI_FALSE。
当isCopy  为JNI_FALSE时，本地代码绝不能修改字符串的内容，否则JVM中的原始字符串也会被修改，这会打破Java语言
中字符串不可变的规则。

通常，我们不必关心JVM是否会返回原始字符串的拷贝，只需要为isCopy传递NULL作为参数 。

  ----     以上内容来自 《JNI编程指南》

 

## 一、类操作             


 > jclass DefineClass (JNIEnv *env, jobject loader,   const jbyte *buf , jsize bufLen);                 

     功能：从原始类数据的缓冲区中加载类。             

     参数： env        JNI 接口指针。            

           loader    分派给所定义的类的类加载器。          

           buf        包含 .class 文件数据的缓冲区。               

           bufLen  缓冲区长度。          

     返回值：返回 Java 类对象。如果出错则返回NULL。            

     抛出： ClassFormatError      如果类数据指定的类无效。                 

           ClassCircularityError  如果类或接口是自身的超类或超接口。               

           OutOfMemoryError  如果系统内存不足。                  

                        

>   jclass FindClass (JNIEnv \*env, const char \*name);                

     功能: 该函数用于加载本地定义的类。它将搜索由CLASSPATH 环境变量为具有指定名称的类所指定的目录和 zip文件。            

     参数：env    JNI 接口指针。            

          name  类全名（即包名后跟类名，之间由"/"分隔）.如果该名称以“[（数组签名字符）打头，则返回一个数组类。         

     返回值：返回类对象全名。如果找不到该类，则返回 NULL。               

     抛出：   ClassFormatError          如果类数据指定的类无效。                 

             ClassCircularityError      如果类或接口是自身的超类或超接口。                

             NoClassDefFoundError  如果找不到所请求的类或接口的定义。            

             OutOfMemoryError       如果系统内存不足。                  

 

>  jclass GetObjectClass (JNIEnv *env, jobject obj); 

     功能：通过对象获取这个类。该函数比较简单，唯一注意的是对象不能为NULL，否则获取的class肯定返回也为NULL。     

     参数：  env   JNI 接口指针。            

            obj   Java 类对象实例。         

   

>  jclass GetSuperclass (JNIEnv *env, jclass clazz);          

     功能：获取父类或者说超类 。 如果 clazz 代表类class而非类 object，则该函数返回由 clazz 所指定的类的超类。 如果 clazz 

           指定类 object 或代表某个接口，则该函数返回NULL。           

     参数：  env   JNI 接口指针。            

                clazz  Java 类对象。            

     返回值：    由 clazz 所代表的类的超类或 NULL。               

                          

>  jboolean IsAssignableFrom (JNIEnv *env, jclass clazz1,  jclass clazz2);           

    功能：确定 clazz1 的对象是否可安全地强制转换为clazz2。            

    参数：  env  JNI 接口指针。            

              clazz1 第一个类参数。               

              clazz2 第二个类参数。               

    返回值：  下列某个情况为真时返回 JNI_TRUE：               

                    1、 第一及第二个类参数引用同一个 Java 类。              

                    2、 第一个类是第二个类的子类。             

                    3、 第二个类是第一个类的某个接口。    

 

         

## 二、异常操作                  

                        

>  jint  Throw(JNIEnv *env, jthrowable obj);         

      功能：抛出 java.lang.Throwable 对象。                 

       参数： env  JNI 接口指针。            

                 obj   java.lang.Throwable 对象。         

       返回值：  成功时返回 0，失败时返回负数。             

       抛出：    java.lang.Throwable 对象 obj。           

                

>  jint ThrowNew (JNIEnv *env ,  jclass clazz,  const char *message);            

     功能：利用指定类的消息（由 message 指定）构造异常对象并抛出该异常。               

     参数： env    JNI 接口指针。            

                clazz  java.lang.Throwable 的子类。          

                message  用于构造java.lang.Throwable对象的消息。           

     返回值： 成功时返回 0，失败时返回负数。             

     抛出：  新构造的 java.lang.Throwable 对象。                 

                   

>  jthrowable ExceptionOccurred (JNIEnv *env);              

    功能：确定是否某个异常正被抛出。在平台相关代码调用 ExceptionClear() 或 Java 代码处理该异常前，异常将始终保持

        抛出状态。                  

    参数：  env  JNI 接口指针。            

    返回值： 返回正被抛出的异常对象，如果当前无异常被抛出，则返回NULL。           

                      

> void ExceptionDescribe (JNIEnv *env);         

    功能：将异常及堆栈的回溯输出到系统错误报告信道（例如 stderr）。该例程可便利调试操作。               

    参数：env   JNI 接口指针。            

                    

>  void ExceptionClear (JNIEnv *env);                

   功能：清除当前抛出的任何异常。如果当前无异常，则此例程不产生任何效果。                  

   参数： env   JNI 接口指针。            

                  

>  void FatalError (JNIEnv *env, const char *msg);           

```
功能：抛出致命错误并且不希望虚拟机进行修复。该函数无返回值。             

参数：  env   JNI 接口指针。            

       msg   错误消息。          
```
            

     

 

## 三、全局及局部引用             

                      

 >  jobject NewGlobalRef (JNIEnv *env, jobject obj);         

     功能：创建 obj 参数所引用对象的新全局引用。obj 参数既可以是全局引用，也可以是局部引用。全局引用通过调用 

          DeleteGlobalRef() 来显式撤消。          

     参数：env   JNI 接口指针。            

                obj    全局或局部引用。                 

     返回值： 返回全局引用。如果系统内存不足则返回 NULL。          

                      

>  void DeleteGlobalRef (JNIEnv *env, jobject globalRef);                 

     功能： 删除 globalRef 所指向的全局引用。         

     参数： env    JNI 接口指针。            

                globalRef  全局引用。         

                              

>  void  DeleteLocalRef (JNIEnv *env, jobject localRef);          

     功能： 删除 localRef所指向的局部引用。             

     参数： env   JNI 接口指针。            

                 localRef  局部引用。            

             

    

 

## 四、对象操作          

          

>  jobject AllocObject (JNIEnv *env, jclass clazz);              

     功能：分配新 Java 对象而不调用该对象的任何构造函数。返回该对象的引用。clazz 参数务必不要引用数组类。               

     参数： env  JNI 接口指针。            

               clazz  Java 类对象。            

     返回值： 返回 Java 对象。如果无法构造该对象，则返回NULL。                 

     抛出： InstantiationException：如果该类为一个接口或抽象类。                 

                OutOfMemoryError：如果系统内存不足。                  

                        

>  jobject NewObject (JNIEnv *env ,  jclass clazz,  jmethodID methodID, ...);   //参数附加在函数后面             

>  jobject NewObjectA (JNIEnv *env , jclassclazz,  jmethodID methodID, jvalue *args);    //参数以指针形式附加           

>  jobject NewObjectV (JNIEnv *env , jclassclazz,  jmethodID methodID, va_list args);    //参数以"链表"形式附加            



    功能：构造新 Java 对象。方法 ID指示应调用的构造函数方法。注意：该 ID特指该类class的构造函数ID ， 必须通过调用 

        GetMethodID() 获得，且调用时的方法名必须为 <init>，而返回类型必须为 void (V)。clazz参数务必不要引用数组类。 

     参数：  env  JNI 接口指针。            

            clazz  Java 类对象。            

            methodID 构造函数的方法 ID。               

      NewObject 的其它参数：  传给构造函数的参数，可以为空 。                  

      NewObjectA 的其它参数： args：传给构造函数的参数数组。              

      NewObjectV 的其它参数： args：传给构造函数的参数 va_list。       

           

      返回值： 返回 Java 对象，如果无法构造该对象，则返回NULL。                 

      抛出：   InstantiationException  如果该类为接口或抽象类。                 

              OutOfMemoryError   如果系统内存不足。                  

              构造函数抛出的任何异常。                  

                               

>  jclass GetObjectClass (JNIEnv *env, jobject obj);         

    功能：返回对象的类。             

    参数： env  JNI 接口指针。            

          obj  Java 对象（不能为 NULL）。               

    返回值： 返回 Java 类对象。              

                          

>  jboolean IsInstanceOf (JNIEnv *env, jobject obj, jclass clazz);             

```
功能：测试对象是否为某个类的实例。                  

参数：  env  JNI 接口指针。            

       obj  Java 对象。           

       clazz Java 类对象。            

返回值：如果可将 obj 强制转换为 clazz，则返回 JNI_TRUE。否则返回 JNI_FALSE。NULL 对象可强制转换为任何类。           
```
                           

>  jbooleanIsSameObject (JNIEnv *env, jobjectref1, jobject ref2);            

    功能：测试两个引用是否引用同一 Java 对象。         

    参数：  env  JNI 接口指针。            

               ref1  Java 对象。                  

               ref2   Java 对象。                  

    返回值： 如果 ref1 和 ref2 引用同一 Java 对象或均为 NULL，则返回 JNI_TRUE。否则返回 JNI_FALSE。         



    

                  

## 五、 字符串操作             

                                 

>  jstring  NewString (JNIEnv *env, const jchar *unicodeChars,   jsize len);         

    功能：利用 Unicode 字符数组构造新的 java.lang.String 对象。               

    参数：   env：JNI 接口指针。            

                 unicodeChars：指向 Unicode 字符串的指针。         

                 len：Unicode 字符串的长度。             

    返回值： Java 字符串对象。如果无法构造该字符串，则为NULL。             

    抛出： OutOfMemoryError：如果系统内存不足。                  

                              

>  jsize  GetStringLength (JNIEnv *env, jstring string);            

    功能：返回 Java 字符串的长度（Unicode 字符数）。                 

    参数：  env：JNI 接口指针。            

                string：Java 字符串对象。          

    返回值： Java 字符串的长度。            

                              

>  const  jchar *  GetStringChars (JNIEnv*env, jstring string,  jboolean *isCopy);           

   功能：返回指向字符串的 Unicode 字符数组的指针。该指针在调用 ReleaseStringchars() 前一直有效。          

         如果 isCopy 非空，则在复制完成后将 *isCopy 设为 JNI_TRUE。如果没有复制，则设为JNI_FALSE。  

   参数：   env：JNI 接口指针。            

                string：Java 字符串对象。          

                isCopy：指向布尔值的指针。               

   返回值：   指向 Unicode 字符串的指针，如果操作失败，则返回NULL。               

                                    

>  void  ReleaseStringChars (JNIEnv *env, jstring string,  const jchar *chars);                  

   功能：通知虚拟机平台相关代码无需再访问 chars。参数chars 是一个指针，可通过 GetStringChars() 从 string 获得。    

   参数： env：JNI 接口指针。            

              string：Java 字符串对象。          

              chars：指向 Unicode 字符串的指针。               

                        

>  jstring  NewStringUTF (JNIEnv *env, const char *bytes);            

   功能：利用 UTF-8 字符数组构造新 java.lang.String 对象。               

   参数： env：JNI 接口指针。如果无法构造该字符串，则为 NULL。         

              bytes：指向 UTF-8 字符串的指针。          

   返回值：Java 字符串对象。如果无法构造该字符串，则为NULL。             

   抛出：  OutOfMemoryError：如果系统内存不足。                  

                            

>  jsize  GetStringUTFLength (JNIEnv *env, jstring string);              

   功能：以字节为单位返回字符串的 UTF-8 长度。                

   参数：   env：JNI 接口指针。            

               string：Java 字符串对象。          

   返回值：  返回字符串的 UTF-8



>  const char* GetStringUTFChars (JNIEnv*env, jstring string, jboolean *isCopy);           

   功能：返回指向字符串的 UTF-8 字符数组的指针。该数组在被ReleaseStringUTFChars() 释放前将一直有效。    如果 isCopy 

      不是 NULL，*isCopy 在复制完成后即被设为 JNI_TRUE。如果未复制，则设为 JNI_FALSE。             

   参数：  env：JNI 接口指针。            

              string：Java 字符串对象。          

              isCopy：指向布尔值的指针。               

   返回值：  指向 UTF-8 字符串的指针。如果操作失败，则为 NULL。             

                            

>  void  ReleaseStringUTFChars (JNIEnv *env, jstring string,  const char *utf);               

   功能：通知虚拟机平台相关代码无需再访问 utf。utf 参数是一个指针，可利用 GetStringUTFChars() 获得。                  

   参数：   env：JNI 接口指针。            

               string：Java 字符串对象。          

               utf：指向 UTF-8 字符串的指针。               

 

         

## 六、数组操作                          



> jsize GetArrayLength (JNIEnv *env, jarray array);                 

   功能：返回数组中的元素数。                  

   参数：  env：JNI 接口指针。            

              array：Java 数组对象。                

   返回值： 数组的长度。                  

                             

> jarray NewObjectArray (JNIEnv *env, jsize length,  jclass elementClass, jobject initialElement);           

   功能：构造新的数组，它将保存类 elementClass 中的对象。所有元素初始值均设为 initialElement。               

   参数： env：JNI 接口指针。            

             length：数组大小。               

             elementClass：数组元素类。               

             initialElement：初始值。    可以为NULL 。           

   返回值：Java 数组对象。如果无法构造数组，则为 NULL。                  

   抛出：  OutOfMemoryError：如果系统内存不足。                  

   

   说明： 使用该函数时，为了便于易操作性，我们一般可以用jobjectArray数组类型或得返回值，例如：

                 jobjectArray objArray = env->NewObjectArray ( );

                 //操作该对象

                 env->GetObjectArrayElement (objArray, 0);//获得该object数组在索引0处的值 ,(可以强制转换类型).



> jobject  GetObjectArrayElement (JNIEnv *env,   jobjectArray array, jsize index);                

   功能：返回 Object 数组的元素。          

   参数：   env：JNI 接口指针。            

                array：Java 数组。                

                index：数组下标。                 

   返回值： Java 对象。            

   抛出： ArrayIndexOutOfBoundsException：如果 index 不是数组中的有效下标。             

                  

>  void  SetObjectArrayElement (JNIEnv *env, jobjectArray array,  jsize index, jobject value);                

   功能：设置 Object 数组的元素。          

   参数：  env：JNI 接口指针。            

              array：Java 数组。                

               index：数组下标。                 

               value：新值。                 

   抛出： ArrayIndexOutOfBoundsException：如果 index 不是数组中的有效下标。             

              ArrayStoreException：如果 value 的类不是数组元素类的子类。           

                      


###    New<PrimitiveType>Array方法类型      

         

 > NativeType New<PrimitiveType>Array (JNIEnv *env, ArrayType array, jboolean*isCopy);                  

 

     说明： 用于构造新基本类型数组对象的一系列操作。下表说明了特定的基本类型数组构造函数。用户应把

    New<PrimitiveType>Array 替换为某个实际的基本类型数组构造函数例程名（见下表），然后将 ArrayType替换为

　该例程相应的数组类型。

     参数：  env ： JNI 接口指针。            

                 length：数组长度。               

     返回值：  Java 数组。如果无法构造该数组，则为 NULL。

       　    

            New<PrimitiveType>Array 方法组               数组类型        

                  NewBooleanArray()                            jbooleanArray 

                  NewByteArray()                                  jbyteArray       

                  NewCharArray()                                 jcharArray       

                  NewShortArray()                                jshortArray      

                  NewIntArray()                                    jintArray 

                  NewLongArray()                                 jlongArray        

                  NewFloatArray()                                 jfloatArray       

                  NewDoubleArray()                             jdoubleArray   

                 

                  

### Get<PrimitiveType>ArrayElements 方法类型       

 

>  NativeType *Get<PrimitiveType>ArrayElements (JNIEnv *env, ArrayType array, jboolean*isCopy);                  

   说明：一组返回基本类型数组体的函数。结果在调用相应的 Release<PrimitiveType>ArrayElements()函数前将一直有效。

     由于返回的数组可能是 Java 数组的副本，因此对返回数组的更改不必在基本类型数组中反映出来，直到调用了

     Release<PrimitiveType>ArrayElements()。 如果 isCopy 不是 NULL，*isCopy 在复制完成后即被设为 JNI_TRUE。如果

     未复制，则设为 JNI_FALSE。          

 　　 使用说明：   

   　　　   将 Get<PrimitiveType>ArrayElements 替换为表中某个实际的基本类型元素访问器例程名。             

      　　　将 ArrayType 替换为对应的数组类型。             

      　　　将 NativeType 替换为该例程对应的本地类型。               

    参数：   env：JNI 接口指针。            

                array：Java 字符串对象。           

                isCopy：指向布尔值的指针。               

    返回值：    返回指向数组元素的指针，如果操作失败，则为 NULL。          

             

     不管布尔数组在 Java 虚拟机中如何表示，GetBooleanArrayElements() 将始终返回一个 jbooleans 类型的指针，其中每一

　字节代表一个元素（开包表示）。内存中将确保所有其它类型。

      　     　

            Get<PrimitiveType>ArrayElements 例程         数组类型                  本地类型

                  GetBooleanArrayElements()                   jbooleanArray            jboolean

                  GetByteArrayElements()                         jbyteArray                  jbyte

                  GetCharArrayElements()                        jcharArray                  jchar

                  GetShortArrayElements()                       jshortArray                 jshort

                  GetIntArrayElements()                           jintArray                     jint

                  GetLongArrayElements()                        jlongArray                  jlong

                  GetFloatArrayElements()                        jfloatArray                  jfloat

                  GetDoubleArrayElements()                     jdoubleArray              jdouble

      

                  

###   Release<PrimitiveType>ArrayElements 方法类型                

 

>  void  Release<PrimitiveType>ArrayElements (JNIEnv *env, ArrayType array, NativeType *elems,jint mode);            

     功能：通知虚拟机平台相关代码无需再访问 elems 的一组函数。elems 参数是一个通过使用对应的

        Get<PrimitiveType>ArrayElements() 函数由 array 导出的指针。必要时，该函数将把对 elems 的修改复制回基本

        类型数组。mode参数将提供有关如何释放数组缓冲区的信息。如果elems 不是 array 中数组元素的副本，mode将无效。

        否则，mode 将具有下表所述的功能：             

                        模式                                         动作        

                         0                            复制回内容并释放elems 缓冲区      

                   JNI_COMMIT               复制回内容但不释放elems 缓冲区  

                   JNI_ABORT                   释放缓冲区但不复制回变化        

       多数情况下，编程人员将把“0”传给 mode 参数以确保固定的数组和复制的数组保持一致。其它选项可以使编程人员进一步

   控制内存管理，但使用时务必慎重。             

     使用说明：

         将 ArrayType 替换为对应的数组类型。             

         将 NativeType 替换为该例程对应的本地类型。               

    

   参数： env：JNI 接口指针。            

             array：Java 数组对象。                

             elems：指向数组元素的指针。           

             mode：释放模式。      

 

         Release<PrimitiveType>ArrayElements 方法组         数组类型             本地类型

              ReleaseBooleanArrayElements()                      jbooleanArray       jboolean

              ReleaseByteArrayElements()                           jbyteArray              jbyte

              ReleaseCharArrayElements()                          jcharArray              jchar

              ReleaseShortArrayElements()                         jshortArray             jshort

              ReleaseIntArrayElements()                             jintArray                 jint

              ReleaseLongArrayElements()                       jlongArray             jlong

              ReleaseFloatArrayElements()                       jfloatArray            jfloat

              ReleaseDoubleArrayElements()                   jdoubleArray         jdouble

          

                  

###    Get<PrimitiveType>ArrayRegion 方法类型          

 

>  void  Get<PrimitiveType>ArrayRegion (JNIEnv *env, ArrayType array,  jsize start, jsize len, NativeType *buf);            

    功能：将基本类型数组某一区域复制到缓冲区中的一组函数。                    

      使用说明：        

               将 Get<PrimitiveType>ArrayRegion 替换为下表的某个实际基本类型元素访问器例程名。

               将 ArrayType 替换为对应的数组类型。             

               将 NativeType 替换为该例程对应的本地类型。     

   参数：     env：JNI 接口指针。            

                 array：Java 指针。                

                 start：起始下标。                  

                 len：要复制的元素数。                 

                 buf：目的缓冲区。                

   抛出：  ArrayIndexOutOfBoundsException：如果区域中的某个下标无效。  

          

   方法族如下：                      　     　

                    Get<PrimitiveType>ArrayRegion方法           数组类型             本地类型

                        GetBooleanArrayRegion()                          jbooleanArray     jboolean

                        GetByteArrayRegion()                                jbyteArray           jbyte

                        GetCharArrayRegion()                               jcharArray           jchar

                        GetShortArrayRegion()                              jshortArray          jhort

                        GetIntArrayRegion()                                  jintArray              jint

                        GetLongArrayRegion()                               jlongArray          jlong

                        GetFloatArrayRegion()                               jfloatArray         jloat

                        GetDoubleArrayRegion()                           jdoubleArray    jdouble

          

                  

###        Set<PrimitiveType>ArrayRegion 方法类型          

 

> void  Set<PrimitiveType>ArrayRegion (JNIEnv *env, ArrayType array,   jsize start, jsize len, NativeType *buf);            

    功能：将基本类型数组的某一区域从缓冲区中复制回来的一组函数。             

        使用说明：  将 Set<PrimitiveType>ArrayRegion 替换为表中的实际基本类型元素访问器例程名。          

                          将 ArrayType 替换为对应的数组类型。             

                          将 NativeType 替换为该例程对应的本地类型。               

    参数： env：JNI 接口指针。            

              array: Java 数组。              

              start：起始下标。                  

              len：要复制的元素数。                 

              buf：源缓冲区。            

    抛出： ArrayIndexOutOfBoundsException：如果区域中的某个下标无效。 

 　     　

                  Set<PrimitiveType>ArrayRegion 方法族            数组类型             本地类型

                        SetBooleanArrayRegion()                          jbooleanArray     jboolean

                        SetByteArrayRegion()                                jbyteArray           jbyte

                        SetCharArrayRegion()                               jcharArray           jchar

                        SetShortArrayRegion()                              jshortArray          jshort

                        SetIntArrayRegion()                                  jintArray              jint

                        SetLongArrayRegion()                               jlongArray           jlong

                        SetFloatArrayRegion()                               jfloatArray           jfloat

                        SetDoubleArrayRegion()                            jdoubleArray      jdouble

       



 

 


##  七、访问对象的属性和方法                  

   

### 1、实例属性的访问

                           

>  jfieldID  GetFieldID (JNIEnv *env, jclass clazz, const char *name, const char *sig);                

   功能：返回类的实例（非静态）域的属性 ID。该域由其名称及签名指定。访问器函数的Get<type>Field 及 Set<type>Field

        系列使用域 ID 检索对象域。GetFieldID() 不能用于获取数组的长度域。应使用GetArrayLength()。          

   参数：  env：JNI 接口指针。            

               clazz：Java 类对象。            

               name: 该属性的Name名称                

               sig：   该属性的域签名。               

   返回值：属性ID。如果操作失败，则返回NULL。              

   抛出： NoSuchFieldError：如果找不到指定的域。                  

              ExceptionInInitializerError：如果由于异常而导致类初始化程序失败。          

              OutOfMemoryError：如果系统内存不足。                 

               

####   Get<type>Field 例程               

 

>   NativeType  Get<type>Field (JNIEnv*env, jobject obj, jfieldID fieldID);                

    功能：该访问器例程系列返回对象的实例（非静态）域的值。要访问的域由通过调用GetFieldID() 而得到的域 ID 指定。           

    参数：   env：JNI 接口指针。            

                 obj：Java 对象（不能为 NULL）。               

                 fieldID：有效的域 ID。                 

    返回值：   属性的内容。      

    　     Get<type>Field 例程名        本地类型        

               GetObjectField()                  jobject     

               GetBooleanField()               jboolean  

               GetByteField()                     jbyte        

               GetCharField()                     jchar        

               GetShortField()                    jshort       

               GetIntField()                        jint  

               GetLongField()                    jlong         

               GetFloatField()                    jfloat        

               GetDoubleField()      jdouble    

 

#### Set<type>Field 方法族 

        

>  void  Set&lt;type>Field (JNIEnv \*env, jobject obj, jfieldID fieldID,  NativeType value);
           
```
功能： 该访问器例程系列设置对象的实例（非静态）属性的值。要访问的属性由通过调用SetFieldID() 而得到的属性 ID指定。


参数：  env：JNI 接口指针。            

       obj：Java 对象（不能为 NULL）。               

       fieldID：有效的域 ID。        

       value：域的新值。   
```

> 方法族 如下：    
             　    

               Set<type>Field 方法族            本地类型        

                  SetObjectField()                    jobject     

                  SetBooleanField()                  jboolean  

                  SetByteField()                       jbyte        

                  SetCharField()                      jchar        

                  SetShortField()                     jshort       

                  SetIntField()                         jint  

                  SetLongField()                      jlong         

                  SetFloatField()                      jfloat        

                  SetDoubleField()                  jdouble    

 

###  2、静态属性的访问 

:也存在相同的方法，

 

> jfieldID  GetStaticFieldID (JNIEnv \*env,jclass clazz, const char \*name, const char *sig);     

> NativeType  GetStatic<type>Field (JNIEnv \*env,jclass classzz , jfieldID fieldID);           

> void  SetStatic<type>Field (JNIEnv \*env,jclassclasszz, jfieldID fieldID,  NativeType value);           

   

它们与实例属性的唯一区别在于第二个参数jclass classzz代表的是类引用，而不是类实例。

        

 ### 3、调用实例方法 

      

> jmethodID GetMethodID(JNIEnv \*env, jclass clazz, const char \*name, const char \*sig); 

```
功能：返回类或接口实例（非静态）方法的方法 ID。方法可在某个 clazz 的超类中定义，也可从 clazz 继承。该方法由其名称和签名决定。 GetMethodID() 可使未初始化的类初始化。要获得构造函数的方法 ID，应将 <init> 作为方法名，同时将 void (V) 作为返回类型。          

参数：  env：JNI 接口指针。            

                clazz：Java 类对象。            

                name：方法名。          

                sig：方法的签名。           

返回值： 方法 ID，如果找不到指定的方法，则为 NULL。             

抛出：    NoSuchMethodError：如果找不到指定方法。            

         ExceptionInInitializerError：如果由于异常而导致类初始化程序失败。          

         OutOfMemoryError：如果系统内存不足。                  
```
                  

####  Call<type>Method 例程  、Call<type>MethodA 例程  、Call<type>MethodV 例程 

              

>  NativeType Call<type>Method (JNIEnv*en v,  jobject obj , jmethodID methodID, ...);     //参数附加在函数后面,              

>  NativeType Call<type>MethodA (JNIEnv *env, jobject obj, jmethodID methodID, jvalue *args);  //参数以指针形式附加  

>  NativeType Call<type>MethodV (JNIEnv *env, jobject obj,jmethodID methodID, va_list args); //参数以"链表"形式附加

     

说明：这三个操作的方法用于从本地方法调用Java 实例方法。它们的差别仅在于向其所调用的方法传递参数时所用的机制。   

这三个操作将根据所指定的方法 ID 调用 Java 对象的实例（非静态）方法。参数 methodID 必须通过调用 GetMethodID() 来获得。当这些函数用于调用私有方法和构造函数时，方法 ID 必须从 obj 的真实类派生而来，而不应从其某个超类派生。

当然，附加参数可以为空 。

```
参数：  env：JNI 接口指针。            

       obj：Java 对象。           

       methodID：方法 ID。                  

返回值： 返回调用 Java 方法的结果。              

抛出：  执行 Java 方法时抛出的异常。    
```
             


下表根据结果类型说明了各个方法类型。用户应将 `Call<type>Method` 中的 type 替换为所调用方法的Java 类型（或使用表中的实际方法名），同时将 NativeType 替换为该方法相应的本地类型。省略掉了其他两种类型。 


 

           Java层返回值                  方法族                                            本地返回类型NativeType



           返回值为void ：          CallVoidMethod( )   A / V                               (无)

           返回值为引用类型：     CallObjectMethod( )                              jobect

           返回值为boolean ：    CallBooleanMethod ( )                           jboolean

           返回值为byte ：          CallByteMethod( )                                  jbyte

           返回值为char  ：         CallCharMethod( )                                 jchar

           返回值为short             CallShortMethod( )                                jshort       

           返回值为int   ：          CallIntMethod( )                                     jint  

           返回值为long：          CallLongMethod()                                   jlong         

           返回值为float ：         CallFloatMethod()                                   jfloat        

           返回值为double：      CallDoubleMethod()                                jdouble    

 

 

### 4、调用静态方法：也存在如下方法群，

 
#### 获取方法
> jfieldID  GetStaticMethodID (JNIEnv *env,jclass clazz, const char *name, const char *sig);     


#### 调用执行
> NativeType Call<type>Method (JNIEnv*env,jclass classzz , jfieldID fieldID);           

它们与于实例方法的唯一区别在于第二个参数jclass classzz代表的是类引用，而不是类实例。


 

## 八、注册本地方法                  

                

>  jint RegisterNatives (JNIEnv \*env, jclass clazz, const JNINativeMethod \*methods,    jint  nMethods);               

```
功能：向 clazz 参数指定的类注册本地方法。methods 参数将指定 JNINativeMethod 结构的数组，其中包含本地方法的名称、签名和函数指针。nMethods 参数将指定数组中的本地方法数。JNINativeMethod 结构定义如下所示：            

         typedef struct {                       
               char *name;          
               char *signature;               
               void *fnPtr;               
         } JNINativeMethod;                  

函数指针通常必须有下列签名：                                  

              ReturnType (*fnPtr)(JNIEnv *env, jobject objectOrClass, ...);                  

                  

参数： env：JNI 接口指针。            

         clazz：Java 类对象。            

         methods：类中本地方法和具体实现方法的映射指针。               

         nMethods：类中的本地方法数。                 

返回值：  成功时返回 "0"；失败时返回负数。         

抛出：  NoSuchMethodError：如果找不到指定的方法或方法不是本地方法。            
```
                  

> jint  UnregisterNatives (JNIEnv *env, jclass clazz);              

```
功能： 取消注册类的本地方法。类将返回到链接或注册了本地方法函数前的状态。
      该函数不应在常规平台相关代码中使用。
      相反，它可以为某些程序提供一种重新加载和重新链接本地库的途径。             

参数：  env：JNI 接口指针。            
       clazz：Java 类对象。            

返回值： 成功时返回“0”；失败时返回负数。                  
```

其实，JNI方面的书籍还是比较少的，建议大家看看《JNI编程指南》，算的上个入门书籍吧，指望你能耐心点看。

