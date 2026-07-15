/**
 * 练习：类和对象基础
 * 场景：表示一个学生
 */
public class Student {

    // ===== 第一步：字段（这个类有哪些"属性"） =====
    // private = 藏起来，外部不能直接碰
    // 类型     变量名
    private String name;   // 姓名，是文字所以用 String
    private int age;       // 年龄，是整数所以用 int

    public Student( String name, int age) {
        this.name = name;
        this.age = age;
    }

    // ===== 第三步：getter方法 =====
    public String getName() {return name;}
    public int getAge() {return age;}

    // ===== 第四步：setter方法 =====
    public void setName(String name) {
        if (name == null || name.length() == 0){
            throw new IllegalArgumentException("姓名不能为空");
        }
        this.name = name;
    }
    public void setAge(int age) {
        if (age < 0 || age > 150) {
            throw new IllegalArgumentException("年龄不合理: " + age);
        }
        this.age = age;
    }

    public void show() {
        System.out.println("姓名：" + name + "，年龄：" + age);
    }
    public static void main(String[] args) {
        Student s = new Student("张三", 18);
        s.show();

        s.setAge(19);                        // 过了一年
        System.out.println(s.getName() + " 现在 " + s.getAge() + " 岁 ");
    }
}
