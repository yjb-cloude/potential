public class Animal{
    private String name;
    public Animal(String name){
        if(name == null){
            throw new IllegalArgumentException("name不能为空");
        }
        this.name = name;
    }

    public String getName() {
        return name;
    }
    public void speak() {
        System.out.println(name + " 发出了声音");
    }
}
