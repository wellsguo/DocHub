# Builder 设计模式

```java
public class CustomDialog extends Dialog {

	public CustomDialog(Context context) {
		super(context);
	}

	public CustomDialog(Context context, int theme) {
		super(context, theme);
	}

	public static class Builder {
        // 属性定义
		private Context context;
		private String title;
		private String message;
		private String positiveButtonText;
		private String negativeButtonText;
		private View contentView;
		private OnClickListener positiveButtonClickListener;
		private OnClickListener negativeButtonClickListener;

        // Builder 构造函数 
		public Builder(Context context) {
			this.context = context;
		}

		public Builder setMessage(String message) {
			this.message = message;
			return this;
		}

        // setXXX 方法
		public Builder setMessage(int message) {
			this.message = (String) context.getText(message);
			return this;
		}
        
		// ...

		public Builder setNegativeButton(int negativeButtonText,
				OnClickListener listener) {
			this.negativeButtonText = (String) context
					.getText(negativeButtonText);
			this.negativeButtonClickListener = listener;
			return this;
		}

		public Builder setNegativeButton(String negativeButtonText,
				OnClickListener listener) {
			this.negativeButtonText = negativeButtonText;
			this.negativeButtonClickListener = listener;
			return this;
		}


		public CustomDialog create() {
			LayoutInflater inflater = (LayoutInflater) context.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
			// instantiate the dialog with the custom Theme
			final CustomDialog dialog = new CustomDialog(context,R.style.Dialog); // 实例化对象
			View layout = inflater.inflate(R.layout.dialog_normal_layout, null);
			LinearLayout linearLayoutButton = (LinearLayout)layout.findViewById(R.id.linearLayoutButton);
			dialog.addContentView(layout, new LayoutParams(LayoutParams.MATCH_PARENT, LayoutParams.WRAP_CONTENT));
			// set the dialog title
			((TextView) layout.findViewById(R.id.title)).setText(title);
			// set the confirm button
			if (positiveButtonText != null) {
				((Button) layout.findViewById(R.id.positiveButton))
						.setText(positiveButtonText);
				if (positiveButtonClickListener != null) {
					((Button) layout.findViewById(R.id.positiveButton))
							.setOnClickListener(new View.OnClickListener() {
								public void onClick(View v) {
									positiveButtonClickListener.onClick(dialog,
											DialogInterface.BUTTON_POSITIVE);
								}
							});
				}
			} else {
				// if no confirm button just set the visibility to GONE
				layout.findViewById(R.id.positiveButton).setVisibility(
						View.GONE);
			}
			// set the cancel button
			if (negativeButtonText != null) {
				((Button) layout.findViewById(R.id.negativeButton))
						.setText(negativeButtonText);
				if (negativeButtonClickListener != null) {
					((Button) layout.findViewById(R.id.negativeButton))
							.setOnClickListener(new View.OnClickListener() {
								public void onClick(View v) {
									negativeButtonClickListener.onClick(dialog,
											DialogInterface.BUTTON_NEGATIVE);
								}
							});
				}
			} else {
				// if no confirm button just set the visibility to GONE
				layout.findViewById(R.id.negativeButton).setVisibility(
						View.GONE);
			}
			if(positiveButtonText == null && negativeButtonText == null)
			{
				linearLayoutButton.setVisibility(
						View.GONE);
			}
			// set the content message
			if (message != null) {
				((TextView) layout.findViewById(R.id.message)).setText(message);
			} else if (contentView != null) {
				// if no message set
				// add the contentView to the dialog body
				((LinearLayout) layout.findViewById(R.id.content))
						.removeAllViews();
				((LinearLayout) layout.findViewById(R.id.content)).addView(
						contentView, new LayoutParams(
								LayoutParams.MATCH_PARENT,
								LayoutParams.MATCH_PARENT));
			}
			dialog.setContentView(layout);
			return dialog;
		}

	}
}

```

## 使用场景分析

在《Effective Java 第2版》中有提到，遇到多个构造器参数时要考虑使用构建器（Builder模式）。相比于重叠构造器（telescoping constructor）模式和JavaBeans模式，Builder模式实现的对象更利于使用。 

以Person例子进行分析以上三种设计模式的使用，Person类有两个必要参数（id和name），有5个可选参数（age,sex,phone,address和desc）

### 多个构造器方式
```java
public class Person {
    //必要参数
    private final int id;
    private final String name;
    //可选参数
    private final int age;
    private final String sex;
    private final String phone;
    private final String address;
    private final String desc;

    public Person(int id, String name) { ...  }

    public Person(int id, String name, int age) { ...  }

    public Person(int id, String name, int age, String sex) { ... }

    public Person(int id, String name, int age, String sex, String phone) { ... }

    public Person(int id, String name, int age, String sex, String phone, String address) { ... }

    public Person(int id, String name, int age, String sex, String phone, String address, String desc) { ... }
}
```
当你想要创建实例的时候，就利用参数列表最短的构造器，但该列表中包含了要设置的所有参数：
```java
Person person = new Persion(1, "李四", 20, "男", "18800000000", "China", "测试使用重叠构造器模式");
```
这个构造器调用通常需要许多你本不想设置的参数，但还是不得不为它们传递值。   
**`一句话：`** 重叠构造器可行，但是当有许多参数的时候，创建使用代码会很难写，并且较难以阅读。

### JavaBean 

遇到许多构造器参数的时候，还有第二种代替办法，即JavaBeans模式。在这种模式下，调用一个无参构造器来创建对象，然后调用setter办法来设置每个必要的参数，以及每个相关的可选参数：

```java
**
 * 使用JavaBeans模式
 */
public class Person {
    //必要参数
    private int id;
    private String name;
    //可选参数
    private int age;
    private String sex;
    private String phone;
    private String address;
    private String desc;
    
    // Setter and Getter
}
```

这种模式弥补了重叠构造器模式的不足。创建实例很容易，这样产生的代码读起来也很容易：
```java
Person person = new Person();
person.setId(1);
person.setName("李四");
person.setAge(20);
person.setSex("男");
person.setPhone("18800000000");
person.setAddress("China");
person.setDesc("测试使用JavaBeans模式");
```

**遗憾的是**，JavaBeans模式自身有着很重要的缺点。因为构造过程被分到了几个调用中，在构造过程中JavaBean可能处于**不一致**的状态。类无法仅仅通过检验构造器参数的有效性来保证一致性。

### builder 模式

幸运的是，还有第三种替代方法，既能保证像重叠构造器模式那样的安全性，也能保证像JavaBeans模式那么好的可读性。这就是Builder模式的一种形式，不直接生成想要的对象，而是让客户端利用所有必要的参数调用构造器（或者静态工厂），得到一个builder对象。然后客户端在builder对象上调用类似于setter的方法，来设置每个相关的可选参数。最后，客户端调用无参的builder方法来生成不可变的对象。这个builder是它构建类的静态成员类。

```java
/**
 * 使用Builder模式
 */
public class Person {
    //必要参数
    private final int id;
    private final String name;
    //可选参数
    private final int age;
    private final String sex;
    private final String phone;
    private final String address;
    private final String desc;

    private Person(Builder builder) {
        this.id = builder.id;
        this.name = builder.name;
        this.age = builder.age;
        this.sex = builder.sex;
        this.phone = builder.phone;
        this.address = builder.address;
        this.desc = builder.desc;
    }

    public static class Builder {
        //必要参数
        private final int id;
        private final String name;
        //可选参数
        private int age;
        private String sex;
        private String phone;
        private String address;
        private String desc;

        public Builder(int id, String name) {
            this.id = id;
            this.name = name;
        }

        public Builder age(int val) {
            this.age = val;
            return this;
        }

        public Builder sex(String val) {
            this.sex = val;
            return this;
        }

        public Builder phone(String val) {
            this.phone = val;
            return this;
        }

        public Builder address(String val) {
            this.address = val;
            return this;
        }

        public Builder desc(String val) {
            this.desc = val;
            return this;
        }

        public Person build() {
            return new Person(this);
        }
    }
}
```

**注意** Person是不可变的，所有的默认参数值都单独放在一个地方。builder的setter方法返回builder本身。以便可以把连接起来。

```java
public class Test {

    public static void main(String[] args) {
        Person person = new Person.Builder(1, "张三")
                .age(18).sex("男").desc("测试使用builder模式").build();
        System.out.println(person.toString());
    }
}
```
