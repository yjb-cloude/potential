public class Cat extends  Animal{
    public Cat(String name) {
        super(name);
    }

    @Override
    public void speak() {
        System.out.println(getName() + " 喵喵喵");
    }
    public static void main(String[] args) {
        Cat cat = new Cat("mimi");
        cat.speak();
    }
}
